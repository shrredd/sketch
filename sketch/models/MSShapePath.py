from sketch.models.MSCurvePoint import MSCurvePoint
from sketch.utils import pairwise


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

    def render(self, surface):
        import gizeh as gz

        for curr_pt, next_pt in pairwise(self.points):
            pt_list = [(curr_pt.point.x, curr_pt.point.y),
                       (next_pt.curveFrom.x, next_pt.curveFrom.y),
                       (next_pt.curveTo.x, next_pt.curveTo.y),
                       (next_pt.point.x, next_pt.point.y)]

            pt_list = [(x * surface.width, y * surface.height) for (x, y) in pt_list]

            print "Point list: %s" % pt_list
            curve = gz.bezier_curve(pt_list,
                                    fill=(0.5, 0.5, 0.5),
                                    stroke_width=1)
            curve.draw(surface)
