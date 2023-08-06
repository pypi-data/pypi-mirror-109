"""
Main module that define function to extract positions in svg file
"""
import reportlab.graphics.shapes as shp
from svglib.svglib import svg2rlg

from .transfo import Transfo


def extract_tick(lay, svg_descr):
    tr_lay = Transfo(lay.transform)
    tr = Transfo(svg_descr.transform)

    pos_gr, label_gr = svg_descr.contents
    if isinstance(pos_gr.contents[0], shp.String):
        label_gr, pos_gr = pos_gr, label_gr

    assert pos_gr.transform == (1, 0, 0, 1, 0, 0)

    label = label_gr.contents[0].text
    path = pos_gr.contents[0].points
    gx0, gy0 = tr_lay.to_global(*tr.to_global(path[0], path[1]))
    gx1, gy1 = tr_lay.to_global(*tr.to_global(path[2], path[3]))
    return (gx0, gy0, gx1, gy1), label


def extract_data(svg, x_formatter, y_formatter):
    """Extract data from well formed svg file

    Args:
        svg (str|Path): path to svg file
        x_formatter (Callable): function to format x data
        y_formatter (Callable): function to format y data

    Returns:
        (dict): key is layer label, values are records of points
    """
    # read raw svg
    d = svg2rlg(str(svg))

    doc, = d.contents
    layers = doc.contents

    # extract relevant layers
    lay_x_axis, = [lay for lay in layers if lay.label == 'x_axis']
    lay_y_axis, = [lay for lay in layers if lay.label == 'y_axis']
    data_lays = [lay for lay in layers if lay.label not in ('figure', 'x_axis', 'y_axis')]

    # find reference system of coordinates
    assert lay_y_axis.transform == lay_x_axis.transform

    ticks_descr = [extract_tick(lay_x_axis, gr) for gr in lay_x_axis.contents if len(gr.contents) == 2]

    x_ticks = sorted([(pth[0], x_formatter(label)) for pth, label in ticks_descr])

    ticks_descr = [extract_tick(lay_y_axis, gr) for gr in lay_y_axis.contents if len(gr.contents) == 2]

    y_ticks = sorted([(pth[1], y_formatter(label)) for pth, label in ticks_descr])

    # convert svg data descr into values
    data = {}

    for lay in data_lays:
        # assert lay.transform == lay_x_axis.transform
        tr = Transfo(lay.transform)

        records = []
        for marker in lay.contents:
            if isinstance(marker, shp.Circle):
                cx, cy = tr.to_global(marker.cx, marker.cy)
            elif isinstance(marker, shp.Rect):
                cx, cy = tr.to_global(marker.x + marker.width / 2, marker.y + marker.height / 2)
            elif isinstance(marker, shp.Group):  # Path
                points = marker.contents[0].points
                nb = len(points) // 2
                cx, cy = tr.to_global(sum(points[::2]) / nb, sum(points[1::2]) / nb)
            else:
                raise NotImplementedError

            x_rel_pos = (cx - x_ticks[0][0]) / (x_ticks[-1][0] - x_ticks[0][0])
            x = x_ticks[0][1] + (x_ticks[-1][1] - x_ticks[0][1]) * x_rel_pos

            y_rel_pos = (cy - y_ticks[0][0]) / (y_ticks[-1][0] - y_ticks[0][0])
            y = y_ticks[0][1] + (y_ticks[-1][1] - y_ticks[0][1]) * y_rel_pos

            records.append((x, y))

        data[lay.label] = records

    return data
