import numpy as np
import matplotlib.pyplot as plt


class Node:

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
        self.root = Node(boundary[0], boundary[1], boundary[2], boundary[3], capacity)

    def insert(self, point):
        self.root.insert(point)

    def query(self, range):
        return self.root.query(range)


def generate_points_around_circle(center, radius, num_points):
    angles = np.linspace(0, 2 * np.pi, num_points)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack((x, y))


radius = 2
center = (5, 5)

num_points = 20
points = generate_points_around_circle(center, radius, num_points)

boundary = (0, 0, 10, 10)
qt = Quadtree(boundary)

for point in points:
    qt.insert(point)

plt.plot(center[0], center[1])
plt.plot(points[:, 0], points[:, 1], 'ko')
plt.axis('equal')
plt.legend()
plt.show()
