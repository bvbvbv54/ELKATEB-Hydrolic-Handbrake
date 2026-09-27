"""P1-012/P1-013 removable Pro Micro enclosure and cover."""

from common import box_at, cylinder_axis
from parameters import v


ORIGIN = (128.0, 45.0, 10.0)


def enclosure():
    x, y, z = ORIGIN
    lx, ly, lz = v("electronics_outer")
    wall = v("electronics_wall")
    outer = box_at(x, y, z, lx, ly, lz)
    inner = box_at(x + wall, y + wall, z + wall, lx - 2 * wall, ly - 2 * wall, lz - wall + 0.1)
    body = outer.cut(inner)
    # USB opening at rear (+X), Hall/JST route toward the pivot (-X).
    body = body.cut(box_at(x + lx - wall - 0.1, y + 8, z + 7, wall + 0.2, 14, 10))
    body = body.cut(cylinder_axis((x - 0.1, y + ly - 9, z + 9), 3.0, wall + 0.2, (1, 0, 0)))
    # Base through-bolts and cover heat-set insert pilot holes.
    for hx in (136.0, 170.0):
        for hy in (51.0, 78.0):
            body = body.cut(cylinder_axis((hx, hy, z - 0.1), 2.25, 4.0))
    for hx, hy in ((132, 49), (174, 49), (132, 79), (174, 79)):
        body = body.cut(cylinder_axis((hx, hy, z + lz - 5), 1.9, 5.1))
    return body


def cover():
    x, y, z = ORIGIN
    lx, ly, lz = v("electronics_outer")
    cover = box_at(x, y, z + lz, lx, ly, 3.0)
    # Shallow locating lip; it sits inside the enclosure wall.
    cover = cover.union(box_at(x + 2.7, y + 2.7, z + lz - 2.0, lx - 5.4, ly - 5.4, 2.0))
    for hx, hy in ((132, 49), (174, 49), (132, 79), (174, 79)):
        cover = cover.cut(cylinder_axis((hx, hy, z + lz - 2.1), 2.1, 5.2))
    return cover


def pro_micro_placeholder():
    x, y, z = ORIGIN
    bx, by, bz = v("pro_micro_envelope")
    return box_at(x + 5, y + 8, z + 4, bx, by, bz)


def parts():
    return {
        "P1-012_ELECTRONICS_ENCLOSURE": enclosure(),
        "P1-013_ELECTRONICS_COVER": cover(),
    }
