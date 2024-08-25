"""
GEOMETRY DEFINITION TEMPLATE!
"""

from abc import ABC, abstractmethod
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def to_numpy_array(points):
        x_coords = [point.x for point in points]
        y_coords = [point.y for point in points]
        return np.array([x_coords, y_coords]).T


# Abstract Class
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
            angle = 2 * np.pi * i / num_points
            x = self.center_x + self.radius * np.cos(angle)
            y = self.center_y + self.radius * np.sin(angle)
            points.append(Point(x, y))
        return points

    def inside_point(self, point):
        distance = np.sqrt(
            (point.x - self.center_x) ** 2 + (point.y - self.center_y) ** 2
        )
        return distance <= self.radius


class Square(Shape):

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
                x = self.center_x - self.side_length / 2 + self.side_length * t * 4
                y = self.center_y - self.side_length / 2
            elif t < 0.5:
                x = self.center_x + self.side_length / 2
                y = (
                    self.center_y
                    - self.side_length / 2
                    + self.side_length * (t - 0.25) * 4
                )
            elif t < 0.75:
                x = (
                    self.center_x
                    + self.side_length / 2
                    - self.side_length * (t - 0.5) * 4
                )
                y = self.center_y + self.side_length / 2
            else:
                x = self.center_x - self.side_length / 2
                y = (
                    self.center_y
                    + self.side_length / 2
                    - self.side_length * (t - 0.75) * 4
                )
            points.append(Point(x, y))
        return points

    def inside_point(self, point):
        return (
            abs(point.x - self.center_x) <= self.side_length / 2
            and abs(point.y - self.center_y) <= self.side_length / 2
        )


class Rectangle(Shape):
    def __init__(self, center_x, center_y, width, height, material):
        super().__init__(material)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

    def to_points(self, num_points):
        points = []
        num_points_per_side = num_points // 4
        for i in range(num_points_per_side):
            t = i / num_points_per_side
            # Bottom side
            points.append(
                Point(
                    self.center_x - self.width / 2 + self.width * t,
                    self.center_y - self.height / 2,
                )
            )
            # Right side
            points.append(
                Point(
                    self.center_x + self.width / 2,
                    self.center_y - self.height / 2 + self.height * t,
                )
            )
            # Top side
            points.append(
                Point(
                    self.center_x + self.width / 2 - self.width * t,
                    self.center_y + self.height / 2,
                )
            )
            # Left side
            points.append(
                Point(
                    self.center_x - self.width / 2,
                    self.center_y + self.height / 2 - self.height * t,
                )
            )
        return points

    def inside_point(self, point):
        return (
            abs(point.x - self.center_x) <= self.width / 2
            and abs(point.y - self.center_y) <= self.height / 2
        )


class MultiPartShape(Shape):
    def __init__(self, material):
        super().__init__(material)
        self.parts = []

    def add_part(self, part, is_hole=False):
        self.parts.append((part, is_hole))

    def to_points(self, num_points):
        points = []
        for part, is_hole in self.parts:
            part_points = part.to_points(num_points)
            if is_hole:
                part_points = [
                    Point(p.x, p.y) for p in part_points
                ]  # or Point(-p.x, -p.y) [I'm not sure!]
            points.extend(part_points)
        return points

    def inside_point(self, point):
        inside_count = 0
        for part, is_hole in self.parts:
            if part.inside_point(point):
                inside_count += 1 if not is_hole else -1
        return inside_count > 0


C1 = Circle(50, 50, 40, material=1)  # A circle
S1 = Square(20, 20, 30, material=2)  # A square
# We might want to consider holes as material with code -1 or 0 [I'm not sure!]
C2 = Circle(50, 50, 20, material=-1)  # A circle
