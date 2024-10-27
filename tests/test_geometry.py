import unittest
from src.geometry import *


class TestMultiPartShape(unittest.TestCase):

    def test_get_boundary_points_single_shape(self):
        """
        Tests the get_boundary_points method for a MultiPartShape with a single circle.

        Verifies that the boundary points of the MultiPartShape match the boundary points of the sole circle.
        """
        # Create a circle with specified parameters
        center = Point(0, 0)
        radius = 1
        material = "material1"
        num_points = 16
        circle = Circle(center.x, center.y, radius, material, num_points)

        # Create a MultiPartShape and add the circle
        multi_part_shape = MultiPartShape("combined")
        multi_part_shape.add_part(circle)

        # Calculate the expected and actual boundary points
        expected_boundary_points = circle.get_boundary_points()
        actual_boundary_points = multi_part_shape.get_boundary_points()

        # Assert that the boundary points are equal, considering floating-point precision
        self.assertEqual(len(expected_boundary_points), len(actual_boundary_points))
        for i in range(len(expected_boundary_points)):
            self.assertAlmostEqual(expected_boundary_points[i][0], actual_boundary_points[i][0], delta=1e-6)
            self.assertAlmostEqual(expected_boundary_points[i][1], actual_boundary_points[i][1], delta=1e-6)

    def test_get_boundary_points_multiple_shapes(self):
        """
        Tests the get_boundary_points method for a MultiPartShape with a circle and a square.

        Verifies that the boundary points of the MultiPartShape are the combined boundary points of the circle and the square.
        """
        # Create a circle and a square
        center_circle = Point(0, 0)
        radius_circle = 1
        material_circle = "material_circle"
        num_points_circle = 16
        circle = Circle(center_circle.x, center_circle.y, radius_circle, material_circle, num_points_circle)

        center_square = Point(2, 2)
        side_length_square = 2
        material_square = "material_square"
        num_points_square = 4
        square = Square(center_square.x, center_square.y, side_length_square, material_square, num_points_square)

        # Create a MultiPartShape and add the circle and square
        multi_part_shape = MultiPartShape("combined")
        multi_part_shape.add_part(circle)
        multi_part_shape.add_part(square)

        # Calculate the expected and actual boundary points
        expected_circle_boundary_points = circle.get_boundary_points()
        expected_square_boundary_points = square.get_boundary_points()
        expected_boundary_points = expected_circle_boundary_points + expected_square_boundary_points

        actual_boundary_points = multi_part_shape.get_boundary_points()

        # Assert that the boundary points are equal, considering floating-point precision
        self.assertEqual(len(expected_boundary_points), len(actual_boundary_points))
        for i in range(len(expected_boundary_points)):
            self.assertAlmostEqual(expected_boundary_points[i][0], actual_boundary_points[i][0], delta=1e-6)
            self.assertAlmostEqual(expected_boundary_points[i][1], actual_boundary_points[i][1], delta=1e-6)

    def test_get_boundary_points_with_holes(self):
        """
        Tests the get_boundary_points method for a MultiPartShape with a circle and a square hole.

        Verifies that the boundary points of the MultiPartShape include the outer circle's boundary and the inner square's boundary.
        """
        # Create a circle and a square hole
        center_circle = Point(0, 0)
        radius_circle = 2
        material_circle = "material_circle"
        num_points_circle = 16
        circle = Circle(center_circle.x, center_circle.y, radius_circle, material_circle, num_points_circle)

        center_square = Point(0, 0)
        side_length_square = 1
        material_square = "material_square"
        num_points_square = 4
        square = Square(center_square.x, center_square.y, side_length_square, material_square, num_points_square)

        # Create a MultiPartShape and add the circle and square hole
        multi_part_shape = MultiPartShape("combined")
        multi_part_shape.add_part(circle)
        multi_part_shape.add_part(square, is_hole=True)
