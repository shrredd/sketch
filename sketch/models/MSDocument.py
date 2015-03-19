class MSDocument(object):
    def setZoomValue(self, zoomLevel):
        """
        Zoom the document. 1.0 represents actual size, 2.0 means 200% etc.
        """
        # Not implemented
        pass

    def export(self):
        """
        Takes you to the the export tool. Pass nil as the argument.
        """
        pass

    def exportPDFBook(self):
        """
        A nice method not exposed in the UI at the moment; exports each slice on each page to a
        multi-page PDF file. Pass nil as the argument.
        """
        # Not implemented
        pass

    def showMessage(self, displayString):
        """
        Pass a string to be displayed at the top of the canvas momentarily. The same method used
        for displaying the current zoom level and other tips.
        """
        # Not implemented
        pass

    def artboards(self):
        """
        Both return an array representing the artboards and slices on the current page. Artboards
        are of type MSArtboardGroup and slices are of MSSliceLayer type.
        """
        pass

    def children(self):
        """
        Returns an array containing all layers (including slices and artboards) on the current page.
        """
        pass

    def pages(self):
        """
        Returns an array of all pages in the document. Each page is an MSPage object.
        """
        pass

    def askForUserInput(self, dialogLabel, initialValue):
        """
        Asks for user input and returns the value they chosen. The first argument is the label for
        the dialog panel, the second argument can be used to provide a default value. See the User
        Input & Feedback section for examples.
        (http://www.bohemiancoding.com/sketch/support/developer/02-common-tasks/05.html)
        """
        # Not implemented
        pass

    def saveArtboardOrSlice(self, exportItem, toFile):
        """
        Saves an area of the canvas to an image file. The first argument is a GKRect, MSSliceLayer
        or MSArtboardGroup and the image gets written to the file specified in the second argument.
        The file format is derived from the extension. See the Exporting section for examples.
        """
        pass

    def currentView(self):
        """
        Returns an MSContentDrawView subclass that represents the visible Canvas
        """
        # Not implemented
        pass

    def addBlankPage(self):
        """
        Adds a new MSPage object to the document, inserting it below the current page, copying its
        grid and ruler position too.
        """
        # Not implemented
        pass

    def removePage(self, page):
        """
        Removes the given page from the document. The argument is an MSPage object.
        """
        # Not implemented
        pass

    def allExportableLayers(self):
        """
        Returns an array of all exportable layers in the document
        """
        pass
