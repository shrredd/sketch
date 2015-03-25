from copy import (copy, deepcopy)

import cairocffi as cairo
import numpy as np

from sketch.drawing.geometry import (
    rotation_matrix,
    scaling_matrix,
    translation_matrix
)
from sketch.drawing.surfaces import Surface


class Element:
    """
    Base class for objects that can be transformed (rotated, translated, scaled)
    and drawn to a Surface.

    Parameter `draw_method` is a function which takes a cairo.Surface.Context()
    as argument and draws on this context. All Elements are draw on a different
    context.
    """

    def __init__(self, draw_method):
        self.draw_method = draw_method
        self.matrix = 1.0 * np.eye(3)

    def _cairo_matrix(self):
        """ returns the element's matrix in cairo form """
        m = self.matrix
        return cairo.Matrix(m[0, 0], m[1, 0],
                            m[0, 1], m[1, 1],
                            m[0, 2], m[1, 2])

    def _transform_ctx(self, ctx):
        """ Tranform the context before drawing.
        It applies all the rotation, translation, etc. to the context.
        In short, it sets the context's matrix to the element's matrix.
        """
        ctx.set_matrix(self._cairo_matrix())

    def draw(self, surface):
        """ Draws the Element on a new context of the given Surface """
        ctx = surface.get_new_context()
        self._transform_ctx(ctx)
        self.draw_method(ctx)

    def set_matrix(self, new_mat):
        """ Returns a copy of the element, with a new transformation matrix """
        new = deepcopy(self)
        new.matrix = new_mat
        return new

    def rotate(self, angle, center=[0, 0]):
        """ Rotate the element.

        Returns a new element obtained by rotating the current element
        by the given `angle` (unit: rad) around the `center`.
        """

        center = np.array(center)
        mat = (translation_matrix(center)
               .dot(rotation_matrix(angle))
               .dot(translation_matrix(-center)))

        return self.set_matrix(mat.dot(self.matrix))

    def translate(self, xy):
        """ Translate the element.

        Returns a new element obtained by translating the current element
        by a vector xy
        """
        return self.set_matrix(translation_matrix(xy).dot(self.matrix))

    def scale(self, rx, ry=None, center=[0, 0]):
        """ Scale the element.

        Returns a new element obtained by scaling the current element
        by a factor rx horizontally and ry vertically, with fix point `center`.
        If ry is not provided it is assumed that rx=ry.
        """

        ry = rx if (ry is None) else ry
        center = np.array(center)
        mat = (translation_matrix(center)
               .dot(scaling_matrix(rx, ry))
               .dot(translation_matrix(-center)))
        return self.set_matrix(mat.dot(self.matrix))


class Group(Element):
    """
    Class for special Elements made out of a group of other elements which
    will be translated, scaled, rotated, and drawn together.
    These elements can be base elements (circles, squares) or even groups.
    """

    def __init__(self, elements):
        self.elements = elements
        self.matrix = 1.0*np.eye(3)

    def draw(self, surface):
        """ Draws the group to a new context of the given Surface """

        for e in self.elements:
            m = self.matrix
            mi = np.linalg.inv(m)
            new_matrix = m.dot(e.matrix)
            e.set_matrix(new_matrix).draw(surface)


class ImagePattern(Element):
    """ Class for images that will be used to fill an element or its contour.

    image
      A numpy RGB(A) image.
    pixel_zero
      The coordinates of the pixel of the image that will serve as 0,0 origin
      when filling the element.

    filter
      Determines the method with which the images are resized:
        "best": slow but good quality
        "nearest": takes nearest pixel (can create artifacts)
        "good": Good and faster than "best"
        "bilinear": use linear interpolation
        "fast":fast filter, quality like 'nearest'

    extend
      Determines what happends outside the boundaries of the picture:
      "none", "repeat", "reflect", "pad" (pad= use pixel closest from source)

    """

    def __init__(self, image, pixel_zero=[0, 0], filter="best", extend="none"):
        if isinstance(image, Surface):
            self._cairo_surface = image
        else:
            self._cairo_surface = Surface.from_image(image)._cairo_surface
        self.matrix = translation_matrix(pixel_zero)
        self.filter = filter
        self.extend = extend

    def set_matrix(self, new_mat):
        """ Returns a copy of the element, with a new transformation matrix """
        new = copy(self)
        new.matrix = new_mat
        return new

    def make_cairo_pattern(self):
        pat = cairo.SurfacePattern(self._cairo_surface)
        pat.set_filter({"best": cairo.FILTER_BEST,
                        "nearest": cairo.FILTER_NEAREST,
                        "gaussian": cairo.FILTER_GAUSSIAN,
                        "good": cairo.FILTER_GOOD,
                        "bilinear": cairo.FILTER_BILINEAR,
                        "fast": cairo.FILTER_FAST}[self.filter])

        pat.set_extend({"none": cairo.EXTEND_NONE,
                        "repeat": cairo.EXTEND_REPEAT,
                        "reflect": cairo.EXTEND_REFLECT,
                        "pad": cairo.EXTEND_PAD}[self.extend])

        pat.set_matrix(self._cairo_matrix())

        return pat


for meth in ["scale", "rotate", "translate", "_cairo_matrix"]:
    exec("ImagePattern.%s = Element.%s" % (meth, meth))
