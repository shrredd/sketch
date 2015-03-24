"""
Translates plain ol' Binary Plist data into sketch.model objects
"""
import datetime

from sketch.bplist import UID
from sketch.models.MSCurvePoint import MSCurvePoint
from sketch.models.MSDocumentData import MSDocumentData
from sketch.models.MSImageCollection import MSImageCollection
from sketch.models.MSLayer import MSLayer
from sketch.models.MSLayerGroup import MSLayerGroup
from sketch.models.MSPage import MSPage
from sketch.models.MSRect import MSRect
from sketch.models.MSShapePath import MSShapePath
from sketch.models.MSShapePathLayer import MSShapePathLayer


##############################################################
#                  MSARCHIVER CONVERTER FUNCTIONS            #
##############################################################
def MSArchiver_object_converter(o):
    """
    Built in converter function (suitable for submission to set_object_converter())
    which automatically converts the following common data-types found in MSArchiver:
        * NSDictionary/NSMutableDictionary;
        * NSArray/NSMutableArray;
        * NSSet/NSMutableSet
        * NSString/NSMutableString
        * NSDate
        * $null strings
    """
    if is_MSDocumentData(o):
        return convert_MSDocumentData(o)

    if is_MSPage(o):
        return convert_MSPage(o)

    if is_MSLayerGroup(o):
        return convert_MSLayerGroup(o)

    if is_MSLayer(o):
        return convert_MSLayer(o)

    if is_MSShapePathLayer(o):
        return convert_MSShapePathLayer(o)

    if is_MSShapePath(o):
        return convert_MSShapePath(o)

    if is_MSCurvePoint(o):
        return convert_MSCurvePoint(o)

    if is_MSRect(o):
        return convert_MSRect(o)

    if is_MSImageCollection(o):
        return convert_MSImageCollection(o)

    if is_MSArray(o):
        return convert_MSArray(o)

    if is_NSArray(o):
        return convert_NSArray(o)

    if is_NSSet(o):
        return convert_NSSet(o)

    if is_NSMutableDictionary(o):
        return convert_NSMutableDictionary(o)

    elif is_NSString(o):
        return convert_NSString(o)

    if is_NSDate(o):
        return convert_NSDate(o)

    # Conversion: "$null" string
    if isinstance(o, str) and o == "$null":
        return None

    # Fallback:
    return o


def MSArchiver_convert(o, object_table):
    if isinstance(o, list):
        result = MSArchiverList(o, object_table)
    elif isinstance(o, dict):
        result = MSArchiverDictionary(o, object_table)
    elif isinstance(o, UID):
        result = MSArchiver_convert(object_table[o.value], object_table)
    else:
        result = o

    return MSArchiver_object_converter(result)


class MSArchiverDictionary(dict):
    def __init__(self, original_dict, object_table):
        super(MSArchiverDictionary, self).__init__(original_dict)
        self.object_table = object_table

    def __getitem__(self, index):
        o = super(MSArchiverDictionary, self).__getitem__(index)
        return MSArchiver_convert(o, self.object_table)

    def get(self, key, default=None):
        return self[key] if key in self else default


class MSArchiverList(list):
    def __init__(self, original_iterable, object_table):
        super(MSArchiverList, self).__init__(original_iterable)
        self.object_table = object_table

    def __getitem__(self, index):
        o = super(MSArchiverList, self).__getitem__(index)
        return MSArchiver_convert(o, self.object_table)

    def __iter__(self):
        for o in super(MSArchiverList, self).__iter__():
            yield MSArchiver_convert(o, self.object_table)


def deserialize(obj):
    """
    Deserializes a Sketch bplist rebuilding the structure.
    obj should be the object returned by the bplist.load()
    function
    """

    # Check that this is an archiver and version we understand
    if not isinstance(obj, dict):
        raise TypeError("obj must be a dict")
    if "$archiver" not in obj or obj["$archiver"] != "MSArchiver":
        raise ValueError("obj does not contain an '$archiver' key or the '$archiver' is unrecognised")
    if "$version" not in obj or obj["$version"] != 100000:
        raise ValueError("obj does not contain a '$version' key or the '$version' is unrecognised")

    object_table = obj["$objects"]
    if "root" in obj["$top"]:
        return MSArchiver_convert(obj["$top"]["root"], object_table)
    else:
        return MSArchiver_convert(obj["$top"], object_table)


##############################################################
#                  MSDOCUMENTDATA FUNCTIONS                  #
##############################################################
def is_MSDocumentData(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSDocumentData"):
        return False

    return True


def convert_MSDocumentData(obj):
    if not is_MSDocumentData(obj):
        raise ValueError("obj does not have the correct structure for a MSDocumentData")

    return MSDocumentData(
        images=obj["images"],
        pages=obj["pages"],

        currentPageIndex=obj["currentPageIndex"],
        enableSliceInteraction=obj["enableSliceInteraction"],
        enableLayerInteraction=obj["enableLayerInteraction"],

        layerStyles=obj["layerStyles"],
        layerSymbols=obj["layerSymbols"],
        layerTextStyles=obj["layerTextStyles"],

        objectID=obj.get("do_objectID"),
    )


##############################################################
#                  MSPAGE FUNCTIONS               #
##############################################################
def is_MSPage(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSPage"):
        return False

    return True


def convert_MSPage(obj):
    if not is_MSPage(obj):
        raise ValueError("obj does not have the correct structure for an MSPage")

    return MSPage(horizontalRulerData=obj["horizontalRulerData"],
                  verticalRulerData=obj["verticalRulerData"],

                  layers=obj["layers"],

                  frame=obj["frame"],
                  style=obj["style"],
                  name=obj["name"],
                  rotation=obj["rotation"],

                  isVisible=obj["isVisible"],
                  isLocked=obj["isLocked"],

                  isFlippedHorizontal=obj["isFlippedHorizontal"],
                  isFlippedVertical=obj["isFlippedVertical"])


##############################################################
#                  MSLAYERGROUP FUNCTIONS                    #
##############################################################
def is_MSLayerGroup(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSLayerGroup", "MSShapeGroup"):
        return False

    return True


def convert_MSLayerGroup(obj):
    if not is_MSLayerGroup(obj):
        raise ValueError("obj does not have the correct structure for an MSLayerGroup")

    return MSLayerGroup(layers=obj["layers"],

                        frame=obj["frame"],
                        style=obj["style"],
                        name=obj["name"],
                        rotation=obj["rotation"],

                        isVisible=obj["isVisible"],
                        isLocked=obj["isLocked"],

                        isFlippedHorizontal=obj["isFlippedHorizontal"],
                        isFlippedVertical=obj["isFlippedVertical"])


##############################################################
#                  MSLAYER FUNCTIONS                         #
##############################################################
def is_MSLayer(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSLayer"):
        return False

    return True


def convert_MSLayer(obj):
    if not is_MSLayer(obj):
        raise ValueError("obj does not have the correct structure for an MSLayer")

    return MSLayer(frame=obj["frame"],
                   style=obj["style"],
                   name=obj["name"],
                   rotation=obj["rotation"],

                   isVisible=obj["isVisible"],
                   isLocked=obj["isLocked"],

                   isFlippedHorizontal=obj["isFlippedHorizontal"],
                   isFlippedVertical=obj["isFlippedVertical"])


##############################################################
#                  MSSHAPEPATHLAYER FUNCTIONS                #
##############################################################
def is_MSShapePathLayer(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSRectangleShape", "MSStarShape", "MSPolygonShape", "MSOvalShape", "MSShapePathLayer"):
        return False

    return True


def convert_MSShapePathLayer(obj):
    if not is_MSShapePathLayer(obj):
        raise ValueError("obj does not have the correct structure for an MSShapePathLayer")

    return MSShapePathLayer(path=obj["path"],
                            fixedRadius=obj.get("fixedRadius"),
                            booleanOperation=obj["booleanOperation"],

                            frame=obj["frame"],
                            style=obj.get("style"),
                            name=obj["name"],
                            rotation=obj["rotation"],

                            isVisible=obj["isVisible"],
                            isLocked=obj["isLocked"],

                            isFlippedHorizontal=obj["isFlippedHorizontal"],
                            isFlippedVertical=obj["isFlippedVertical"])


##############################################################
#                  MSSHAPEPATH FUNCTIONS                #
##############################################################
def is_MSShapePath(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSShapePath"):
        return False

    return True


def convert_MSShapePath(obj):
    if not is_MSShapePath(obj):
        raise ValueError("obj does not have the correct structure for an MSShapePath")

    return MSShapePath(points=obj["points"],
                       isClosed=obj["isClosed"])


##############################################################
#                  MSCURVEPOINT FUNCTIONS                    #
##############################################################
def is_MSCurvePoint(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSCurvePoint"):
        return False

    return True


def convert_MSCurvePoint(obj):
    if not is_MSCurvePoint(obj):
        raise ValueError("obj does not have the correct structure for an MSCurvePoint")

    return MSCurvePoint(curveFrom=obj["curveFrom"],
                        curveTo=obj["curveTo"],
                        point=obj["point"],
                        curveMode=obj["curveMode"],
                        cornerRadius=obj["cornerRadius"])


##############################################################
#                  MSRECT FUNCTIONS                          #
##############################################################
def is_MSRect(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSRect"):
        return False

    return True


def convert_MSRect(obj):
    if not is_MSRect(obj):
        raise ValueError("obj does not have the correct structure for an MSRect")

    return MSRect(x=obj["x"],
                  y=obj["y"],
                  width=obj["width"],
                  height=obj["height"])

# ##############################################################
# #                  MSRULERDATA FUNCTIONS                     #
# ##############################################################
# def is_MSRulerData(obj):
#     if not isinstance(obj, dict):
#         return False
#     if "$class" not in obj.keys():
#         return False
#     if obj["$class"].get("$classname") not in ("MSRulerData"):
#         return False

#     return True

##############################################################
#                  MSIMAGECOLLECTION FUNCTIONS               #
##############################################################
def is_MSImageCollection(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSImageCollection"):
        return False

    return True


def convert_MSImageCollection(obj):
    if not is_MSImageCollection(obj):
        raise ValueError("obj does not have the correct structure for an MSImageCollection")

    return MSImageCollection(images=obj["images"])


##############################################################
#                  MSARRAY FUNCTIONS                         #
##############################################################
def is_MSArray(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("MSArray"):
        return False
    if "array_do" not in obj.keys():
        return False

    return True


def convert_MSArray(obj):
    if not is_MSArray(obj):
        raise ValueError("obj does not have the correct structure for an MSArray")

    return obj["array_do"]


##############################################################
#                  NSMUTABLEDICTIONARY FUNCTIONS             #
##############################################################
def is_NSMutableDictionary(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("NSMutableDictionary", "NSDictionary"):
        return False
    if "NS.keys" not in obj.keys():
        return False
    if "NS.objects" not in obj.keys():
        return False

    return True


def convert_NSMutableDictionary(obj):
    """
    Converts an MSArchiver serialised NSMutableDictionary into
    a straight dictionary (rather than two lists as it is serialised
    as)
    """

    if not is_NSMutableDictionary(obj):
        raise ValueError("obj does not have the correct structure for a NSDictionary/NSMutableDictionary")
    keys = obj["NS.keys"]
    vals = obj["NS.objects"]

    # sense check the keys and values:
    if not isinstance(keys, list):
        raise TypeError("The 'NS.keys' value is an unexpected type (expected list; actual: {0}".format(type(keys)))
    if not isinstance(vals, list):
        raise TypeError("The 'NS.objects' value is an unexpected type (expected list; actual: {0}".format(type(vals)))
    if len(keys) != len(vals):
        raise ValueError("The length of the 'NS.keys' list ({0}) is not equal to that of the 'NS.objects ({1})".format(len(keys), len(vals)))

    result = {}
    for i, k in enumerate(keys):
        if k in result:
            raise ValueError("The 'NS.keys' list contains duplicate entries")
        result[k] = vals[i]

    return result


##############################################################
#                  NSARRAY FUNCTIONS                         #
##############################################################
def has_individual_keys(raw_keys):
    return reduce(lambda x, y: x or y,
                  [key.startswith("NS.object.") for key in raw_keys])


def extract_individual_keys(raw_keys):
    individual_keys = [key for key in raw_keys if key.startswith("NS.object.")]
    individual_keys.sort(key=lambda x: int(x.lstrip("NS.object.")))
    return individual_keys


def is_NSArray(obj):
    """
    An NSArray can either be a keyed as a list w/ "NS.objects" or have
    individual keys such as NS.object.0, NS.object.1, etc.
    """
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("NSArray", "NSMutableArray"):
        return False

    if "NS.objects" not in obj.keys() and not has_individual_keys(obj.keys()):
        return False

    return True


def convert_NSArray(obj):
    if not is_NSArray(obj):
        raise ValueError("obj does not have the correct structure for a NSArray/NSMutableArray")

    if has_individual_keys(obj.keys()):
        individual_keys = extract_individual_keys(obj.keys())
        return [obj[key] for key in individual_keys]

    return obj["NS.objects"]


##############################################################
#                  NSSET FUNCTIONS                           #
##############################################################
def is_NSSet(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("NSSet", "NSMutableSet"):
        return False
    if "NS.objects" not in obj.keys():
        return False

    return True


def convert_NSSet(obj):
    if not is_NSSet(obj):
        raise ValueError("obj does not have the correct structure for a NSSet/NSMutableSet")

    return set(obj["NS.objects"])


##############################################################
#                  NSSTRING FUNCTIONS                        #
##############################################################
def is_NSString(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("NSString", "NSMutableString"):
        return False
    if "NS.string" not in obj.keys():
        return False
    return True


def convert_NSString(obj):
    if not is_NSString(obj):
        raise ValueError("obj does not have the correct structure for a NSString/NSMutableString")

    return obj["NS.string"]


##############################################################
#                  NSDATE FUNCTIONS                          #
##############################################################
def is_NSDate(obj):
    if not isinstance(obj, dict):
        return False
    if "$class" not in obj.keys():
        return False
    if obj["$class"].get("$classname") not in ("NSDate"):
        return False
    if "NS.time" not in obj.keys():
        return False

    return True


def convert_NSDate(obj):
    if not is_NSDate(obj):
        raise ValueError("obj does not have the correct structure for a NSDate")

    return datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=obj["NS.time"])
