from PIL import ImageFont, ImageDraw

from bbdraw.color import get_font_color
from bbdraw.polygon import Polygon


def write_text(draw: ImageDraw.ImageDraw, bounding_polygon: Polygon, text: str, background_color, font_size):
    image_width, image_height = draw.im.size

    font = ImageFont.truetype("Pillow/Tests/fonts/DejaVuSans/DejaVuSans.ttf", font_size)

    text_width, text_height = draw.textsize(text, font=font)
    text_offset_left, text_offset_top = font.getoffset(text)
    padding = text_offset_top

    box_top = bounding_polygon.top - text_height - 2 * padding
    if box_top < 0:
        box_top = bounding_polygon.bottom
    box_bottom = box_top + text_height + 2*padding

    box_right = bounding_polygon.left + text_width + 2*padding
    if box_right > image_width and not text_width > image_width:
        box_right = image_width
    box_left = box_right - text_width - 2*padding

    draw.rectangle([(box_left, box_top), (box_right, box_bottom)], fill=background_color)
    draw.text((box_left+padding, box_top + padding), text, font=font, fill=get_font_color(background_color))




