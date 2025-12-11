from collections import defaultdict

def parse_input(file_path):
    """Parse the input file and return a list of points."""
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            origin = line.strip().split(':')[0]
            dests = line.strip().split(':')[1][1:].split(' ')
            data[origin] = dests
    return data

def dfs(node, data, vis, paths, out='out'):
    """
    Depth-First Search to find all routes between node and out.
    """
    vis.add(node)
    for neighbor in data.get(node, []):
        if neighbor == out:
            paths[node] += 1
            continue
        if neighbor not in vis:
            dfs(neighbor, data, vis, paths, out)
        paths[node] += paths[neighbor]
    return paths[node]

def make_paths():
    return defaultdict(int)

def main():
    file_path = 'd11/input.txt'
    data = parse_input(file_path)
    start_node = 'you'
    total_routes = dfs(start_node, data, set(), make_paths(), out="out")
    print(f"Total routes from '{start_node}' to 'out': {total_routes}")
    part2 = dfs("svr", data, set(), make_paths(), "dac") * dfs("dac", data, set(), make_paths(), "fft") * \
    dfs("fft", data, set(), make_paths(), "out") + dfs("svr", data, set(), make_paths(), "fft") * dfs("fft", data, set(), make_paths(), "dac") \
    * dfs("dac", data, set(), make_paths(), "out")
    print(f"Part 2 result: {part2}")

if __name__ == "__main__":
    main()