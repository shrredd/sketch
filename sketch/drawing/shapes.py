import cairocffi as cairo
import numpy as np

from math import sqrt
from itertools import chain

from sketch.drawing.elements import (Element, ImagePattern)
from sketch.drawing.geometry import polar2cart
from sketch.drawing.gradients import ColorGradient


def _set_source(ctx, src):
    """ Sets a source before drawing an element.

    The source is what fills an element (or the element's contour).
    If can be of many forms. See the documentation of shape_element for more
    details.

    """
    if isinstance(src, ColorGradient):
        src.set_source(ctx)
    elif isinstance(src, ImagePattern):
        ctx.set_source(src.make_cairo_pattern())
    elif isinstance(src, np.ndarray) and len(src.shape) > 1:
        string = src.to_string()
        surface = cairo.ImageSurface.create_for_data(string)
        _set_source(ctx, surface)
    elif len(src) == 4:  # RGBA
        ctx.set_source_rgba(*src)
    else:  # RGB
        ctx.set_source_rgb(*src)


def shape_element(draw_contour, xy=(0, 0), angle=0, fill=None,
                  stroke=(0, 0, 0), stroke_width=0,
                  line_cap=None, line_join=None):
    """

    Parameters
    ------------

    xy
      vector [x,y] indicating where the Element should be inserted in the drawing.
      Note that for shapes like circle, square, rectangle, regular_polygon, the
      [x,y] indicates the *center* of the element. So these elements are centered
      around 0 by default.

    angle
      Angle by which to rotate the shape. The rotation uses (0,0) as center point.
      Therefore all circles, rectangles, squares, and regular_polygons are rotated
      around their center.

    fill
      Defines wath will fill the element. Default is None (no fill). `fill` can
      be one of the following:
      - A (r,g,b) color tuple, where 0 =< r,g,b =< 1
      - A (r,g,b, a) color tuple, where 0=< r,g,b,a =< 1 (a defines the transparency:
        0 is transparent, 1 is opaque)
      - A sketch.gradients.ColorGradient object.
      - A sketch.surfaces.Surface
      - A numpy image (not implemented yet)

    stroke
      Decides how the stroke (contour) of the element will be filled.
      Same rules as for argument ``fill``. Default is color black

    stroke_width
      Width of the stroke, in pixels. Default is 0 (no apparent stroke)

    line_cap
      The shape of the ends of the stroke: 'butt' or 'round' or 'square'

    line_join
      The shape of the 'elbows' of the contour: 'square', 'cut' or 'round'

    """

    def new_draw(ctx):
        draw_contour(ctx)
        if fill is not None:
            ctx.move_to(*xy)
            _set_source(ctx, fill)
            ctx.fill_preserve()
        if stroke_width > 0:
            ctx.move_to(*xy)
            ctx.set_line_width(stroke_width)
            if line_cap is not None:
                ctx.set_line_cap({"butt":  cairo.LINE_CAP_BUTT,
                                  "round": cairo.LINE_CAP_ROUND,
                                  "square": cairo.LINE_CAP_SQUARE}[line_cap])
            if line_join is not None:
                ctx.set_line_join({"cut":  cairo.LINE_JOIN_BEVEL,
                                   "square": cairo.LINE_JOIN_MITER,
                                   "round": cairo.LINE_JOIN_ROUND}[line_join])
            _set_source(ctx, stroke)
            ctx.stroke_preserve()

    return Element(new_draw).rotate(angle).translate(xy)


def rectangle(lx, ly, **kw):
    return shape_element(lambda c: c.rectangle(-lx/2, -ly/2, lx, ly), **kw)


def square(l, **kw):
    return rectangle(l, l, **kw)


def arc(r, a1, a2, **kw):
    return shape_element(lambda c: c.arc(0, 0, r, a1, a2), **kw)


def circle(r, **kw):
    return arc(r, 0, 2*np.pi, **kw)


def polyline(points, close_path=False, **kw):
    def draw(ctx):
        ctx.move_to(*points[0])
        for p in points[1:]:
            ctx.line_to(*p)
        if close_path:
            ctx.close_path()
    return shape_element(draw, **kw)


def regular_polygon(r, n, **kw):
    points = [polar2cart(r, a) for a in np.linspace(0, 2*np.pi, n+1)[:-1]]
    return polyline(points, close_path=True, **kw)


def bezier_curve(points, **kw):
    """Create cubic Bezier curve

    points
      List of four (x,y) tuples specifying the points of the curve.
    """
    def draw(ctx):
        ctx.move_to(*points[0])
        ctx.curve_to(*tuple(chain(*points))[2:])
    return shape_element(draw, **kw)


def ellipse(w, h, **kw):
    """Create an ellipse.

    w, h
      These are used to set the control points for the first quarter
      of the ellipse.
    """

    # Bezier control points for a quarter of an ellipse.
    ctrl_pnts = [((w/2), 0), ((w/2), (h/2)*(4/3)*(sqrt(2)-1)),
                 ((w/2)*(4/3)*(sqrt(2)-1), (h/2)), (0, (h/2))]

    # Create a list, all_points, which will be populated with lists of control
    # points for 4 Bezier curves that will approximate the ellipse.
    all_points = []
    for i in [1, -1]:
        for j in [1, -1]:
            all_points.append([(pnt[0]*i, pnt[1]*(-j)) for pnt in ctrl_pnts])
    # Permutes the last three lists to put the curves in correct order
    all_points.append(all_points.pop(1))
    # Correct the order of the two sublists defining their respective quarter
    # pieces of the ellipse so that the whole ellipse is drawn in order
    all_points[1].reverse()
    all_points[3].reverse()

    def draw(ctx):
        ctx.move_to(*ctrl_pnts[0])
        for points in all_points:
            ctx.curve_to(*tuple(chain(*points))[2:])
        ctx.close_path()

    return shape_element(draw, **kw)


def star(nbranches=5, radius=1.0, ratio=0.5, **kwargs):
    """ This function draws a star with the given number of branches,
    radius, and ratio between branches and body. It accepts the usual
    parameters xy, angle, fill, etc. """

    rr = radius*np.array(nbranches*[1.0, ratio])
    aa = np.linspace(0, 2*np.pi, 2*nbranches+1)[:-1]
    points = polar2cart(rr, aa)
    return polyline(points, close_path=True, **kwargs)


def text(txt, fontfamily, fontsize, fill=(0, 0, 0),
         h_align="center", v_align="center",
         stroke=(0, 0, 0), stroke_width=0,
         fontweight="normal", fontslant="normal",
         angle=0, xy=[0, 0], y_origin="top"):
    """

    Parameters
    -----------

    v_align
      vertical alignment of the text: "top", "center", "bottom"

    h_align
      horizontal alignment of the text: "left", "center", "right"

    fontweight
      "normal" "bold"

    fontslant
      "normal" "oblique" "italic"

    y_origin
      Adapts the vertical orientation of the text to the coordinates system:
      if you are going to export the image with y_origin="bottom" (see for
      instance Surface.write_to_png) then set y_origin to "bottom" here too.

    angle, xy, stroke, stroke_width
      see the doc for ``shape_element``
    """

    fontweight = {"normal": cairo.FONT_WEIGHT_NORMAL,
                  "bold":   cairo.FONT_WEIGHT_BOLD}[fontweight]
    fontslant = {"normal":  cairo.FONT_SLANT_NORMAL,
                 "oblique": cairo.FONT_SLANT_OBLIQUE,
                 "italic":  cairo.FONT_SLANT_ITALIC}[fontslant]

    def draw(ctx):

        ctx.select_font_face(fontfamily, fontslant, fontweight)
        ctx.set_font_size(fontsize)
        xbear, ybear, w, h, xadvance, yadvance = ctx.text_extents(txt)
        xshift = {"left": 0, "center": -w/2, "right": -w}[h_align] - xbear
        yshift = {"bottom": 0, "center": -h/2, "top": -h}[v_align] - ybear
        new_xy = np.array(xy) + np.array([xshift, yshift])
        ctx.move_to(*new_xy)
        ctx.text_path(txt)
        _set_source(ctx, fill)
        ctx.fill()
        if stroke_width > 0:
            ctx.move_to(*new_xy)
            ctx.text_path(txt)
            _set_source(ctx, stroke)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

    return (Element(draw).scale(1, 1 if (y_origin == "top") else -1)
            .rotate(angle))
