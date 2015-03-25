from itertools import chain

from sketch.drawing.shapes import shape_element
from sketch.models.MSLayer import MSLayer
from sketch.models.MSShapePath import MSShapePath
from sketch.utils import pairwise


class MSShapePathLayer(MSLayer):
    def __init__(self, path, booleanOperation,
                 frame, style, name, rotation,
                 isVisible, isLocked,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(path, MSShapePath)
        self._path = path

        assert isinstance(booleanOperation, int)
        self._booleanOperation = booleanOperation

        super(MSShapePathLayer, self).__init__(frame, style, name, rotation,
                                               isVisible, isLocked,
                                               isFlippedHorizontal, isFlippedVertical)

    @property
    def path(self):
        return self._path

    @property
    def booleanOperation(self):
        return self._booleanOperation

    def __repr__(self):
        return "<MSShapePathLayer \n\
                    path: {path}, \n\
                    booleanOperation: {booleanOperation}".format(
                        path=self.path,
                        booleanOperation=self.booleanOperation,)

    def render(self, surface):
        """
        renders the current `MSShapePathLayer` to `surface`
        """
        path = self.to_cairo()
        path.draw(surface)

    def _bezier_curves(self):
        """
        :returns a list of bezier_pts that define the entire shape path.
        each bezier_pt is itself a list of four (x,y) tuples specifying
        the points of an individual bezier curve of the path.
        """
        def _bezier_pts(start, end):
            bezier_pts = [(start.point.x, start.point.y), (start.curveFrom.x, start.curveFrom.y),
                          (end.curveTo.x, end.curveTo.y), (end.point.x, end.point.y)]
            print "x: %s y: %s w: %s h: %s" % (self.frame.x, self.frame.y, self.frame.width, self.frame.height)
            return [(self.frame.x + (x * self.frame.width), self.frame.y + (y * self.frame.height)) for (x, y) in bezier_pts]

        bezier_curves = []
        for _curr, _next in pairwise(self.path.points):
            bezier_curves.append(_bezier_pts(_curr, _next))

        if self.path.isClosed and len(self.path.points) >= 1:
            bezier_curves.append(_bezier_pts(self.path.points[-1], self.path.points[0]))

        return bezier_curves

    def to_cairo(self):
        """
        :returns a Cairo Element corresponding to this ShapePath
        """
        def draw(ctx):
            bezier_curves = self._bezier_curves()
            for curve_pts in bezier_curves:
                ctx.move_to(*curve_pts[0])
                ctx.curve_to(*tuple(chain(*curve_pts))[2:])

        return shape_element(draw, stroke_width=1)


##############################################################
#   LEAVING HERE IN CASE WE NEED TO EXTEND MSSHAPEPATHLAYER  #
##############################################################

class MSRectangleShape(MSShapePathLayer):
    pass


class MSStarShape(MSShapePathLayer):
    pass


class MSPolygonShape(MSShapePathLayer):
    pass


class MSOvalShape(MSShapePathLayer):
    pass


class MSTriangleShape(MSShapePathLayer):
    pass
