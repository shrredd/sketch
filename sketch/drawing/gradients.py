import cairocffi as cairo


class ColorGradient:
    """ This class is more like a structure to store the data for color gradients

    These gradients are used as sources for filling elements or their borders (see
    parameters `fill` and `stroke` in `shape_elements`).

    Parameters
    ------------
    type
      Type of gradient: "linear" or "radial"

    xy1, xy2, xy3

    stops_colors
      For instance, if you want a blue color then a red color then a green color
      you will write stops_colors=[(0,(1,0,0)), (0.5,(0,1,0)) , (1,(0,0,1))].

    """

    def __init__(self, type, stops_colors, xy1, xy2, xy3=None):
        self.xy1 = xy1
        self.xy2 = xy2
        self.xy3 = xy3
        self.stops_colors = stops_colors
        if type not in ["radial", "linear"]:
            raise ValueError("unkown gradient type")
        self.type = type

    def set_source(self, ctx):

        if self.type == "linear":
            (x1, y1), (x2, y2) = self.xy1, self.xy2
            pat = cairo.LinearGradient(x1, y1, x2, y2)
        elif self.type == "radial":
            (x1, y1), (x2, y2), (x3, y3) = self.xy1, self.xy2, self.xy3
            pat = cairo.RadialGradient(x1, y1, x2, y2, x3, y3)
        for stop, color in self.stops_colors:
            if len(color) == 4:
                pat.add_color_stop_rgba(stop, *color)
            else:
                pat.add_color_stop_rgb(stop, *color)
        ctx.set_source(pat)
