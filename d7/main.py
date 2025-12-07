split_counter=0

def parse_input(file_path: str): 
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines

def find_elements_coordinates(data):
    """
    Generate 2D coordinates of specific elements in the array.
    """
    splitters = []
    start = None
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == 'S':
                start = (i, j)
            elif char == '^':
                splitters.append((i, j))
    return start, splitters

def truncate_splitters(splitters):
    """
    Find splitters that are vertically aligned and remove them from the list.
    """
    to_remove = set()
    for i in range(len(splitters)):
        for j in range(i + 1, len(splitters)):
            if splitters[i][1] == splitters[j][1]:
                found_saviour = False
                for k in range(splitters[i][0], splitters[j][0]+1):
                    if (k, splitters[i][1]-1) in splitters or (k, splitters[i][1]+1) in splitters:
                        found_saviour = True
                        break
                if not found_saviour:
                    to_remove.add(splitters[j])
    return [s for s in splitters if s not in to_remove]
    
def find_first_splitter(start, splitters):
    """
    Find the first splitter that is directly below the start position.
    """

    start_x, start_y = start
    vertical_splitters = [s for s in splitters if s[1] == start_y and s[0] > start_x]
    if not vertical_splitters:
        return None
    first_splitter = min(vertical_splitters, key=lambda s: s[0])
    return first_splitter

def split(start, splitter):
    """
    Split the array into two parts at the splitter position.
    """
    _, start_x = start
    split_y, split_x = splitter
    if start_x != split_x:
        raise ValueError("Splitter must be vertically aligned with the start position.")
    part1 = (split_y, split_x-1)
    part2 = (split_y, split_x+1)
    global split_counter
    split_counter += 1
    return part1, part2

def process_splits(start, splitters, visited=None):
    """
    Recursively process splits until no more splitters are found.
    Uses visited set to avoid reprocessing splitters.
    """
    if visited is None:
        visited = set()
    
    splitter = find_first_splitter(start, splitters)
    if splitter is None:
        return [start]
    
    if splitter in visited:
        return []
    
    visited.add(splitter)
    part1, part2 = split(start, splitter)
    
    results = []
    results.extend(process_splits(part1, splitters, visited))
    results.extend(process_splits(part2, splitters, visited))
    return results

def process_splits_p2(start, splitters, memo=None):
    """
    Count all possible paths through splits, including overlapping ones.
    Uses memoization to cache path counts for each position.
    """
    if memo is None:
        memo = {}
    
    # Check if we've already computed this position
    if start in memo:
        return memo[start]
    
    splitter = find_first_splitter(start, splitters)
    if splitter is None:
        # Leaf node - one path ends here
        memo[start] = 1
        return 1
    
    part1 = (splitter[0], splitter[1]-1)
    part2 = (splitter[0], splitter[1]+1)
    
    # Count paths from both branches
    count1 = process_splits_p2(part1, splitters, memo)
    count2 = process_splits_p2(part2, splitters, memo)
    
    # Total paths = sum of paths from both branches
    total = count1 + count2
    memo[start] = total
    return total


def main():
    file_path = 'd7/input.txt'
    data_array = parse_input(file_path)
    start, splitters = find_elements_coordinates(data_array)
    splitters = truncate_splitters(splitters)
    
    # Part 1: Unique splits
    results = process_splits(start, splitters)
    print(f"Total splits made (p1): {split_counter}")
    print(f"Unique endpoints (p1): {len(results)}")

    # Part 2: Total path possibilities
    total_paths = process_splits_p2(start, splitters)
    print(f"Total split possibilities (p2): {total_paths}")

if __name__ == "__main__":
    main()
