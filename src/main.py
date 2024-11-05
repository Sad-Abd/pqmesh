import geometry as gm
import matplotlib.pyplot as plt
from quadtree import process_boundary_points, DomainBox

if __name__ == "__main__":
    # Create shapes
    circle = gm.Circle(50, 50, 20, material=1, num_points=20)
    square = gm.Square(50, 50, 10, material=2, num_points=4)
    rectangle = gm.Rectangle(50, 50, 30, 10, material=3, num_points=4)

    shapes = [circle, square, rectangle]
    
    # Get boundary points with material information
    boundary_points = process_boundary_points(shapes)

    # Create and partition domain
    domain = DomainBox(100, 100, shapes)  # Pass shapes to DomainBox
    domain.partition(boundary_points, threshold=1)  # Adjust threshold as needed

    # Generate mesh
    nodes, elements = domain.generate_mesh()

    # Print mesh information
    print("\nNodes:")
    for node in nodes:
        print(f"Node {node.id}: ({node.x}, {node.y})")

    print("\nElements:")
    for element in elements:
        print(f"Element {element.id}:")
        print(f"  Nodes (CCW): {element.nodes}")
        print(f"  Materials: {element.materials}")

    # Plot mesh with material information
    domain.plot()