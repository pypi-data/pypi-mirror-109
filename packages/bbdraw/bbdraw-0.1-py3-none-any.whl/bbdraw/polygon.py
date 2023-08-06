class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices

        xs, ys = zip(*vertices)
        self.left = min(xs)
        self.right = max(xs)
        self.top = min(ys)
        self.bottom = max(ys)


def parse_rectangle(corner_points):
    # list of tuples [(x0, y0), (x1, y1)]
    if len(corner_points) == 2:
        if len(corner_points[0]) != 2 or len(corner_points[1]) != 2:
            raise ValueError("Rectangle must either be [x0, y0, x1, y1] or [(x0, y0), (x1, y1)]")

        (x0, y0), (x1, y1) = corner_points

    # flat list of [x0, y0, x1, y1]
    elif len(corner_points) == 4:
        x0, y0, x1, y1 = corner_points

    else:
        raise ValueError("Rectangle must either be [x0, y0, x1, y1] or [(x0, y0), (x1, y1)]")

    # int always rounds down - prefer that so that not drawing too far to the right/bottom side
    vertex0 = int(x0), int(y0)
    vertex1 = int(x1), int(y0)
    vertex2 = int(x1), int(y1)
    vertex3 = int(x0), int(y1)

    return Polygon([vertex0, vertex1, vertex2, vertex3])


def parse_polygon(vertices):
    if len(vertices) == 0:
        raise ValueError("List of vertices must have at least one entry")

    # easiest way to check if entry is a number is by just treating it like a number
    try:
        [int(entry) for entry in vertices]
        all_entries_are_numbers = True
    except TypeError:
        all_entries_are_numbers = False

    # flat list of  [x0, y0, x1, y1, ...]
    if all_entries_are_numbers:
        if len(vertices) % 2 != 0:
            raise ValueError("Flat list of vertices must contain even number of entries (since using xy coordinates)")

        num_vertices = int(len(vertices) / 2)
        xs = [vertices[2*i] for i in range(num_vertices)]      # even entries in the flat list are the xs
        ys = [vertices[2*i + 1] for i in range(num_vertices)]  # odd entries in the flat list are the ys

    # list of tuples of [(x0, y0), (x1, y1), ...] (or 2D array)
    elif all([len(entry) == 2 for entry in vertices]):
        xs = [x for x, y in vertices]
        ys = [y for x, y in vertices]

    else:
        raise ValueError("Vertices must either be flat list of [x0, y0, x1, y1, ...] "
                         "or list of tuples of [(x0, y0), (x1, y1), ...]")

    # int always rounds down - prefer that so that not drawing too far to the right/bottom side
    vertices = [(int(x), int(y)) for x, y in zip(xs, ys)]

    return Polygon(vertices)