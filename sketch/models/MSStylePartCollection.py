class MSStylePartCollection(object):
    """
    Basically a wrapper around an array that holds style objects such as
    fill, border and more. See MSStyle for possible values.
    """
    def array(self):
        """
        Returns the standard NSArray containing the objects. However, do not
        add objects to this array directly. Instead use the ones below
        (an added benefit of doing that is you can participate in the undo stack for free).
        """
        pass

    def addNewStylePart(self):
        """
        Adds a new style object to the list, this one will have the default values
        that the user set and that make sense for the particular collection. For
        example, a first fill will always be a flat color but a second one will
        have a half transparent gradient.
        """
        # Not implemented
        pass

    def removeStylePart(self):
        # Not implemented
        pass

    def removeStylePartAtIndex(self):
        """
        Remove either a specific style, or one at an index from the list
        """
        # Not implemented
        pass

    def moveStylePart(self, fromIndex, toIndex):
        """ Reorder styles in the list; moves an object from one index to another """
        # Not implemented
        pass
