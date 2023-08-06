from typing import List, Union

from PIL import Image, ImageDraw

from bbdraw.color import PURPLE
from bbdraw.text import write_text
from bbdraw.polygon import parse_rectangle, parse_polygon, Polygon


def _get_line_width(image: Image.Image):
    min_side = min(image.width, image.height)

    if min_side < 200:
        return 2

    elif min_side < 400:
        return 3

    elif min_side < 800:
        return 4

    else:
        return 5


def _draw(image: Image.Image,
          polygon: Polygon,
          color: Union[str, tuple] = PURPLE,
          text: str = None,
          in_place=False):

    if not in_place:
        image = image.copy()

    line_width = _get_line_width(image)
    font_size = line_width * 8

    draw = ImageDraw.Draw(image)
    draw.line(polygon.vertices + polygon.vertices[0:1], fill=color, width=line_width)

    if text:
        write_text(draw, polygon, text, color, font_size)

    return image


def draw_polygon(image: Image.Image,
                 polygon: List,
                 color: Union[str, tuple] = PURPLE,
                 text: str = None,
                 in_place=False):
    """
    :param image:
    :param polygon: Sequence of either [(x0, y0), (x1, y1), (x2, y2)] or [x0, y0, x1, y1, x2, y2]
    :param color: Color of the polygon (also background color of the text, if any)
    :param text: Label or other text to place next to the polygon.
    :param in_place: If in_place=True, the image supplied to this function is manipulated. Otherwise a copy is used.
    :return:
    """
    polygon = parse_polygon(polygon)
    return _draw(image, polygon, color, text, in_place)


def draw_rectangle(image: Image.Image,
                   rectangle: List,
                   color: Union[str, tuple] = PURPLE,
                   text: str = None,
                   in_place: bool = False):
    """
    :param image:
    :param rectangle: Sequence of either [(x0, y0), (x1, y1)] or [x0, y0, x1, y1]
    :param color: Color of the rectangle (also background color of the text, if any)
    :param text: Label or other text to place next to the rectangle.
    :param in_place: If in_place=True, the image supplied to this function is manipulated. Otherwise a copy is used.
    :return:
    """

    polygon = parse_rectangle(rectangle)
    return _draw(image, polygon, color, text, in_place)







