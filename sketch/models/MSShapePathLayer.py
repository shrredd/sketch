from sketch.models.MSLayer import MSLayer
from sketch.models.MSShapePath import MSShapePath


class MSShapePathLayer(MSLayer):
    def __init__(self, path, fixedRadius, booleanOperation,
                 frame, style, name, rotation,
                 isVisible, isLocked,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(path, MSShapePath)
        self._path = path

        assert isinstance(fixedRadius, float)
        self._fixedRadius = fixedRadius

        assert isinstance(booleanOperation, int)
        self._booleanOperation = booleanOperation

        super(MSShapePathLayer, self).__init__(frame, style, name, rotation,
                                               isVisible, isLocked,
                                               isFlippedHorizontal, isFlippedVertical)

    @property
    def path(self):
        return self._path

    @property
    def fixedRadius(self):
        return self._fixedRadius

    @property
    def booleanOperation(self):
        return self._booleanOperation

    def __repr__(self):
        return "<MSShapePathLayer \n\
                    path: {path}, \n\
                    fixedRadius: {fixedRadius}, \n\
                    booleanOperation: {booleanOperation}".format(
                        path=self.path,
                        fixedRadius=self.fixedRadius,
                        booleanOperation=self.booleanOperation,)

    def render(self):
        print "Frame width: %s frame height: %s" % (self.frame.width, self.frame.height)
        import gizeh as gz
        surface = gz.Surface(self.frame.width, self.frame.height)
        self.path.render(surface)
        surface.write_to_png("/Users/shravan/Desktop/output.png")


class MSRectangleShape(MSShapePathLayer):
    pass
