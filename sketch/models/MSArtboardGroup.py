from sketch.models import (
    MSLayerGroup,
    MSRulerData,
)


class MSArtboardGroup(MSLayerGroup):

    @property
    def frame(self):
        """
        An MSRect which determines its position in the canvas.
        """
        pass

    @property
    def layers(self):
        """
        To see which layers are inside the Artboard, use the layers property.
        """
        pass

    @property
    def horizontalRulerData(self):
        """
        Returns the MSRulerData object used to store rulers for the horizontal
        axis. Note that this data is only used on the artboard itself.
        """
        pass

    @property
    def verticalRulerData(self):
        """
        Returns the MSRulerData object used to store rulers for the vertical
        axis. Note that this data is only used on the artboard itself.
        """
        pass
