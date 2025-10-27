"""
Task 1 – Simple Function with Arithmetic
---------------------------------------
Write a function `circle_area(radius)` that returns the area of a circle.
Formula: area = π × radius²
Use the math module for π.
Ask user for radius and print result with 2 decimals.
"""
import math
# TODO: import math

def circle_area(radius):
    """Return the area of a circle given its radius."""
    # TODO: implement formula using math.pi
    area = math.pi * radius**2
    return area

if __name__ == "__main__":
    # TODO: ask for user input, call circle_area(), and print formatted result
    x = float(input('Enter radius ='))
    print(circle_area(x))

    pass
