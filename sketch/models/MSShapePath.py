from sketch.models.MSCurvePoint import MSCurvePoint


class MSShapePath(object):
    def __init__(self, points, isClosed):
        assert isinstance(points, list)
        for point in points:
            assert isinstance(point, MSCurvePoint)
        self._points = points

        assert isinstance(isClosed, bool)
        self._isClosed = isClosed

    @property
    def points(self):
        return self._points

    @property
    def isClosed(self):
        return self._isClosed

    def __repr__(self):
        return "<MSShapePath \n\
                    points: {points}, \n\
                    isClosed: {isClosed}".format(
                        points=self.points,
                        isClosed=self.isClosed)
