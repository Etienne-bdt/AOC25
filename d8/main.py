from scipy.spatial import cKDTree
import numpy as np


def parse_input(file_path):
    """Parse input file and return list of 3D points."""
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y, z = map(float, line.strip().split(','))
            points.append((x, y, z))
    return points


def find_k_smallest_distances(tree, k):
    """
    Get the k smallest distances from each point in the cKDTree to its nearest neighbors.
    Return the k global smallest distances and the corresponding point indices.
    (From which to which points these distances originate)
    """
    distances, indices = tree.query(tree.data, k=k)
    # Exclude the first column which is the distance to itself (0)
    return distances[:, 1:], indices[:, 1:]


def get_sorted_distances(distances, indices):
    """Flatten and sort distances, returning sort indices and flattened indices."""
    flat_distances = distances.flatten()
    flat_indices = indices.flatten()
    sort_indices = np.argsort(flat_distances)
    return sort_indices, flat_indices


def merge_into_subgraph(sub_graphs, idx1, idx2):
    """
    Merge two point indices into existing sub-graphs or create a new one.
    Returns True if both indices were already in the same sub-graph.
    """
    for s in sub_graphs:
        if idx1 in s and idx2 in s:
            return True
        elif idx1 in s or idx2 in s:
            for i in sub_graphs:
                if i is not s and (idx1 in i or idx2 in i):
                    s.update(i)
                    sub_graphs.remove(i)
                else:
                    s.update([idx1, idx2])
            return False
    sub_graphs.append(set([idx1, idx2]))
    return False


def build_initial_subgraphs(sort_indices, flat_indices, k):
    """Build initial sub-graphs from the k smallest distances."""
    sub_graphs = []
    global_k_smallest = sort_indices[:2*k]
    corresponding_indices = flat_indices[global_k_smallest]
    idx_to_stop = 2*k
    
    for idx in range(0, len(global_k_smallest), 2):
        if idx >= idx_to_stop:
            break
        idx1 = corresponding_indices[idx]
        idx2 = corresponding_indices[idx + 1]
        if merge_into_subgraph(sub_graphs, idx1, idx2):
            k += 2
    
    return sub_graphs


def add_isolated_points(sub_graphs, points):
    """Add any points not yet in a sub-graph as isolated sub-graphs."""
    for p in points:
        point_idx = points.index(p)
        found = any(point_idx in s for s in sub_graphs)
        if not found:
            sub_graphs.append(set([np.int64(point_idx)]))


def find_largest_subgraphs(sub_graphs, j):
    """Return the j largest sub-graphs sorted by size."""
    return sorted(sub_graphs, key=lambda x: len(x), reverse=True)[:j]


def connect_all_subgraphs(sub_graphs, sort_indices, flat_indices, k):
    """Connect all sub-graphs by processing additional distances."""
    while len(sub_graphs) > 1:
        global_k_smallest = sort_indices[k:k+2]
        corresponding_indices = flat_indices[global_k_smallest]
        
        for idx in range(0, len(global_k_smallest), 2):
            idx1 = corresponding_indices[idx]
            idx2 = corresponding_indices[idx + 1]
            merge_into_subgraph(sub_graphs, idx1, idx2)
        k += 2
    
    return k, corresponding_indices[0], corresponding_indices[1]


def part1(sub_graphs, j=3):
    """Compute and print part 1 result: product of j largest sub-graph sizes."""
    j_largest = find_largest_subgraphs(sub_graphs, j)
    sizes = [len(s) for s in j_largest]
    product = np.prod(sizes)
    print(f"Found {len(sub_graphs)} sub-graphs:")
    print(f"The {product} combinations of the sizes of the {j} largest sub-graphs: {sizes}")
    return product


def part2(sub_graphs, sort_indices, flat_indices, points, k=1000):
    """Compute and print part 2 result: product of x-coordinates of final connecting points."""
    final_k, idx1, idx2 = connect_all_subgraphs(sub_graphs, sort_indices, flat_indices, k)
    result = points[idx1][0] * points[idx2][0]
    print(f"Final product of x-coordinates: {int(result)}")
    return result


def main():
    input_file = "d8/input.txt"
    k = 1000
    
    # Parse input and build KD-tree
    points = parse_input(input_file)
    tree = cKDTree(points)
    
    # Find k smallest distances
    distances, indices = find_k_smallest_distances(tree, k)
    sort_indices, flat_indices = get_sorted_distances(distances, indices)
    
    # Build initial sub-graphs
    sub_graphs = build_initial_subgraphs(sort_indices, flat_indices, k)
    add_isolated_points(sub_graphs, points)
    
    # Part 1
    part1(sub_graphs, j=3)
    
    # Part 2
    part2(sub_graphs, sort_indices, flat_indices, points, k)


if __name__ == "__main__":
    main()