from sketch.models import MSLayer


class MSSliceLayer(MSLayer):
    """
    Subclass of MSLayer representing a slice in the document.
    Although it may have a style attribute, this is never used.

    MSSliceLayer has —like MSLayer— a frame property that is an
    MSRect which determines its position in the canvas or inside its artboard.
    """
    pass
