import math

class square:
  def area(side: float):
    square_area = side ** 2
    return square_area
  def perimeter(side: float):
    square_peri = side * 4
    return square_peri

class triangle:
  def area(base: float, height: float):
    triangle_area = (base * height) / 2
    return triangle_area
  def perimeter(sideA: float, sideB: float, sideC: float):
    triangle_peri = sideA + sideB + sideC
    return triangle_peri

class circle:
  def area(radius: float):
    circle_area = math.pi * radius ** 2
    return circle_area
  def perimeter(radius: float):
    circle_peri = 2 * math.pi * radius
    return circle_peri

class trapezoid:
  def area(short_base: float, long_base: float, height: float):
    trapezoid_area = ((short_base + long_base) / 2 ) * height
    return trapezoid_area
  def perimeter(short_base: float, long_base: float, sideA: float, sideB: float):
    trapezoid_peri = short_base + long_base + sideA + sideB
    return trapezoid_peri

class cone:
  def volume(height: float, radius: float):
    volume = (1.0/3) * math.pi * radius * radius * height
    return volume
  def surfaceArea(height: float, radius: float):
    length = math.sqrt((radius * radius) + (height * height))
    surface_area = math.pi * radius * (radius + length)
    return surface_area

class cube:
  def volume(length: float):
    volume = (length ** 3)
    return volume
  def surfaceArea(length: float):
    surface_area = ((6 * length) ** 2)
    return surface_area

class cylinder:
  def volume(height: float, radius: float):
    volume = (math.pi * (radius ** 2) * height)
    return volume
  def surfaceArea(height: float, radius: float):
    surface_area = (2 * math.pi * radius * height) + (2 * math.pi * (radius ** 2))
    return surface_area

class rectangularPrism:
  def volume(lenght: float, width: float, height: float):
    volume = (lenght * width * height)
    return volume
  def surfaceArea(lenght: float, width: float, height: float):
    surface_area = (2 * lenght * width) + (2 * (lenght + width) * height)
    return surface_area

class pyramid:
  def volume(lenght: float, width: float, height: float):
    volume = (lenght * width * height) / 3
    return volume
  def surfaceArea(lenght: float, width: float, height: float):
    surface_area = (lenght * width) + (lenght * math.sqrt((width/2)**2 + height**2)) + (width * math.sqrt((lenght/2)**2 + height**2))
    return surface_area

class sphere:
  def volume(radius: float):
    volume = (4 * math.pi * radius**3) / 3
    return volume
  def surfaceArea(radius: float):
    surface_area = (4 * math.pi * radius**2)
    return surface_area

class hemisphere:
  def volume(radius: float):
    volume = (2 * math.pi * radius**3) / 3
    return volume
  def surfaceArea(radius: float):
    surface_area = (3 * math.pi * radius**2)
    return surface_area

class frustrum:
  def volume(radiusTop: float, radiusBottom: float, height: float):
    volume = (math.pi/ 3) * height * (radiusBottom**2 + radiusTop**2 + radiusBottom * radiusTop)
    return volume
  def surfaceArea(radiusTop: float, radiusBottom: float, height: float):
    root_this = (radiusBottom-radiusTop)**2 + height**2
    surface_area = (math.pi * (radiusBottom + radiusTop) * math.sqrt(root_this) + math.pi*(radiusBottom**2) + math.pi*(radiusTop**2))
    return surface_area

def main():
  print("ShapeCal is a collection of functions.")

if __name__ == '__main__':
  main()