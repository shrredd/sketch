from sketch.models import MSLayer


class MSTextLayer(MSLayer):
    """
    Represents text. Only the most basic of properties have yet been exposed.
    """

    @property
    def fontSize(self):
        pass

    @property
    def fontPostscriptName(self):
        pass

    @property
    def textColor(self):
        pass

    @property
    def textAlignment(self):
        pass

    @property
    def characterSpacing(self):
        pass

    @property
    def lineSpacing(self):
        pass
