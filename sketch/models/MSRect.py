from sketch.models import CGPoint


class MSRect(object):
    """
    Represents a size and position of a layer on the screen. See MSLayer for more information
    """
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = int(width)
        self._height = int(height)

    """
    Base attributes. All floats
    """
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    """
    Adding to any of the base attributes
    """
    def addX(self, x):
        self._x += x

    def addY(self, y):
        self._y += y

    def addWidth(self, width):
        self._width += width

    def addHeight(self, height):
        self._height += height

    def subtractX(self, x):
        self._x -= x

    def subtractY(self, y):
        self._y -= y

    def subtractWidth(self, width):
        self._width -= width

    def subtractHeight(self, height):
        self._height -= height

    """
    For each axis the minimum, middle and maximum of the rectangle. All floats
    """
    @property
    def minX(self):
        return self.x

    @property
    def midX(self):
        return (self.x + self.width) / 2

    @property
    def maxX(self):
        return (self.x + self.width)

    @property
    def minY(self):
        return self.y

    @property
    def midY(self):
        return (self.y + self.height) / 2

    @property
    def maxY(self):
        return (self.y + self.height)

    """
    All point structures, representing a corner each
    """
    @property
    def topLeft(self):
        return CGPoint(self.minX, self.maxY)

    @property
    def topRight(self):
        return CGPoint(self.maxX, self.maxY)

    @property
    def topMiddle(self):
        return CGPoint(self.midX, self.maxY)

    @property
    def bottomLeft(self):
        return CGPoint(self.minX, self.minY)

    @property
    def bottomRight(self):
        return CGPoint(self.maxX, self.minY)

    @property
    def bottomMiddle(self):
        return CGPoint(self.midX, self.minY)

    @property
    def middleLeft(self):
        return CGPoint(self.minX, self.midY)

    @property
    def middleRight(self):
        return CGPoint(self.maxX, self.midY)

    @property
    def middleMiddle(self):
        return CGPoint(self.midX, self.midY)

    def expandBy(self, cgFloat):
        """
        Make the rectangle smaller or larger by adding to each side, or scale the rectangle.
        """
        # Not implemented
        pass

    def constrainProportions(self):
        """
        Keeps the width and height proportionally the same.
        constrainProportions returns a boolean
        """
        # Not implemented
        pass

    def calculateProportions(self):
        """
        Keeps the width and height proportionally the same.
        calculateProportions does exactly what it says on the tin
        """
        # Not implemented
        pass

    def proportions(self):
        """
        proportions returns a float
        """
        # Not implemented
        pass
