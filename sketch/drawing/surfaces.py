from base64 import b64encode
import numpy as np
import cairocffi as cairo


class Surface:
    """
    A Surface is an object on which Elements are drawn, and which can be
    exported as PNG images, numpy arrays, or be displayed into an IPython Notebook.

    Note that this class is simply a thin wrapper around Cairo's Surface class.
    """

    def __init__(self, width, height, bg_color=None):
        self.width = width
        self.height = height
        self._cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                                 width, height)

        from sketch.drawing.shapes import rectangle
        if bg_color:
            rectangle(2*width, 2*height, fill=bg_color).draw(self)

    @staticmethod
    def from_image(image):
        h, w, d = image.shape
        if d == 4:
            image = image[:, :, [2, 1, 0, 3]]
        if d == 1:
            image = np.array(3*[image])
        elif d == 3:
            image = image[:, :, [2, 1, 0]]
            image = np.dstack([image, 255*np.ones((h, w))])
        sf = Surface(w, h)
        arr = np.frombuffer(sf._cairo_surface.get_data(), np.uint8)
        arr += image.flatten()
        sf._cairo_surface.mark_dirty()
        return sf

    def get_new_context(self):
        """ Returns a new context for drawing on the surface."""
        return cairo.Context(self._cairo_surface)

    def write_to_png(self, filename, y_origin="top"):
        """ Writes the image to a PNG.

        Parameter y_origin ("top" or "bottom") decides whether point (0,0) lies in
        the top-left or bottom-left corner of the screen.
        """
        from sketch.drawing.shapes import rectangle
        from sketch.drawing.elements import ImagePattern

        if y_origin == "bottom":
            W, H = self.width, self.height
            new_surface = Surface(W, H)
            rect = (rectangle(2*W, 2*H, fill=ImagePattern(self))
                    .scale(1, -1).translate([0, H]))
            rect.draw(new_surface)
            new_surface.write_to_png(filename, y_origin="top")
        else:
            self._cairo_surface.write_to_png(filename)

    def get_npimage(self, transparent=False, y_origin="top"):
        """ Returns a WxHx[3-4] numpy array representing the RGB picture.

        If `transparent` is True the image is WxHx4 and represents a RGBA picture,
        i.e. array[i,j] is the [r,g,b,a] value of the pixel at position [i,j].
        If `transparent` is false, a RGB array is returned.

        Parameter y_origin ("top" or "bottom") decides whether point (0,0) lies in
        the top-left or bottom-left corner of the screen.
        """

        im = 0+np.frombuffer(self._cairo_surface.get_data(), np.uint8)
        im.shape = (self.height, self.width, 4)
        im = im[:, :, [2, 1, 0, 3]]  # put RGB back in order
        if y_origin == "bottom":
            im = im[::-1]
        return im if transparent else im[:, :, :3]

    def get_html_embed_code(self, y_origin="top"):
        """ Returns an html code containing all the PNG data of the surface. """
        self.write_to_png("__temp__.png", y_origin=y_origin)
        with open("__temp__.png", "rb") as f:
            data = b64encode(f.read())
        return "<img  src='data:image/png;base64,%s'>" % (data)

    def ipython_display(self, y_origin="top"):
        """ displays the surface in the IPython notebook.

        Will only work if surface.ipython_display() is written at the end of one
        of the notebook's cells.
        """

        from IPython.display import HTML
        return HTML(self.get_html_embed_code(y_origin=y_origin))
