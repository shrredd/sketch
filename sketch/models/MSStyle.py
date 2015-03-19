class MSStyle(object):
    """
    Represents all style attributes on a layer. Whatever kind of layer you have,
    each has a valid style object.

    Some layers will ignore unsupported attributes though (such as a text layer
    only supports one border even if style objects has more than one).
    """

    """
    Each returns an MSStylePartCollection that contains an array of each
    represented object. See MSStyleBorder, MSStyleFill, MSStyleShadow and
    MSStyleInnerShadow for details.
    """

    @property
    def borders(self):
        pass

    @property
    def fills(self):
        pass

    @property
    def shadows(self):
        pass

    @property
    def innerShadows(self):
        pass

    @property
    def contextSettings(self):
        """
        Contains an MSGraphicsContextSettings object that holds the opacity
        and blending mode of its layer
        """
        pass
