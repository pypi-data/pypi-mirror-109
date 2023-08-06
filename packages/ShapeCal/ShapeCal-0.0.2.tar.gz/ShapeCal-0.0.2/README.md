# ShapeCal
[![License](https://img.shields.io/pypi/l/shapecal.svg)](https://github.com/The-Real-Thisas/ShapeCal/blob/main/LICENSE)
[![Version](https://img.shields.io/pypi/v/shapecal.svg)](https://pypi.org/project/ShapeCal/)
[![Python](https://img.shields.io/pypi/pyversions/ShapeCal.svg)](https://pypi.org/project/ShapeCal/)
[![Code Style](https://img.shields.io/badge/codestyle-black-black.svg)](https://github.com/ambv/black)
[![Build Status](https://dev.azure.com/Thisas/ShapeCal/_apis/build/status/The-Real-Thisas.ShapeCal?branchName=main)](https://dev.azure.com/Thisas/ShapeCal/_build/latest?definitionId=1&branchName=main)

A package for calculating the area/perimeter/volume of some geometric shapes.

---

## Installation

```bash
pip install ShapeCal
```

---

## Usage

- `square`
	- `square.area()` : Takes one float and returns area as a float.
	- `square.perimeter()` : Takes one float and returns perimeter as a float.
- `triangle`
	- `triangle.area()` : Takes two floats (base, height) and returns area as a float.
	- `triangle.perimeter()` : Takes three floats (sideA, sideB, sideC) and returns perimeter as a float.
- `circle`
	- `circle.area()` : Takes one float (radius) and returns area as a float.
	- `circle.perimeter()` : Takes one float (radius) and returns perimeter as a float.
- `trapezoid`
	- `trapezoid.area()` : Takes three floats (short_base, long_base, height) and returns area as a float.
	- `trapezoid.perimeter()` : Takes four floats (short_base, long_base, sideA, sideB) and returns perimeter as a float.
- `cone`
	- `cone.volume()` : Takes two floats (height, radius) and returns volume as a float.
	- `cone.surfaceArea()` : Takes two floats (height, radius) and returns surfaceArea as a float.
- `cube`
	- `cube.volume()` : Takes one float (one float) and returns volume as a float.
	- `cube.surfaceArea()` : Takes one float (one float) and returns surfaceArea as a float.
- `cylinder`
	- `cylinder.volume()` : Takes two floats (height, radius) and returns volume as a float.
	- `cylinder.surfaceArea()` : Takes two floats (height, radius) and returns surfaceArea as a float.
- `rectangularPrism`
	- `rectangularPrism.volume()` : Takes three floats (lenght, width, height) and returns volume as a float.
	- `rectangularPrism.surfaceArea()` : Takes three floats (lenght, width, height) and returns surfaceArea as a float.
- `pyramid`
	- `pyramid.volume()` : Takes three floats (lenght, width, height) and returns volume as a float.
	- `pyramid.surfaceArea()` : Takes three floats (lenght, width, height) and returns surfaceArea as a float.
- `sphere`
	- `sphere.volume()` : Takes one float (radius) and returns volume as a float.
	- `sphere.surfaceArea()` : Takes one float (radius) and returns surfaceArea as a float.
- `hemisphere`
	- `hemisphere.volume()` : Takes one float (radius) and returns volume as a float.
	- `hemisphere.surfaceArea()` : Takes one float (radius) and returns surfaceArea as a float.
- `frustrum`
	- `frustrum.volume()` : Takes three floats (radiusTop, radiusBottom, height) and returns volume as a float.
	- `frustrum.surfaceArea()` : Takes three floats (radiusTop, radiusBottom, height) and returns surfaceArea as a float.


---

## Update Log

- 0.0.2
	- Added Riposte framework and refactored code for ShapeCal.py
	- Added CLI support

- 0.0.1
	- Initial

