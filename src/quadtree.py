from geometry import *
import numpy as np
import matplotlib.pyplot as plt


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def boundary_point(shape: Shape, num_points=40, marker="o", padding=2):
    fig, ax = plt.subplots()
    points = shape.to_points(num_points)
    points_array = np.array([(point.x, point.y) for point in points])
    ax.plot(points_array[:, 0], points_array[:, 1], marker, color="k")
    min_x = np.min(points_array[:, 0])
    max_x = np.max(points_array[:, 0])
    min_y = np.min(points_array[:, 1])
    max_y = np.max(points_array[:, 1])
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max(max_x - min_x, max_y - min_y) + 2 * padding
    half_width = width / 2
    square_nodes = [
        Node(center_x - half_width, center_y - half_width),
        Node(center_x + half_width, center_y - half_width),
        Node(center_x + half_width, center_y + half_width),
        Node(center_x - half_width, center_y + half_width),
        Node(center_x - half_width, center_y - half_width)
    ]
    square_x = [node.x for node in square_nodes]
    square_y = [node.y for node in square_nodes]
    ax.plot(square_x, square_y)
    plt.axis('equal')
    plt.grid()
    plt.show()


num_points = 40
circle = Circle(50, 50, 40, material=1)
boundary_point(circle, num_points, padding=5)

square = Square(20, 20, 30, material=2)
boundary_point(square, num_points, padding=5)

rectangle = Rectangle(50, 50, 60, 30, material=3)
boundary_point(rectangle, num_points, padding=5)
