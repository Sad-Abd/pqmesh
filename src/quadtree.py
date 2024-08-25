import matplotlib.pyplot as plt
from geometry import *


class Cell:
    def __init__(self, x, y, width, height, point=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.point = point
        self.divided = False
        self.nodes = []


class Quadtree:
    def __init__(self, boundary, capacity=1):
        self.root = (Cell
                     (boundary[0], boundary[1], boundary[2], boundary[3], capacity))


def plot_shape(shape, num_points, marker='o'):
    fig, ax = plt.subplots()
    points = shape.to_points(num_points)
    points_array = np.array([(point.x, point.y) for point in points])
    ax.plot(points_array[:, 0], points_array[:, 1], marker, color='k')
    plt.axis('equal')
    plt.show()


num_points = 40

circle = Circle(50, 50, 40, material=1)
plot_shape(circle, num_points)

square = Square(20, 20, 30, material=2)
plot_shape(square, num_points)

rectangle = Rectangle(20, 20, 30, 10, material=2)
plot_shape(rectangle, num_points)

multi_shape = MultiPartShape(material=1)
multi_shape.add_part(Rectangle(10, 10, 20, 10, material=1))
multi_shape.add_part(Circle(10, 10, 2, material=2), is_hole=True)
plot_shape(multi_shape, num_points)
