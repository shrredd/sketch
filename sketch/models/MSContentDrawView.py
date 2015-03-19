class MSContentDrawView(object):
    @property
    def frame(self):
        """
        Returns a CGRect of the current view
        """
        pass

    def zoomIn(self):
        """
        Zooms in by 2x.
        """
        # Not implemented
        pass

    def zoomOut(self):
        """
        Zooms out by the 2x.
        """
        # Not implemented
        pass

    def actualSize(self):
        """
        Zooms back to 100%
        """
        # Not implemented
        pass

    def centerRect(self, nsRect):
        """
        Centers an arbitrary NSRect in the canvas.
        """
        # Not implemented
        pass

    def zoomToFitRect(self, gkRect):
        """
        Zooms the canvas in or out and scrolls to fit supplied
        GKRect argument in the view.
        """
        # Not implemented
        pass

    def refresh(self):
        """
        Refreshes the entire canvas, both the content and overlays
        """
        # Not implemented
        pass
