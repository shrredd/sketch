class MSStyleBorder(object):
    """
    Represents a border on a layer. Can be either a color or gradient fill
    """
    @property
    def position(self):
        """ The position of the layer; Center (0), Inside (1) or Outside (2). """
        pass

    @property
    def thickness(self):
        """ The thickness of the border as a float value. """
        pass

    @property
    def fillType(self):
        """
        A color fill (0) or a gradient (1). Other values make no sense and
        can lead to unpredictable behaviour.
        """
        pass

    @property
    def gradient(self):
        """
        An MSGradient object that will only be used if the fillType is set to a gradient.
        """
        pass

    @property
    def isEnabled(self):
        """
        Whether the style object is enabled or not
        """
        pass
