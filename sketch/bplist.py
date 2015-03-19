import sys
import os
import struct
import datetime


class DataIntegrityError(Exception):
    pass


class UID:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "UID: {0}".format(self.value)

    def __str__(self):
        return self.__repr__()


##############################################################
#                  DECODING FUNCTIONS                        #
##############################################################
def __decode_multibyte_int(b, signed=True):
    if len(b) == 1:
        fmt = ">B"  # Always unsigned?
    elif len(b) == 2:
        fmt = ">h"
    elif len(b) == 3:
        if signed:
            return ((b[0] << 16) | struct.unpack(">H", b[1:])[0]) - ((b[0] >> 7) * 2 * 0x800000)
        else:
            return (b[0] << 16) | struct.unpack(">H", b[1:])[0]
    elif len(b) == 4:
        fmt = ">i"
    elif len(b) == 8:
        fmt = ">q"
    else:
        raise DataIntegrityError("Cannot decode multibyte int of length {0}".format(len(b)))

    if signed and len(b) > 1:
        return struct.unpack(fmt.lower(), b)[0]
    else:
        return struct.unpack(fmt.upper(), b)[0]


def __decode_float(b, signed=True):
    if len(b) == 4:
        fmt = ">f"
    elif len(b) == 8:
        fmt = ">d"
    else:
        raise DataIntegrityError("Cannot decode float of length {0}".format(len(b)))

    if signed:
        return struct.unpack(fmt.lower(), b)[0]
    else:
        return struct.unpack(fmt.upper(), b)[0]


def __decode_object(f, offset, collection_offset_size, offset_table):
    # Move to offset and read type
    f.seek(offset)

    type_byte = read_next_byte(f)

    if type_byte == 0x00:                   # Null    0000 0000
        return None
    elif type_byte == 0x08:                 # False   0000 1000
        return False
    elif type_byte == 0x09:                 # True    0000 1001
        return True
    elif type_byte == 0x0F:                 # Fill    0000 1111
        raise DataIntegrityError("Fill type not currently supported at offset {0}".format(f.tell()))
    elif type_byte & 0xF0 == 0x10:          # Int     0001 xxxx
        return read_int(f, type_byte)
    elif type_byte & 0xF0 == 0x20:          # Float   0010 nnnn
        return read_float(f, type_byte)
    elif type_byte & 0xFF == 0x33:          # Date    0011 0011
        return read_date(f)
    elif type_byte & 0xF0 == 0x40:          # Data    0100 nnnn
        return read_data(f, type_byte)
    elif type_byte & 0xF0 == 0x50:          # ASCII   0101 nnnn
        return read_ascii(f, type_byte)
    elif type_byte & 0xF0 == 0x60:          # UTF-16  0110 nnnn
        return read_utf16(f, type_byte)
    elif type_byte & 0xF0 == 0x80:          # UID     1000 nnnn
        return read_uid(f, type_byte)
    elif type_byte & 0xF0 == 0xA0:          # Array   1010 nnnn
        return read_array(f, type_byte, collection_offset_size, offset_table)
    elif type_byte & 0xF0 == 0xC0:          # Set     1010 nnnn
        return read_set(f, type_byte, collection_offset_size, offset_table)
    elif type_byte & 0xF0 == 0xD0:          # Dict    1011 nnnn
        return read_dict(f, type_byte, collection_offset_size, offset_table)


##############################################################
#                  DATA READING FUNCTIONS                    #
##############################################################
def read_next_byte(f):
    # A little hack to keep the script portable between py2.x and py3k
    if sys.version_info[0] < 3:
        next_byte = ord(f.read(1)[0])
    else:
        next_byte = f.read(1)[0]
    return next_byte


def verify_next_byte_int(f):
    # Verifies that the next byte is an int. Raises BplistError if not
    int_type_byte = read_next_byte(f)
    if int_type_byte & 0xF0 != 0x10:
        raise DataIntegrityError("Definition not followed by int type at offset {0}".format(f.tell()))
    return int_type_byte


def read_int(f, type_byte, signed=True):
    int_length = 2 ** (type_byte & 0x0F)
    int_bytes = f.read(int_length)
    return __decode_multibyte_int(int_bytes, signed=signed)


def read_float(f, type_byte):
    float_length = 2 ** (type_byte & 0x0F)
    float_bytes = f.read(float_length)
    return __decode_float(float_bytes)


def read_date(f):
    date_bytes = f.read(8)
    date_value = __decode_float(date_bytes)
    try:
        result = datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=date_value)
    except OverflowError:
        result = datetime.datetime.min
    return result


def read_data(f, type_byte):
    if type_byte & 0x0F != 0x0F:
        # length in 4 lsb
        data_length = type_byte & 0x0F
    else:
        int_type_byte = verify_next_byte_int(f)
        data_length = read_int(f, int_type_byte, signed=False)

    return f.read(data_length)


def read_ascii(f, type_byte):
    if type_byte & 0x0F != 0x0F:
        # length in 4 lsb
        ascii_length = type_byte & 0x0F
    else:
        int_type_byte = verify_next_byte_int(f)
        ascii_length = read_int(f, int_type_byte, signed=False)

    return f.read(ascii_length).decode("ascii")


def read_utf16(f, type_byte):
    if type_byte & 0x0F != 0x0F:
        # length in 4 lsb
        utf16_length = (type_byte & 0x0F) * 2  # Length is characters - 16bit width
    else:
        int_type_byte = verify_next_byte_int(f)
        utf16_length = read_int(f, int_type_byte, signed=False) * 2

    return f.read(utf16_length).decode("utf_16_be")


def read_uid(f, type_byte):
    uid_length = (type_byte & 0x0F) + 1
    uid_bytes = f.read(uid_length)
    return UID(__decode_multibyte_int(uid_bytes, signed=False))


def read_array(f, type_byte, collection_offset_size, offset_table):
    if type_byte & 0x0F != 0x0F:
        # length in 4 lsb
        array_count = type_byte & 0x0F
    else:
        int_type_byte = verify_next_byte_int(f)
        array_count = read_int(f, int_type_byte, signed=False)

    array_refs = []
    for i in range(array_count):
        array_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))
    return [__decode_object(f, offset_table[obj_ref], collection_offset_size, offset_table) for obj_ref in array_refs]


def read_set(f, type_byte, collection_offset_size, offset_table):
    if type_byte & 0x0F != 0x0F:
        # length in 4 lsb
        set_count = type_byte & 0x0F
    else:
        int_type_byte = verify_next_byte_int(f)
        set_count = read_int(f, int_type_byte, signed=False)

    set_refs = []
    for i in range(set_count):
        set_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))
    return [__decode_object(f, offset_table[obj_ref], collection_offset_size, offset_table) for obj_ref in set_refs]


def read_dict(f, type_byte, collection_offset_size, offset_table):
    if type_byte & 0x0F != 0x0F:
        # length in 4 lsb
        dict_count = type_byte & 0x0F
    else:
        int_type_byte = verify_next_byte_int(f)
        dict_count = read_int(f, int_type_byte, signed=False)

    key_refs = []

    for i in range(dict_count):
        key_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))
    value_refs = []
    for i in range(dict_count):
        value_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))

    dict_result = {}
    for i in range(dict_count):
        key = __decode_object(f, offset_table[key_refs[i]], collection_offset_size, offset_table)
        val = __decode_object(f, offset_table[value_refs[i]], collection_offset_size, offset_table)
        dict_result[key] = val
    return dict_result


##############################################################
#                      ENTRY POINT                           #
##############################################################
def read(f):
    """
    Reads a file-like object containing a binary property list.
    :param f: Any file-like object that supports reading and seeking
    :return: A data structure representing the data in the property list
    """
    # Verify header
    f.seek(0)
    header = f.read(8)
    if header != b"bplist00":
        raise DataIntegrityError("Bad file header")

    # Read footer
    f.seek(-32, os.SEEK_END)
    footer = f.read(32)
    offset_int_size, collection_offset_size, \
        object_count, top_level_object_index, offest_table_offset = struct.unpack(">6xbbQQQ", footer)

    # Read offset table
    f.seek(offest_table_offset)
    offset_table = []
    for i in range(object_count):
        offset_table.append(__decode_multibyte_int(f.read(offset_int_size), False))

    return __decode_object(f, offset_table[top_level_object_index], collection_offset_size, offset_table)
