from quadtree import *
import geometry as gm

if __name__ == "__main__":
    circle = gm.Circle(50, 50, 20, 1, 20)
    boundary_points = circle.get_boundary_points()
    domain_box = DomainBox(100, 100)
    threshold = 1
    domain_box.partition(boundary_points, threshold)
    domain_box.plot()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
