from enum import Enum


class BlendMode(Enum):
    Normal = 0
    Darken = 1
    Multiply = 2
    Color_Burn = 3
    Lighten = 4
    Screen = 5
    Color_Dodge = 6
    Overlay = 7
    Soft_Light = 8
    Hard_Light = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15
    Source_In = 16
    Source_Out = 17
    Source_Atop = 18
    Destination_Over = 19
    Destination_In = 20
    Destination_Out = 21
    Destination_Atop = 22


class MSGraphicsContextSettings(object):
    """
    This class holds Opacity and Blending for its associated layer or style.
    Each layer fill also has a ContextSettings such that we can vary opacity between fills.
    """

    @property
    def opacity(self):
        """ A float between 0 and 1 """
        pass

    @property
    def blendMode(self):
        """
        The blending mode for the layer or fill. See BlendMode for possible values
        """
        pass
