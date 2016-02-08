from sketch.models.MSLayer import MSLayer


class MSLayerGroup(MSLayer):
    def __init__(self, layers,
                 frame, style, name, rotation,
                 isVisible, isLocked,
                 isFlippedHorizontal, isFlippedVertical):

        assert isinstance(layers, list)
        self._layers = layers

        super(MSLayerGroup, self).__init__(frame, style, name, rotation,
                                           isVisible, isLocked,
                                           isFlippedHorizontal, isFlippedVertical)

    def to_cairo(self):
        from sketch.drawing.elements import Group
        element_list = []
        for layer in self.layers:
            element_list.append(layer.to_cairo())
        return Group(element_list)

    def render(self):
        from sketch.drawing.surfaces import Surface

        surface = Surface(int(self.frame.width), int(self.frame.height))
        context = surface.get_new_context()

        for layer in self.layers:
            layer_surface = layer.render()
            context.set_source_surface(layer_surface._cairo_surface,
                                       layer.frame.x, layer.frame.y)
            context.paint()

        return surface

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
        Adds a completely new layer to the group, at the group's {0,0} origin.
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
