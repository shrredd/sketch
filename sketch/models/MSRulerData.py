class MSRulerData(object):
    """
    Stores the guides used on its ruler. MSPage and MSArtboardGroup both return their ruler
    data using horizontalRulerData and verticalRulerData.
    """
    def addGuideWithValue(self, value):
        """
        Supply an integer value (measured from the origin of the ruler). Adds a new guide at the given value.
        """
        # Not implemented
        pass

    def numberOfGuides(self):
        """
        Returns the number of guides on this ruler.
        """
        pass

    def guideAtIndex(self, index):
        """
        Returns the integer value of the given guide. The argument is a zero-based index value.
        """
        pass

    def removeGuideAtIndex(self, index):
        """
        Remove the guide at the given index.
        """
        # Not implemented
        pass
