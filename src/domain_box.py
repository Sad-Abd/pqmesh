from quadtree import *


class DomainBox:
    def __init__(self, width, height):
        # Initialize DomainBox with specified width and height
        self.width = width  # Store the width of the box
        self.height = height  # Store the height of the box
        self.quadtree = Quadtree((0, 0, width, height))  # Create a Quadtree with the given boundaries

    def partition(self, boundary_points, threshold):
        # Partition the quadtree using the provided points and threshold
        self.quadtree.partition(boundary_points, threshold)

    def plot(self):
        # Plot the boundary of the DomainBox
        plt.plot([0, self.width, self.width, 0, 0], [0, 0, self.height, self.height, 0], 'k-')
        # Call plot method on the quadtree to visualize it
        self.quadtree.plot()

    def points_coordinates(self):
        return self.quadtree.points_coordinates()

    def get_elements(self):
        return self.quadtree.get_elements()

    def check_elements_position(self):
        return self.quadtree.check_elements_position()
