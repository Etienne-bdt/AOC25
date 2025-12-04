import numpy as np

def parse_input(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return np.array([list(line) for line in lines])

def compute_grid(grid):
    positions = []
    pos_no_neighbours = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '@':
                num_neighbours = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        if is_paperroll(r + dr, c + dc, grid):
                            num_neighbours += 1
                positions.append((r, c, num_neighbours))
                pos_no_neighbours.append((r, c))
    return positions, pos_no_neighbours

def is_paperroll(row, col, grid):
    if isinstance(row, list) or isinstance(col, list):
        return [is_paperroll(r, c, grid) for r in row for c in col]
    else:
        rows = len(grid)
        cols = len(grid[0])
        if row >= rows or col >= cols or row < 0 or col < 0:
            return False
        elif grid[row, col] == "@":
            return True
        else:
            return False

def accessible(positions):
    return [1 if pos[2] < 4 else 0 for pos in positions]

def remove_accessible(positions, accessible_positions, pos_no_neighbours):
    m_pos = [pos if accessible_positions[idx] == 1 else None for idx, pos in enumerate(positions)]
    m_pos = [pos for pos in m_pos if pos is not None]
    for masked_pos in m_pos:
        idx_to_remove = pos_no_neighbours.index((masked_pos[0], masked_pos[1]))
        positions.pop(idx_to_remove)
        pos_no_neighbours.remove((masked_pos[0], masked_pos[1]))
        #Decrement neighbours
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                neighbour = (masked_pos[0] + dr, masked_pos[1] + dc)
                if neighbour in pos_no_neighbours:
                    idx = pos_no_neighbours.index(neighbour)
                    positions[idx] = (positions[idx][0], positions[idx][1], positions[idx][2] - 1)
    return positions, pos_no_neighbours


def part2(positions, pos_no_neighbours):
    sum_accessible = 0
    accessible_positions = accessible(positions)
    while accessible_positions.count(1) >0:
        sum_accessible += accessible_positions.count(1)
        positions, pos_no_neighbours = remove_accessible(positions, accessible_positions, pos_no_neighbours)
        accessible_positions = accessible(positions)
    return sum_accessible


def main():
    input = parse_input("d4/input.txt")
    find_paper, pos_no_neighbours = compute_grid(input)
    accessible_positions = accessible(find_paper)
    print(f"Accessible positions: {accessible_positions.count(1)}")
    part2_result = part2(find_paper, pos_no_neighbours)
    print(f"Part 2 result: {part2_result}")
if __name__ == "__main__":
    main()