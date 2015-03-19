import sqlite3
import io

from sketch import (
    bplist,
    converter
)


def _fetch_plist(filename):
    """ Retrieves the embedded plist from the Sketch doc """
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute("select value from payload where name='main'")
    payload = c.fetchone()[0]
    plist_obj = io.BytesIO(payload)

    conn.close()

    return plist_obj


def _parse_plist(plist_obj):
    """ Parses Sketch's raw plist info into an MSDocumentData object """
    plist_data = bplist.read(plist_obj)
    return converter.deserialize(plist_data)


def read(filename):
    """ Reads and parses a Sketch document into an MSDocumentData object """
    assert isinstance(filename, basestring)

    plist_obj = _fetch_plist(filename)
    return _parse_plist(plist_obj)
