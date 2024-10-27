import matplotlib.pyplot as plt
import pandas as pd
from quadtree import *
from domain_box import *


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
