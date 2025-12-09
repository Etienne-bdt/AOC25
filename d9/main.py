def parse_input(file_path):
    """Parse input file and return list of 3D points."""
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split(','))
            points.append((x, y))
    return points

def get_area(point1, point2):
    """
    Calculate the area of the rectangle defined by two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    width = abs(x2 - x1)+1
    height = abs(y2 - y1)+1
    return width * height

def build_coordinate_maps(points):
    """Build mapping from actual coordinates to compressed indices."""
    x_coords = sorted(set(p[0] for p in points))
    y_coords = sorted(set(p[1] for p in points))
    
    # Map coordinates to indices with spacing for edges
    x_indices = {coord: 2 * i + 2 for i, coord in enumerate(x_coords)}
    y_indices = {coord: 2 * i + 2 for i, coord in enumerate(y_coords)}
    
    return x_indices, y_indices

def mark_edge_pixels(points, x_indices, y_indices):
    """Mark all compressed pixels on polygon edges."""
    edge_pixels = set()
    
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        
        x1_idx = x_indices[p1[0]]
        x2_idx = x_indices[p2[0]]
        y1_idx = y_indices[p1[1]]
        y2_idx = y_indices[p2[1]]
        
        min_x_idx = min(x1_idx, x2_idx)
        max_x_idx = max(x1_idx, x2_idx)
        min_y_idx = min(y1_idx, y2_idx)
        max_y_idx = max(y1_idx, y2_idx)
        
        for x_idx in range(min_x_idx, max_x_idx + 1):
            for y_idx in range(min_y_idx, max_y_idx + 1):
                edge_pixels.add((x_idx, y_idx))
    
    return edge_pixels

def flood_fill_outside(points, x_indices, y_indices):
    """Use flood fill to mark all outside pixels in compressed space."""
    edge_pixels = mark_edge_pixels(points, x_indices, y_indices)
    
    # Grid bounds in compressed space
    grid_size_x = 2 * len(x_indices) + 8
    grid_size_y = 2 * len(y_indices) + 8
    
    # Flood fill from (0, 0)
    outside_pixels = set()
    queue = [(0, 0)]
    outside_pixels.add((0, 0))
    
    while queue:
        x, y = queue.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size_x and 0 <= ny < grid_size_y:
                    if (nx, ny) not in edge_pixels and (nx, ny) not in outside_pixels:
                        outside_pixels.add((nx, ny))
                        queue.append((nx, ny))
    
    return outside_pixels, edge_pixels

def is_rectangle_filled(p1, p2, x_indices, y_indices, outside_pixels):
    """Check if rectangle is fully inside (no outside pixels in compressed space)."""
    x1_idx = x_indices[p1[0]]
    x2_idx = x_indices[p2[0]]
    y1_idx = y_indices[p1[1]]
    y2_idx = y_indices[p2[1]]
    
    min_x_idx = min(x1_idx, x2_idx)
    max_x_idx = max(x1_idx, x2_idx)
    min_y_idx = min(y1_idx, y2_idx)
    max_y_idx = max(y1_idx, y2_idx)
    
    for x_idx in range(min_x_idx, max_x_idx + 1):
        for y_idx in range(min_y_idx, max_y_idx + 1):
            if (x_idx, y_idx) in outside_pixels:
                return False
    return True


def find_largest_enclosed_rectangle(points, x_indices=None, y_indices=None, outside_pixels=None):
    """Find the largest rectangle fully enclosed within the polygon."""
    max_area = 0
    best_pair = None
    

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if x_indices is not None and y_indices is not None and outside_pixels is not None:
                if is_rectangle_filled(points[i], points[j], x_indices, y_indices, outside_pixels):
                    area = get_area(points[i], points[j])
                    if area > max_area:
                        max_area = area
                        best_pair = (i, j)
            else:
                area = get_area(points[i], points[j])
                if area > max_area:
                    max_area = area
                    best_pair = (i, j)
    
    return best_pair, max_area


def print_result(best_pair, max_area, points):
    """Print the result of the largest enclosed rectangle search."""
    if best_pair:
        print(f"Biggest filled area is {max_area} between points {points[best_pair[0]]} and {points[best_pair[1]]}")
    else:
        print("No filled rectangles found")


def main():
    # Parse input
    points = parse_input('d9/input.txt')
    
    best_pair, max_area = find_largest_enclosed_rectangle(points)
    
    print("Part 1:")
    print_result(best_pair, max_area, points)

    # Build coordinate compression maps
    x_indices, y_indices = build_coordinate_maps(points)
    
    # Flood fill to find outside pixels in compressed space
    outside_pixels, edge_pixels = flood_fill_outside(points, x_indices, y_indices)
    
    # Find largest enclosed rectangle
    best_pair, max_area = find_largest_enclosed_rectangle(points, x_indices, y_indices, outside_pixels)
    
    # Print result
    print_result(best_pair, max_area, points)


if __name__ == "__main__":
    main()