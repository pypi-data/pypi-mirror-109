# bbdraw 

### Library for drawing labeled bounding boxes / bounding polygons

![Example image showing labeled bounding boxes and bounding polygons](https://raw.githubusercontent.com/krasch/bbdraw/master/example.jpg "Example containing bounding boxes and bounding polygons")

Basically, a small wrapper around the python pillow library that combines drawing
boxes and writing labels into one simple function call:

```
corners = [(650, 290), (715, 335)]
image = bbdraw.rectangle(image, corners, text="cactus", color="red")
```

# Installation

Needs python >= 3.5

`pip3 install bbdraw`

# Usage

```
from PIL import Image

import bbdraw

image = Image.open("example.jpg")

# box/rectangle is given by two corners
# either as list of tuples [(x0, y0), (x1, y1)] or flat list [x0, y0, x1, y1]
corners = [(650, 290), (715, 335)]
image = bbdraw.rectangle(image, corners, text="cactus", color="red")

# polygon is given by list of vertices
# either as list of tuples [(x0, y0), (x1, y1), (x2, y2), ...] 
# or as flat list [x0, y0, x1, y1, x2, y2, ...]
vertices = [(440, 360), (400, 265), (525, 195), (590, 280), (520, 360)]
image = bbdraw.polygon(image, vertices, text="shrub", color="green")

# use in_place=True to directly draw on the input image, instead of making a copy
corners = [(1080, 350), (1180, 285)]
bbdraw.rectangle(image, corners, text="cactus", color="red", in_place=True)

image.save("example_out.jpg")
```