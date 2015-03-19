class GKRect(object):
    """
    GKRect is a lightweight rectangle object that is used in many places in Sketch.
    It has many of the same methods as MSRect but they cannot always be used
    interchangeably
    """
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

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
