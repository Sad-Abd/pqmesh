import geometry as gm
import matplotlib.pyplot as plt
import numpy as np
import plot as p

if __name__ == "__main__":
    # Create geometrical shapes
    circle = gm.Circle(50, 50, 20, 1, 20)
    square = gm.Square(50, 50, 10, 1, 4)
    rectangle = gm.Rectangle(50, 50, 30, 10, 2, 4)

    # Create multipart shape
    multi_shape = gm.MultiPartShape(material=3)
    multi_shape.add_part(square)
    multi_shape.add_part(circle, is_hole=True)


    shapes = [
        ("Circle", circle),
        ("Square", square),
        ("Rectangle", rectangle),
        ("multiple shapes", multi_shape),
    ]

    for shape_name, shape in shapes:
        boundary_points = shape.get_boundary_points() if shape_name != "Multipart Shape" else shape.get_boundary_points()

        print(f"\nPlotting {shape_name}:")
        p.plot_shape(boundary_points, 100, 1)
