from sketch.models.MSLayer import MSLayer


class MSTextLayer(MSLayer):
    """
    Represents text. Only the most basic of properties have yet been exposed.
    """
    def __init__(self, text,
                 usesNewLineSpacingBehaviour, textBehaviour,
                 heightIsClipped, automaticallyDrawOnUnderlyingPath,
                 frame, style, name, rotation,
                 isVisible, isLocked,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(text, basestring)
        self.text = text

        assert isinstance(usesNewLineSpacingBehaviour, bool)
        self.usesNewLineSpacingBehaviour = usesNewLineSpacingBehaviour

        assert isinstance(textBehaviour, int)
        self.textBehaviour = textBehaviour

        assert isinstance(heightIsClipped, bool)
        self.heightIsClipped = heightIsClipped

        assert isinstance(automaticallyDrawOnUnderlyingPath, bool)
        self.automaticallyDrawOnUnderlyingPath = automaticallyDrawOnUnderlyingPath

        super(MSTextLayer, self).__init__(frame, style, name, rotation,
                                          isVisible, isLocked,
                                          isFlippedHorizontal, isFlippedVertical)

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
