"""Test item styles."""

import pytest

from gaphor.diagram.style import (
    get_text_point,
    get_text_point_at_line,
    get_text_point_at_line2,
    get_min_size,
    ALIGN_LEFT,
    ALIGN_CENTER,
    ALIGN_RIGHT,
    ALIGN_TOP,
    ALIGN_MIDDLE,
    ALIGN_BOTTOM,
)


def test_min_size():
    """Test minimum size calculation."""
    width, height = get_min_size(10, 10, (1, 2, 3, 4))
    assert width == 16
    assert height == 14


def test_align_box():
    """Test aligned text position calculation."""
    extents = 80, 12
    padding = (1, 2, 3, 4)
    data = {
        (ALIGN_LEFT, ALIGN_TOP, False): (4, 1),
        (ALIGN_LEFT, ALIGN_MIDDLE, False): (4, 14),
        (ALIGN_LEFT, ALIGN_BOTTOM, False): (4, 25),
        (ALIGN_CENTER, ALIGN_TOP, False): (42, 1),
        (ALIGN_CENTER, ALIGN_MIDDLE, False): (42, 14),
        (ALIGN_CENTER, ALIGN_BOTTOM, False): (42, 25),
        (ALIGN_RIGHT, ALIGN_TOP, False): (78, 1),
        (ALIGN_RIGHT, ALIGN_MIDDLE, False): (78, 14),
        (ALIGN_RIGHT, ALIGN_BOTTOM, False): (78, 25),
        (ALIGN_LEFT, ALIGN_TOP, True): (-84, -13),
        (ALIGN_LEFT, ALIGN_MIDDLE, True): (-84, 14),
        (ALIGN_LEFT, ALIGN_BOTTOM, True): (-84, 43),
        (ALIGN_CENTER, ALIGN_TOP, True): (40, -13),
        (ALIGN_CENTER, ALIGN_MIDDLE, True): (40, 14),
        (ALIGN_CENTER, ALIGN_BOTTOM, True): (40, 43),
        (ALIGN_RIGHT, ALIGN_TOP, True): (162, -13),
        (ALIGN_RIGHT, ALIGN_MIDDLE, True): (162, 14),
        (ALIGN_RIGHT, ALIGN_BOTTOM, True): (162, 43),
    }

    for halign in range(-1, 2):
        for valign in range(-1, 2):
            for outside in (True, False):
                align = (halign, valign)
                point_expected = data[(halign, valign, outside)]
                point = get_text_point(extents, 160, 40, align, padding, outside)

                assert point[0] == point_expected[0], "%s, %s -> %s" % (
                    align,
                    outside,
                    point[0],
                )
                assert point[1] == point_expected[1], "%s, %s -> %s" % (
                    align,
                    outside,
                    point[1],
                )


def test_align_line():
    """Test aligned at the line text position calculation."""
    p1 = 0, 0
    p2 = 20, 20

    extents = 10, 5

    x, y = get_text_point_at_line(
        extents, p1, p2, (ALIGN_LEFT, ALIGN_TOP), (2, 2, 2, 2)
    )
    assert x == 5
    assert y == (-10)

    x, y = get_text_point_at_line(
        extents, p1, p2, (ALIGN_RIGHT, ALIGN_TOP), (2, 2, 2, 2)
    )
    assert x == 5
    assert y == (-10)

    p2 = -20, 20
    x, y = get_text_point_at_line(
        extents, p1, p2, (ALIGN_LEFT, ALIGN_TOP), (2, 2, 2, 2)
    )
    assert x == (-15)
    assert y == (-10)

    x, y = get_text_point_at_line(
        extents, p1, p2, (ALIGN_RIGHT, ALIGN_TOP), (2, 2, 2, 2)
    )
    assert x == (-15)
    assert y == (-10)


def test_align_line2_h():
    """Test aligned at the line text position calculation, horizontal mode."""
    extents = 10, 5
    p1 = 2.0, 2.0

    # align top
    p2 = 22.0, 7.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7)
    assert y == pytest.approx(-4.75)

    p2 = 22.0, -3.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7)
    assert y == pytest.approx(-9.75)

    p2 = -18.0, 7.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13)
    assert y == pytest.approx(-4.75)

    p2 = -18.0, -3.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13)
    assert y == pytest.approx(-9.75)

    # align bottom
    p2 = 22.0, 7.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7)
    assert y == pytest.approx(8.75)

    p2 = 22.0, -3.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7)
    assert y == pytest.approx(3.75)

    p2 = -18.0, 7.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13)
    assert y == pytest.approx(8.75)

    p2 = -18.0, -3.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13)
    assert y == pytest.approx(3.75)


def test_align_line2_v():
    """Test aligned at the line text position calculation, vertical mode."""
    extents = 10, 5
    p1 = 2.0, 2.0

    # top align
    p2 = 7.0, 22.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7.125)
    assert y == pytest.approx(9.5)

    p2 = 7.0, -18.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-8.125)
    assert y == pytest.approx(-10.5)

    p2 = -3.0, 22.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13.125)
    assert y == pytest.approx(9.5)

    p2 = -3.0, -18.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(2.125)
    assert y == pytest.approx(-10.5)

    # bottom align
    p2 = 7.0, 22.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-8.125)
    assert y == pytest.approx(9.5)

    p2 = 7.0, -18.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7.125)
    assert y == pytest.approx(-10.5)

    p2 = -3.0, 22.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(2.125)
    assert y == pytest.approx(9.5)

    p2 = -3.0, -18.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13.125)
    assert y == pytest.approx(-10.5)


def test_align_line2_o():
    """Test aligned at the line text position calculation, orthogonal lines."""
    extents = 10, 5
    p1 = 2.0, 2.0

    # top align
    p2 = 22.0, 2.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7)
    assert y == pytest.approx(-6)

    p2 = -18.0, 2.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13)
    assert y == pytest.approx(-6)

    p2 = 2.0, 22.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-10.0)
    assert y == pytest.approx(9.5)

    p2 = 2.0, -18.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_TOP), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-10.0)
    assert y == pytest.approx(-10.5)

    # bottom align
    p2 = 22.0, 2.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(7)
    assert y == pytest.approx(5)

    p2 = -18.0, 2.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(-13.0)
    assert y == pytest.approx(5.0)

    p2 = 2.0, 22.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(4.0)
    assert y == pytest.approx(9.5)

    p2 = 2.0, -18.0
    x, y = get_text_point_at_line2(
        extents, p1, p2, (ALIGN_CENTER, ALIGN_BOTTOM), (3, 2, 3, 2)
    )
    assert x == pytest.approx(4.0)
    assert y == pytest.approx(-10.5)
