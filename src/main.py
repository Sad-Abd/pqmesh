from quadtree import *
import geometry as gm
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    # Create geometrical shapes
    circle = gm.Circle(50, 50, 20, 1, 20)
    square = gm.Square(50, 50, 10, 1, 4)
    rectangle = gm.Rectangle(50, 50, 30, 10, 2, 4)

    # Create multipart shape
    multipart_shape = gm.MultiPartShape(material=3)
    multipart_shape.add_part(circle)
    multipart_shape.add_part(square, is_hole=True)


    def plot_shape(boundary_points, domain_box_size, threshold):
        domain_box = DomainBox(domain_box_size, domain_box_size)
        domain_box.partition(boundary_points, threshold)
        domain_box.plot()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

        points_coord = domain_box.points_coordinates()
        positions_check = domain_box.check_elements_position()

        # Create a DataFrame for points coordinates with position check
        df_points = pd.DataFrame(points_coord, columns=['X', 'Y'])

        # Map positions check to coordinates
        position_mapping = {pos[0]: pos[1] for pos in positions_check}
        df_points['Positions'] = df_points.apply(lambda row: position_mapping.get((row['X'], row['Y']), ''),
                                             axis=1)

        # Sort by X and Y
        sorted_points = df_points

        # Separate boundary points
        boundary_table = pd.DataFrame(boundary_points, columns=['Boundary X', 'Boundary Y'])

        print(sorted_points)
        print("\nBoundary Points:")
        print(boundary_table)


    boundary_points_circle = circle.get_boundary_points()
    boundary_points_square = square.get_boundary_points()
    boundary_points_rectangle = rectangle.get_boundary_points()

    print("Plotting Circle:")
    plot_shape(boundary_points_circle, 100, 1)

    print("\nPlotting Square:")
    plot_shape(boundary_points_square, 100, 1)

    print("\nPlotting Rectangle:")
    plot_shape(boundary_points_rectangle, 100, 1)

    print("\nPlotting Multipart Shape:")
    plot_shape(multipart_shape.get_boundary_points(), 100, 1)
