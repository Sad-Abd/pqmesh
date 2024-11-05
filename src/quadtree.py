import numpy as np
from typing import List, Tuple, Set
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

class Node:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y

class Element:
    def __init__(self, id: int, nodes: List[int]):
        self.id = id
        self.nodes = nodes  # Counter-clockwise order
        self.materials = set()  # Set of material numbers

class Quadtree:
    def __init__(self, boundary: Tuple[float, float, float, float], shapes: List = None, depth=0, max_depth=5):
        self.boundary = boundary  # (x_min, y_min, x_max, y_max)
        self.depth = depth
        self.max_depth = max_depth
        self.points = []  # Boundary points in this cell
        self.children = []
        self.is_leaf = True
        self.shapes = shapes or []  # Store shapes for material checking
        
        # For mesh generation
        self.node_dict = {}  # (x,y) -> node_id
        self.next_node_id = 0
        self.elements = []
        self.next_element_id = 0

    def insert_point(self, point: Tuple[float, float, int]):  # (x, y, material)
        self.points.append(point)

    def subdivide(self, threshold: int):
        """Subdivide cell if it contains more points than threshold"""
        if len(self.points) <= threshold or self.depth >= self.max_depth:
            return

        self.is_leaf = False
        mid_x = (self.boundary[0] + self.boundary[2]) / 2
        mid_y = (self.boundary[1] + self.boundary[3]) / 2

        # Define quadrants in counter-clockwise order
        quadrants = [
            (self.boundary[0], self.boundary[1], mid_x, mid_y),      # Bottom Left
            (mid_x, self.boundary[1], self.boundary[2], mid_y),      # Bottom Right
            (mid_x, mid_y, self.boundary[2], self.boundary[3]),      # Top Right
            (self.boundary[0], mid_y, mid_x, self.boundary[3])       # Top Left
        ]

        # Create children and distribute points
        for quad in quadrants:
            child = Quadtree(quad, self.shapes, self.depth + 1, self.max_depth)
            # Add points that fall within this quadrant
            for point in self.points:
                if (quad[0] <= point[0] <= quad[2] and 
                    quad[1] <= point[1] <= quad[3]):
                    child.insert_point(point)
            child.subdivide(threshold)
            self.children.append(child)

    def get_or_create_node(self, x: float, y: float) -> int:
        """Get existing node ID or create new node"""
        key = (round(x, 6), round(y, 6))  # Round coordinates to avoid floating point issues
        if key not in self.node_dict:
            self.node_dict[key] = Node(self.next_node_id, x, y)
            self.next_node_id += 1
        return self.node_dict[key].id

    def get_cell_materials(self, corners) -> Set[int]:
        """Determine which materials a point belongs to"""
        materials = set()
        
        for each in corners:
            point = Point(each[0], each[1])
            
            # First add materials from boundary points in the cell
            for p in self.points:
                materials.add(p[2])
                
            # Then check if point is inside any shapes
            for shape in self.shapes:
                if shape.inside_point(point):
                    materials.add(shape.material)
                
        return materials

    def generate_mesh(self) -> Tuple[List[Node], List[Element]]:
        """Generate mesh elements for the entire quadtree"""
        if self.is_leaf:
            # Create nodes for cell corners
            corners = [
                (self.boundary[0], self.boundary[1]),  # Bottom Left
                (self.boundary[2], self.boundary[1]),  # Bottom Right
                (self.boundary[2], self.boundary[3]),  # Top Right
                (self.boundary[0], self.boundary[3])   # Top Left
            ]
            
            node_ids = [self.get_or_create_node(x, y) for x, y in corners]
            
            # Create element
            element = Element(self.next_element_id, node_ids)
            self.next_element_id += 1
            
            
            # Assign materials based on center point
            element.materials = self.get_cell_materials(corners)
                
            self.elements.append(element)
            
        else:
            for child in self.children:
                child.node_dict = self.node_dict
                child.next_node_id = self.next_node_id
                child.next_element_id = self.next_element_id
                child.generate_mesh()
                self.next_node_id = child.next_node_id
                self.next_element_id = child.next_element_id
                self.elements.extend(child.elements)

        return list(self.node_dict.values()), self.elements

    def plot(self, ax=None, plot_points=True):
        """Plot the quadtree with points and material information"""
        if ax is None:
            ax = plt.gca()

        # Plot cell boundaries
        ax.plot([self.boundary[0], self.boundary[2], self.boundary[2], self.boundary[0], self.boundary[0]],
                [self.boundary[1], self.boundary[1], self.boundary[3], self.boundary[3], self.boundary[1]],
                'b-', linewidth=0.5)

        if self.is_leaf:
            # Plot center point with material information
            center_x = (self.boundary[0] + self.boundary[2]) / 2
            center_y = (self.boundary[1] + self.boundary[3]) / 2
            
            corners = [
                (self.boundary[0], self.boundary[1]),  # Bottom Left
                (self.boundary[2], self.boundary[1]),  # Bottom Right
                (self.boundary[2], self.boundary[3]),  # Top Right
                (self.boundary[0], self.boundary[3])   # Top Left
            ]
            
            materials = self.get_cell_materials(corners)
            if materials:
                material_str = ','.join(map(str, sorted(materials)))
                ax.text(center_x, center_y, material_str, fontsize=8, ha='center', va='center')
            
            if plot_points:
                # Plot boundary points
                for point in self.points:
                    ax.plot(point[0], point[1], 'ro', markersize=2)

        for child in self.children:
            child.plot(ax, plot_points)

class DomainBox:
    def __init__(self, width: float, height: float, shapes: List):
        self.width = width
        self.height = height
        self.shapes = shapes
        self.quadtree = Quadtree((0, 0, width, height), shapes)

    def partition(self, boundary_points: List[Tuple[float, float, int]], threshold: int):
        """
        Partition domain using boundary points
        boundary_points: List of (x, y, material_number)
        """
        for point in boundary_points:
            self.quadtree.insert_point(point)
        self.quadtree.subdivide(threshold)

    def generate_mesh(self) -> Tuple[List[Node], List[Element]]:
        return self.quadtree.generate_mesh()

    def plot(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        self.quadtree.plot(ax)
        plt.show()

def process_boundary_points(shapes: List) -> List[Tuple[float, float, int]]:
    """Convert shape boundary points to (x, y, material) format"""
    boundary_points = []
    for shape in shapes:
        points = shape.get_boundary_points()
        material = shape.material
        boundary_points.extend([(x, y, material) for x, y in points])
    return boundary_points