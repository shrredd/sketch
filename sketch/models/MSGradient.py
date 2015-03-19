from enum import Enum


class GradientType(Enum):
    Linear = 0
    Radial = 1


class MSGradient(object):
    @property
    def gradientType(self):
        """
        Either Linear (0) or Radial (1)
        """
        pass

    @property
    def from_(self):
        """
        Point are point structures in the coordinate system of the layer.
        For example: from (0,0) to (1,1) makes the gradient from top left to bottom right.
        """
        pass

    @property
    def to(self):
        """
        Point are point structures in the coordinate system of the layer.
        For example: from (0,0) to (1,1) makes the gradient from top left to bottom right.
        """
        pass

    @property
    def stops(self):
        """
        An array of MSGradientStop objects representing color and position (0..1) on the line
        between the from and to points.
        """
        pass

    def addStopAtLength(self, length):
        """
        Adds a new stop on the line from 0..1
        """
        # Not implemented
        pass

    def removeStopAtIndex(self, index):
        """
        Removes a stop at the specified index
        """
        # Not implemented
        pass

    def setColor(self, color, atIndex):
        """
        Set the color of gradient stop at the given index
        """
        # Not implemented
        pass
