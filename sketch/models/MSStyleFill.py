class MSStyleFill(object):
    """
    Represents a fill on a layer. Can be either a color or gradient fill.
    """
    @property
    def fillType(self):
        """
        A color fill (0), gradient (1) or pattern (4). Other values make no sense and
        can lead to unpredictable behaviour
        """
        pass

    @property
    def gradient(self):
        """
        An MSGradient object that will only be used if the fillType is set to a gradient.
        """
        pass

    @property
    def image(self):
        """
        An NSImage object that will be used if the fillType is set to pattern
        """
        pass

    @property
    def noiseIntensity(self):
        """
        Sketch 2.0: A float representing the intensity of the noise from 0..1
        """
        pass

    @property
    def isEnabled(self):
        """
        Whether the style object is enabled or not
        """
        pass
