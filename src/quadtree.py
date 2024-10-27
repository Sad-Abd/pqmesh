import matplotlib.pyplot as plt


class Quadtree:
    def __init__(self, boundary, depth=0, max_depth=5):
        # Initialize the Quadtree with specified boundary and depth
        self.boundary = boundary  # (x_min, y_min, x_max, y_max) defines the area of the node
        self.depth = depth  # Current depth of the node in the quadtree
        self.max_depth = max_depth  # Maximum allowed depth for subdivision
        self.shapes = []  # Holds shapes contained in this quadtree node
        self.children = []  # Holds child quadtree nodes

    def is_within(self, quad, shape):
        # Check if the shape is within the specified quadrant
        return quad[0] <= shape[0] <= quad[2] and quad[1] <= shape[1] <= quad[3]

    def partition(self, geoms, threshold):
        # Partition the current node if depth is less than max_depth and geometries exceed threshold
        if self.depth < self.max_depth and len(geoms) > threshold:
            # Calculate midpoints to divide the current boundary into four quadrants
            mid_x = (self.boundary[0] + self.boundary[2]) / 2
            mid_y = (self.boundary[1] + self.boundary[3]) / 2

            # Define the four quadrants
            quadrants = [
                (self.boundary[0], self.boundary[1], mid_x, mid_y),  # Top left
                (mid_x, self.boundary[1], self.boundary[2], mid_y),  # Top right
                (self.boundary[0], mid_y, mid_x, self.boundary[3]),  # Bottom left
                (mid_x, mid_y, self.boundary[2], self.boundary[3])  # Bottom right
            ]

            # Iterate through the quad and create child quadtree nodes
            for quad in quadrants:
                child = Quadtree(quad, self.depth + 1, self.max_depth)  # Create a child quadtree
                self.children.append(child)  # Add child to the list of children
                # Filter geometries that fall within the current quadrant
                child_geoms = [geom for geom in geoms if self.is_within(quad, geom)]
                # Recursively partition the child quadtree with the filtered geometries
                child.partition(child_geoms, threshold)
        else:
            self.shapes = geoms

    def points_coordinates(self):
        points_coords = []
        for shape in self.shapes:
            points_coords.append(shape)
        for child in self.children:
            points_coords.extend(child.points_coordinates())
        return points_coords

    def get_elements(self):
        elements = []
        for shape in self.shapes:
            elements.append([shape])
        for child in self.children:
            elements.extend(child.get_elements())
        return elements

    def check_elements_position(self):
        positions = []
        for shape in self.shapes:
            if (self.boundary[0] < shape[0] < self.boundary[2] and
                    self.boundary[1] < shape[1] < self.boundary[3]):
                positions.append((shape, 'inside'))
            elif (shape[0] == self.boundary[0] or shape[0] == self.boundary[2] or
                  shape[1] == self.boundary[1] or shape[1] == self.boundary[3]):
                positions.append((shape, 'on border'))
            else:
                positions.append((shape, 'outside'))
        for child in self.children:
            positions.extend(child.check_elements_position())
        return positions

    def plot(self):
        plt.plot([self.boundary[0], self.boundary[2], self.boundary[2], self.boundary[0], self.boundary[0]],
                 [self.boundary[1], self.boundary[1], self.boundary[3], self.boundary[3], self.boundary[1]], 'b-',
                 linewidth=0.5)
        for shape in self.shapes:
            plt.plot(shape[0], shape[1], 'ro', markersize=1)
        for child in self.children:
            child.plot()
