from sketch.models.CGPoint import CGPoint


def parsePoint(storedPt):
    """
    Translates a string of the form "{1, 0}" into a float tuple (1.0, 0.0)
    """
    return tuple(float(c) for c in storedPt.strip("{}").split(","))


class MSCurvePoint(object):

    def __init__(self, curveFrom, curveTo, point, curveMode, cornerRadius):
        # curveFrom, curveTo are stored as <unicode> in the form "{x, y}"
        assert isinstance(curveFrom, unicode)
        (x, y) = parsePoint(curveFrom)
        self.curveFrom = CGPoint(x, y)

        assert isinstance(curveTo, unicode)
        (x, y) = parsePoint(curveTo)
        self.curveTo = CGPoint(x, y)

        assert isinstance(point, unicode)
        (x, y) = parsePoint(point)
        self.point = CGPoint(x, y)

        assert isinstance(curveMode, int)
        self._curveMode = curveMode

        assert isinstance(cornerRadius, float)
        self._cornerRadius = cornerRadius

    def __repr__(self):
        return "<MSCurvePoint curveFrom: {curveFrom} curveTo: {curveTo} point: {point}".format(
            curveFrom=self.curveFrom,
            curveTo=self.curveTo,
            point=self.point)
