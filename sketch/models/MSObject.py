class MSObject(object):
    def __init__(self, objectID):
        self._objectID = objectID

    @property
    def objectID(self):
        """ <str> """
        return self._objectID
