"""
GEOMETRY DEFINITION TEMPLATE!
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple
from math import radians, cos, sin


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def to_numpy_array(points: List[Point]):
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    return np.array([x_coords, y_coords]).T


# Abstract Class
def generate_boundary_points(shapes: List['Shape']) -> List[Tuple[float, float]]:
    boundary_points = []
    for shape in shapes:
        boundary_points.extend(shape.get_boundary_points())
    return boundary_points


class Shape(ABC):
    def __init__(self, material):
        self.material = material

    @abstractmethod
    def to_points(self, num_points):
        pass

    @abstractmethod
    def inside_point(self, point):
        pass

    @abstractmethod
    def get_boundary_points(self) -> List[Tuple[float, float]]:
        pass

    # Concrete Classes


class Circle(Shape):
    def __init__(self, center_x: float, center_y: float, radius: float, material,num_points):
        super().__init__(material)
        self.center = (center_x, center_y)
        self.radius = radius
        self.num_points = num_points

    def to_points(self, num_points):
        return self.get_boundary_points()

    def inside_point(self, point):
        distance = np.sqrt((point.x - self.center[0]) ** 2 + (point.y - self.center[1]) ** 2)
        return distance <= self.radius

    def get_boundary_points(self):
        points = []
        for angle in np.linspace(0, 360, self.num_points):
            rad = radians(angle)  # Convert to radians
            x = self.center[0] + self.radius * cos(rad)
            y = self.center[1] + self.radius * sin(rad)
            points.append((x, y))
        return points


class Square(Shape):

    def __init__(self, center_x: float, center_y: float, side_length: float, material, num_points):
        super().__init__(material)
        self.center = (center_x, center_y)
        self.side_length = side_length
        self.num_points = num_points

    def to_points(self, num_points):
        return self.get_boundary_points()

    def inside_point(self, point):
        return (
                abs(point.x - self.center[0]) <= self.side_length / 2
                and abs(point.y - self.center[1]) <= self.side_length / 2
        )

    def get_boundary_points(self):
        points = []
        half_side = self.side_length / 2
        points.append((self.center[0] - half_side, self.center[1] - half_side))  # Bottom Left
        points.append((self.center[0] + half_side, self.center[1] - half_side))  # Bottom Right
        points.append((self.center[0] + half_side, self.center[1] + half_side))  # Top Right
        points.append((self.center[0] - half_side, self.center[1] + half_side))  # Top Left
        return points


class Rectangle(Shape):
    def __init__(self, center_x: float, center_y: float, width: float, height: float, material,num_points):
        super().__init__(material)
        self.center = (center_x, center_y)
        self.width = width
        self.height = height
        self.num_points = num_points

    def to_points(self, num_points):
        return self.get_boundary_points()

    def inside_point(self, point):
        return (
                abs(point.x - self.center[0]) <= self.width / 2
                and abs(point.y - self.center[1]) <= self.height / 2
        )

    def get_boundary_points(self):
        points = []
        half_width = self.width / 2
        half_height = self.height / 2
        points.append((self.center[0] - half_width, self.center[1] - half_height))  # Bottom Left
        points.append((self.center[0] + half_width, self.center[1] - half_height))  # Bottom Right
        points.append((self.center[0] + half_width, self.center[1] + half_height))  # Top Right
        points.append((self.center[0] - half_width, self.center[1] + half_height))  # Top Left
        return points


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
                    Point(p[0], p[1]) for p in part_points
                ]
            points.extend(part_points)
        return points

    def inside_point(self, point):
        inside_count = 0
        for part, is_hole in self.parts:
            if part.inside_point(point):
                inside_count += 1 if not is_hole else -1
        return inside_count > 0

    def get_boundary_points(self):
        points = []
        for part, is_hole in self.parts:
            points.extend(part.get_boundary_points())
        return points
