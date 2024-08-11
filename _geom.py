"""
GEOMETRY DEFINITION TEMPLATE!
"""

import math
from abc import ABC, abstractmethod

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Abstact Class
class Shape(ABC):
    def __init__(self, material):
        self.material = material

    @abstractmethod
    def to_points(self, num_points):
        pass

    @abstractmethod
    def inside_point(self, point):
        pass

# Concrete Classes
class Circle(Shape):
    def __init__(self, center_x, center_y, radius, material):
        super().__init__(material)
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def to_points(self, num_points):
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            points.append(Point(x, y))
        return points

    def inside_point(self, point):
        distance = math.sqrt((point.x - self.center_x)**2 + (point.y - self.center_y)**2)
        return distance <= self.radius

class Square(Shape):
    """
    I think we can replace it with a Rectangle builder for a more general case.
    """
    def __init__(self, center_x, center_y, side_length, material):
        super().__init__(material)
        self.center_x = center_x
        self.center_y = center_y
        self.side_length = side_length

    def to_points(self, num_points):
        points = []
        for i in range(num_points):
            t = i / num_points
            if t < 0.25:
                x = self.center_x - self.side_length/2 + self.side_length * t * 4
                y = self.center_y - self.side_length/2
            elif t < 0.5:
                x = self.center_x + self.side_length/2
                y = self.center_y - self.side_length/2 + self.side_length * (t-0.25) * 4
            elif t < 0.75:
                x = self.center_x + self.side_length/2 - self.side_length * (t-0.5) * 4
                y = self.center_y + self.side_length/2
            else:
                x = self.center_x - self.side_length/2
                y = self.center_y + self.side_length/2 - self.side_length * (t-0.75) * 4
            points.append(Point(x, y))
        return points

    def inside_point(self, point):
        return (abs(point.x - self.center_x) <= self.side_length/2 and
                abs(point.y - self.center_y) <= self.side_length/2)


C1 = Circle(50, 50, 40, material=1) # A circle
S1 = Square(20, 20, 30, material=2)  # A square
# We might want to consider holes as material with code -1 or 0 [I'm not sure!]
C2 = Circle(50, 50, 20, material=-1) # A circle