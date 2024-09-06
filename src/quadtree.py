import matplotlib.pyplot as plt


class DomainBox:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.quadtree = Quadtree((0, 0, width, height))

    def partition(self, boundary_points, threshold):
        self.quadtree.partition(boundary_points, threshold)

    def plot(self):
        plt.plot([0, self.width, self.width, 0, 0], [0, 0, self.height, self.height, 0], 'k-')
        self.quadtree.plot()


class Quadtree:
    def __init__(self, boundary, depth=0, max_depth=5):
        self.boundary = boundary  # (x_min, y_min, x_max, y_max)
        self.depth = depth
        self.max_depth = max_depth
        self.shapes = []
        self.children = []

    def is_within(self, quad, shape):
        return quad[0] <= shape[0] <= quad[2] and quad[1] <= shape[1] <= quad[3]

    def partition(self, geoms, threshold):
        if self.depth < self.max_depth and len(geoms) > threshold:
            mid_x = (self.boundary[0] + self.boundary[2]) / 2
            mid_y = (self.boundary[1] + self.boundary[3]) / 2
            quadrants = [(self.boundary[0], self.boundary[1], mid_x, mid_y),  # Top left
                         (mid_x, self.boundary[1], self.boundary[2], mid_y),  # Top right
                         (self.boundary[0], mid_y, mid_x, self.boundary[3]),  # Bottom left
                         (mid_x, mid_y, self.boundary[2], self.boundary[3])]  # Bottom right
            for quad in quadrants:
                child = Quadtree(quad, self.depth + 1, self.max_depth)
                self.children.append(child)
                child_geoms = [geom for geom in geoms if self.is_within(quad, geom)]
                child.partition(child_geoms, threshold)
        else:
            self.shapes = geoms

    def plot(self):
        plt.plot([self.boundary[0], self.boundary[2], self.boundary[2], self.boundary[0], self.boundary[0]],
                 [self.boundary[1], self.boundary[1], self.boundary[3], self.boundary[3], self.boundary[1]], 'b-')
        for shape in self.shapes:
            plt.plot(shape[0], shape[1], 'ro')
        for child in self.children:
            child.plot()
