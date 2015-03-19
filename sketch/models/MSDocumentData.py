from sketch.models.MSObject import MSObject


class MSDocumentData(MSObject):
    """ Represents the data within a sketch document """

    def __init__(self,
                 images, pages,
                 currentPageIndex, enableSliceInteraction, enableLayerInteraction,
                 layerStyles, layerSymbols, layerTextStyles,
                 objectID):  # Inherited

        self._images = images
        self._pages = pages

        self._currentPageIndex = currentPageIndex
        self._enableSliceInteraction = enableSliceInteraction
        self._enableLayerInteraction = enableLayerInteraction

        self._layerStyles = layerStyles
        self._layerSymbols = layerSymbols
        self._layerTextStyles = layerTextStyles

        super(MSDocumentData, self).__init__(objectID)

    @property
    def images(self):
        """ <dict> """
        return self._images

    @property
    def pages(self):
        """ <dict> """
        return self._pages

    @property
    def currentPageIndex(self):
        """ <int> """
        return self._currentPageIndex

    @property
    def enableSliceInteraction(self):
        """ <bool> """
        return self._enableSliceInteraction

    @property
    def enableLayerInteraction(self):
        """ <bool> """
        return self._enableLayerInteraction

    @property
    def layerStyles(self):
        """ <dict> """
        return self._layerStyles

    @property
    def layerSymbols(self):
        """ <dict> """
        return self._layerSymbols

    @property
    def layerTextStyles(self):
        """ <dict> """
        return self._layerTextStyles

    def __repr__(self):
        return '<MSDocumentData \n\
                objectID: {objectID}\n\
                images: {images}\n\
                pages: {pages}\n\
                currentPageIndex: {currentPageIndex}\n\
                enableSliceInteraction: {enableSliceInteraction}\n\
                enableLayerInteraction: {enableLayerInteraction}\n\
                layerStyles: {layerStyles}\n\
                layerSymbols: {layerSymbols}\n\
                layerTextStyles: {layerTextStyles}>'.format(
                    objectID=self.objectID,
                    images=self.images,
                    pages=self.pages,
                    currentPageIndex=self.currentPageIndex,
                    enableSliceInteraction=self.enableSliceInteraction,
                    enableLayerInteraction=self.enableLayerInteraction,
                    layerStyles=self.layerStyles,
                    layerSymbols=self.layerSymbols,
                    layerTextStyles=self.layerTextStyles,
                )
