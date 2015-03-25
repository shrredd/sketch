from sketch.models.MSRect import MSRect
from sketch.models.MSStyle import MSStyle


class MSLayer(object):
    def __init__(self, frame, style, name, rotation,
                 isVisible, isLocked,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(frame, MSRect)
        self._frame = frame

        assert isinstance(style, MSStyle)
        self._style = style

        assert isinstance(name, basestring)
        self._name = name

        assert isinstance(rotation, float)
        self._rotation = rotation

        assert isinstance(isVisible, bool)
        assert isinstance(isLocked, bool)

        self._isVisible = isVisible
        self._isLocked = isLocked

        assert isinstance(isFlippedHorizontal, bool)
        assert isinstance(isFlippedVertical, bool)
        self._isFlippedHorizontal = isFlippedHorizontal
        self._isFlippedVertical = isFlippedVertical

        super(MSLayer, self).__init__()

    @property
    def frame(self):
        """
        An instance of MSRect. Determines size and position on
        the canvas. (readonly)
        """
        return self._frame

    @property
    def style(self):
        """
        An instance of MSStyle. Determines all style-related attributes
        such as Borders, Fills, Shadows and more. (readonly)
        """
        return self._style

    @property
    def name(self):
        """
        The name of the layer as it appears in the layer list. <str>
        """
        return self._name

    @property
    def isVisible(self):
        """
        Returns true if the layer is visible, and false if it is hidden.
        """
        return self._isVisible

    @property
    def isLocked(self):
        """
        Returns true if the layer is locked, and false if it isn't locked.
        """
        return self._isLocked

    @property
    def rotation(self):
        """
        An integer denoting the rotation of the layer - in degrees.
        Rotation happens counter-clockwise.
        """
        return self._rotation

    @property
    def isFlippedHorizontal(self):
        """
        Returns true if the layer is flipped horizontally.
        """
        return self._isFlippedHorizontal

    @property
    def isFlippedVertical(self):
        """
        Returns true if the layer is flipped vertically.
        """
        return self._isFlippedVertical

    def parentGroup(self):
        """
        Returns the parent group of this layer. Note that this can return an
        MSPage or MSArtboardGroup as well as an MSLayerGroup
        """
        # Not implemented
        pass

    @property
    def isSelected(self):
        """
        True if the layer is selected, false otherwise
        """
        # Not implemented
        pass

    def select(self, shouldSelect=True, byExpandingSelection=False):
        """
        Check the Working with Selections
        (http://www.bohemiancoding.com/sketch/support/developer/02-common-tasks/02.html)
        section for some examples.
        """
        # Not implemented
        pass

    def absoluteRect(self):
        """
        Returns a GKRect object that returns the bounds of this layer in absolute coordinates;
        it takes into account the layer's rotation and that of any of its parents. (readonly)
        """
        # Not implemented
        pass

    def duplicate(self):
        """
        Duplicates the layer and insert the copy above itself.
        """
        # Not implemented
        pass

    def __repr__(self):
        return "<MSLayer \n\
                frame: {frame}, \n\
                style: {style}, \n\
                name: {name}, \n\
                rotation: {rotation}, \n\
                isVisible: {isVisible}, \n\
                isLocked: {isLocked}, \n\
                isFlippedHorizontal: {isFlippedHorizontal}, \n\
                isFlippedVertical: {isFlippedVertical}".format(
                    frame=self.frame, style=self.style, name=self.name, rotation=self.rotation,
                    isVisible=self.isVisible, isLocked=self.isLocked,
                    isFlippedHorizontal=self.isFlippedHorizontal, isFlippedVertical=self.isFlippedVertical)
