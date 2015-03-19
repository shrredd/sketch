from sketch.models import MSLayer


class MSLayerGroup(MSLayer):
    def __init__(self, layers,
                 frame, style, name, rotation,  # Everything from here on is inherited from MSLayer
                 isVisible, isLocked, isSelected,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(layers, list)
        self._layers = layers

        super(MSLayerGroup, self).__init(frame, style, name, rotation,
                                         isVisible, isLocked, isSelected,
                                         isFlippedHorizontal, isFlippedVertical)

    @property
    def layers(self):
        """
        Returns an array of all layers in the group - not including any of their children.
        In this way you can see that a document is basically a tree structure of layers & groups.
        """
        return self._layers

    @property
    def children(self):
        """
        Returns an array of all layers in the group, including those in any sub-groups that
        have click-through enabled. Basically this array contains all layers that are directly
        selectable from within this group.
        """
        pass

    def resizeRoot(self):
        """
        Resizes the group to fit around all of its sub-layers.
        """
        # Not implemented
        pass

    def addLayer(self, layer):
        """
        Add a layer to this group.
        """
        # Not implemented
        pass

    def removeLayer(self, layer):
        """
        Remove a layer from this group.
        """
        # Not implemented
        pass

    def addLayerOfType(self, type):
        """
        Adds a completely new layer to the group, at the group’s {0,0} origin.
        This method takes one argument; a string which indicates the kind of layer.
        Currently the only supported values are: "rectangle" and "text".

        This method returns the new layer which you can then manipulate/style using
        the other scripting methods.
        """
        # Not implemented
        pass

    def __repr__(self):
        return "<MSLayerGroup \n\
                layers: {layers}".format(layers=self.layers)
