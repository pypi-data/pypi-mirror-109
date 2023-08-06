from riposte import Riposte
import math

calculator = Riposte(prompt="▲:~$ ")
MEMORY = []


class square:
    @calculator.command("square-area")
    def area(side: float):
        square_area = side ** 2
        result = f"{side} ** 2 = {square_area}"
        MEMORY.append(result)
        calculator.success(result)
        return square_area

    @calculator.command("square-perimeter")
    def perimeter(side: float):
        square_peri = side * 4
        result = f"{side} * 4 = {square_peri}"
        MEMORY.append(result)
        calculator.success(result)
        return square_peri


class triangle:
    @calculator.command("triangle-area")
    def area(base: float, height: float):
        triangle_area = (base * height) / 2
        result = f"({base} * {height}) / 2 = {triangle_area}"
        MEMORY.append(result)
        calculator.success(result)
        return triangle_area

    @calculator.command("triangle-perimeter")
    def perimeter(sideA: float, sideB: float, sideC: float):
        triangle_peri = sideA + sideB + sideC
        result = f"{sideA} + {sideB} + {sideC} = {triangle_peri}"
        MEMORY.append(result)
        calculator.success(result)
        return triangle_peri


class circle:
    @calculator.command("circle-area")
    def area(radius: float):
        circle_area = math.pi * radius ** 2
        result = f"pi * {radius} ** 2 = {circle_area}"
        MEMORY.append(result)
        calculator.success(result)
        return circle_area

    @calculator.command("circle-perimeter")
    def perimeter(radius: float):
        circle_peri = 2 * math.pi * radius
        result = f"2 * pi * {radius} = {circle_peri}"
        MEMORY.append(result)
        calculator.success(result)
        return circle_peri


class trapezoid:
    @calculator.command("trapezoid-area")
    def area(short_base: float, long_base: float, height: float):
        trapezoid_area = ((short_base + long_base) / 2) * height
        result = f"(({short_base} + {long_base}) / 2 ) * {height} = {trapezoid_area}"
        MEMORY.append(result)
        calculator.success(result)
        return trapezoid_area

    @calculator.command("trapezoid-perimeter")
    def perimeter(short_base: float, long_base: float, sideA: float, sideB: float):
        trapezoid_peri = short_base + long_base + sideA + sideB
        result = f"{short_base} + {long_base} + {sideA} + {sideB} = {trapezoid_peri}"
        MEMORY.append(result)
        calculator.success(result)
        return trapezoid_peri


class cone:
    @calculator.command("cone-volume")
    def volume(height: float, radius: float):
        volume = (1.0 / 3) * math.pi * radius * radius * height
        result = f"(1.0/3) * pi * {radius} * {radius} * {height} = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("cone-surface_area")
    def surfaceArea(height: float, radius: float):
        length = math.sqrt((radius * radius) + (height * height))
        surface_area = math.pi * radius * (radius + length)
        result = f"pi * {radius} * ({radius} + sqrt(({radius} * {radius}) + ({height} * {height}))) = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class cube:
    @calculator.command("cube-volume")
    def volume(length: float):
        volume = length ** 3
        result = f"{length} ** 3 = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("cube-surface_area")
    def surfaceArea(length: float):
        surface_area = (6 * length) ** 2
        result = f"(6 * {length}) ** 2 = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class cylinder:
    @calculator.command("cylinder-volume")
    def volume(height: float, radius: float):
        volume = math.pi * (radius ** 2) * height
        result = f"pi * ({radius} ** 2) * {height} = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("cylinder-surface_area")
    def surfaceArea(height: float, radius: float):
        surface_area = (2 * math.pi * radius * height) + (2 * math.pi * (radius ** 2))
        result = f"(2 * pi * {radius} * {height}) + (2 * pi * ({radius} ** 2) = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class rectangularPrism:
    @calculator.command("rectangularPrism-volume")
    def volume(lenght: float, width: float, height: float):
        volume = lenght * width * height
        result = f"{lenght} * {width} * {height} = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("rectangularPrism-surface_area")
    def surfaceArea(lenght: float, width: float, height: float):
        surface_area = (2 * lenght * width) + (2 * (lenght + width) * height)
        result = f"(2 * {lenght} * {width}) + (2 * ({lenght} + {width}) * {height}) = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class pyramid:
    @calculator.command("pyramid-volume")
    def volume(lenght: float, width: float, height: float):
        volume = (lenght * width * height) / 3
        result = f"({lenght} * {width} * {height}) / 3 = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("pyramid-surface_area")
    def surfaceArea(lenght: float, width: float, height: float):
        surface_area = (
            (lenght * width)
            + (lenght * math.sqrt((width / 2) ** 2 + height ** 2))
            + (width * math.sqrt((lenght / 2) ** 2 + height ** 2))
        )
        result = f"({lenght} * {width}) + ({lenght} * sqrt(({width}/2)**2 + {height}**2)) + ({width} * sqrt(({lenght}/2)**2 + {height}**2)) = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class sphere:
    @calculator.command("sphere-volume")
    def volume(radius: float):
        volume = (4 * math.pi * radius ** 3) / 3
        result = f"(4 * pi * {radius}**3) / 3 = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("sphere-surface_area")
    def surfaceArea(radius: float):
        surface_area = 4 * math.pi * radius ** 2
        result = f"4 * pi * {radius}**2 = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class hemisphere:
    @calculator.command("hemisphere-volume")
    def volume(radius: float):
        volume = (2 * math.pi * radius ** 3) / 3
        result = f"(2 * pi * {radius}**3) / 3 = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("hemisphere-surface_area")
    def surfaceArea(radius: float):
        surface_area = 3 * math.pi * radius ** 2
        result = f"3 * pi * {radius}**2 = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


class frustrum:
    @calculator.command("frustrum-volume")
    def volume(radiusTop: float, radiusBottom: float, height: float):
        volume = (
            (math.pi / 3)
            * height
            * (radiusBottom ** 2 + radiusTop ** 2 + radiusBottom * radiusTop)
        )
        result = f"(pi/ 3) * {height} * ({radiusBottom}**2 + {radiusTop}**2 + {radiusBottom} * {radiusTop}) = {volume}"
        MEMORY.append(result)
        calculator.success(result)
        return volume

    @calculator.command("frustrum-surface_area")
    def surfaceArea(radiusTop: float, radiusBottom: float, height: float):
        root_this = (radiusBottom - radiusTop) ** 2 + height ** 2
        surface_area = (
            math.pi * (radiusBottom + radiusTop) * math.sqrt(root_this)
            + math.pi * (radiusBottom ** 2)
            + math.pi * (radiusTop ** 2)
        )
        result = f"A lot of math later = {surface_area}"
        MEMORY.append(result)
        calculator.success(result)
        return surface_area


@calculator.command("memory")
def memory():
    for entry in MEMORY:
        calculator.print(entry)


@calculator.command("help")
def help():
    calculator.print(
        """ 
  Commands:
    - 2D
      - Square
        - Area            : square-area {side}
        - Perimeter       : square-perimeter {side}
      - Triangle
        - Area            : triangle-area {base} {height}
        - Perimeter       : triangle-perimeter {sideA} {sideB} {sideC}
      - Circle
        - Area            : circle-area {radius}
        - Perimeter       : circle-perimeter {radius}
      - Trapezoid
        - Area            : trapezoid-area {short_base} {long_base} {height}
        - Perimeter       : trapezoid-perimeter {short_base} {long_base} {sideA} {sideB}

    - 3D
      - Cone
        - Volume          : cone-volume {height} {radius}
        - Surface Area    : cone-surface_area {height} {radius}
      - Cube
        - Volume          : cube-volume {length}
        - Surface Area    : cube-surface_area {length}
      - Cylinder 
        - Volume          : cylinder-volume {height} {radius}
        - Surface Area    : cylinder-surface_area {height} {radius}
      - Rectangular Prism
        - Volume          : rectangularPrism-volume {lenght} {width} {height}
        - Surface Area    : rectangularPrism-surface_area {lenght} {width} {height}
      - Pyramid
        - Volume          : pyramid-volume {lenght} {width} {height}
        - Surface Area    : pyramid-surface_area {lenght} {width} {height}
      - Sphere
        - Volume          : sphere-volume {radius}
        - Surface Area    : sphere-surface_area {radius}
      - Hemisphere
        - Volume          : hemisphere-volume {radius}
        - Surface Area    : hemisphere-surface_area {radius}
      - Frustrum
        - Volume          : frustrum-volume {radiusTop} {radiusBottom} {height}
        - Surface Area    : frustrum-surface_area {radiusTop} {radiusBottom} {height}
      """
    )


@calculator.command("exit")
def close():
    exit()


def main():
    print(
        r"""
 ________  ___  ___  ________  ________  _______   ________  ________  ___          
|\   ____\|\  \|\  \|\   __  \|\   __  \|\  ___ \ |\   ____\|\   __  \|\  \         
\ \  \___|\ \  \\\  \ \  \|\  \ \  \|\  \ \   __/|\ \  \___|\ \  \|\  \ \  \        
 \ \_____  \ \   __  \ \   __  \ \   ____\ \  \_|/_\ \  \    \ \   __  \ \  \       
  \|____|\  \ \  \ \  \ \  \ \  \ \  \___|\ \  \_|\ \ \  \____\ \  \ \  \ \  \____  
    ____\_\  \ \__\ \__\ \__\ \__\ \__\    \ \_______\ \_______\ \__\ \__\ \_______\
   |\_________\|__|\|__|\|__|\|__|\|__|     \|_______|\|_______|\|__|\|__|\|_______|
   \|_________|                                                                     
                                                                                    
Type "help" for help.
    """
    )
    calculator.run()


if __name__ == "__main__":
    main()
