from PIL import ImageColor

PURPLE = 117, 112, 179
ORANGE = 217, 95, 2
GREEN = 27, 158, 119


def get_font_color(background_color):
    if not isinstance(background_color, tuple):
        background_color = ImageColor.getrgb(background_color)

    # calculate perceptive luminance
    r, g, b = background_color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # bright color -> black font
    if luminance > 0.5:
        return "black"

    # dark color -> white font
    else:
        return "white"

