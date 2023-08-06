from ShapeCal import *


def test_shapecal_square():
    assert square.area(5) == 25
    assert square.perimeter(5) == 20


def test_shapecal_triangle():
    assert triangle.area(5, 5) == 12.5
    assert triangle.perimeter(5, 5, 5) == 15


def test_shapecal_circle():
    assert circle.area(5) == 78.53981633974483
    assert circle.perimeter(5) == 31.41592653589793


def test_shapecal_trapezoid():
    assert trapezoid.area(5, 5, 5) == 25.0
    assert trapezoid.perimeter(5, 5, 5, 5) == 20


def test_shapecal_cone():
    assert cone.volume(5, 5) == 130.89969389957471
    assert cone.surfaceArea(5, 5) == 189.611889793704


def test_shapecal_cube():
    assert cube.volume(5) == 125
    assert cube.surfaceArea(5) == 900


def test_shapecal_cylinder():
    assert cylinder.volume(5, 5) == 392.69908169872417
    assert cylinder.surfaceArea(5, 5) == 314.1592653589793


def test_shapecal_rectangularPrism():
    assert rectangularPrism.volume(5, 5, 5) == 125
    assert rectangularPrism.surfaceArea(5, 5, 5) == 150


def test_shapecal_pyramid():
    assert pyramid.volume(5, 5, 5) == 41.666666666666664
    assert pyramid.surfaceArea(5, 5, 5) == 80.90169943749474


def test_shapecal_sphere():
    assert sphere.volume(5) == 523.5987755982989
    assert sphere.surfaceArea(5) == 314.1592653589793


def test_shapecal_hemisphere():
    assert hemisphere.volume(5) == 261.79938779914943
    assert hemisphere.surfaceArea(5) == 235.61944901923448


def test_shapecal_frustrum():
    assert frustrum.volume(5, 5, 5) == 392.6990816987241
    assert frustrum.surfaceArea(5, 5, 5) == 314.1592653589793
