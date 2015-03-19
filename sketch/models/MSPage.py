from sketch.models import (MSLayerGroup, MSRulerData)


class MSPage(MSLayerGroup):
    """
    MSPage is a subclass of MSLayerGroup that represents a page of the document.
    The frame parameter of an MSPage is not useful as its not guaranteed to contain
    all layers on the page.

    However do check out MSLayerGroup as there are useful methods in there as well.
    """

    def __init__(self,
                 horizontalRulerData,  verticalRulerData,
                 layers,  # inherited from MSLayerGroup
                 frame, style, name, rotation,
                 isVisible, isLocked, isSelected,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(horizontalRulerData, MSRulerData)
        assert isinstance(verticalRulerData, MSRulerData)
        self._horizontalRulerData = horizontalRulerData
        self._verticalRulerData = verticalRulerData

        super(MSPage, self).__init__(layers,
                                     frame, style, name, rotation,
                                     isVisible, isLocked, isSelected,
                                     isFlippedHorizontal, isFlippedVertical)

    @property
    def contentBounds(self):
        """
        If you want a rectangle around everything on the canvas, use this. It returns a
        GKRect object that you can use to export from. See the Exporting section for examples.
        """
        pass

    @property
    def exportableLayers(self):
        """
        Returns an array of all exportable layers in the page
        """
        pass

    @property
    def artboards(self):
        """
        Returns a readonly array of all artboards on the page. If you want to add a
        new artboard to a page, use the addLayer method.
        """
        pass

    def addLayer(self, layer):
        """
        Adds an MSLayer to the page.
        """
        # Not implemented
        pass

    @property
    def slices(self):
        """
        Returns an array of all slices on the page, not including artboards.
        """
        pass

    @property
    def horizontalRulerData(self):
        """
        Returns the MSRulerData object used to store rulers for the horizontal axis.
        Note that this data is only used if there’s no artboard on the page
        (MSArtboardGroup has similar methods for itself).
        """
        return self._horizontalRulerData

    @property
    def verticalRulerData(self):
        """
        Returns the MSRulerData object used to store rulers for the vertical axis.
        Note that this data is only used if there’s no artboard on the page
        (MSArtboardGroup has similar methods for itself).
        """
        return self._verticalRulerData

    def __repr__(self):
        return "<MSPage \n\
                layers: {layers}\n\
                horizontalRulerData: {horizontalRulerData}\n\
                verticalRulerData: {verticalRulerData}".format(
                    layers=self.layers,
                    horizontalRulerData=self.horizontalRulerData,
                    verticalRulerData=self.verticalRulerData)
