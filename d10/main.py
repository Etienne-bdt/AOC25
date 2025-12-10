from collections import deque


def parse_input(file_path):
    """Parse the input file and return a list of points."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            lights = line.strip().split(' ')[0]
            buttons = line.strip().split(' ')[1:-1]
            joltage = line.strip().split(' ')[-1]
            data.append((lights, buttons, joltage))

    return data

def process_joltage(joltage):
    joltage = joltage.strip('{').strip('}')
    joltage_set = list(map(int, joltage.split(','))) if joltage else []
    return joltage_set


def process_light(light):
    """Process a single light entry and return goal bitmask."""
    light = light.strip('[').strip(']')
    goal = 0
    for i, state in enumerate(light):
        if state == '#':
            goal |= (1 << i)
    return goal


def process_buttons_bin(buttons):
    """Process button entries and return list of bitmasks."""
    processed_buttons = []
    for button in buttons:
        mask = 0
        for b in button.strip('(').strip(')').split(','):
            mask |= (1 << int(b))
        processed_buttons.append(mask)
    return processed_buttons

def process_buttons(buttons):
    """Process button entries and return list of bitmasks."""
    processed_buttons = []
    for button in buttons:
        mask = 0
        button = button.strip('(').strip(')')
        processed_buttons.append(tuple(sorted(map(int, button.split(',')))))
    return processed_buttons

def solve_bfs(goal, buttons):
    """Solve using BFS to find minimum button presses."""
    q = deque([(0, 0)])
    vis = {0}
    while q:
        curr, steps = q.popleft()
        if curr == goal:
            return steps
        for b in buttons:
            nxt = curr ^ b
            if nxt not in vis:
                vis.add(nxt)
                q.append((nxt, steps + 1))
    return 0

def solve_joltage(joltage, buttons):
    """ Use scipy to solve the joltage problem. """
    target = joltage
    matrix = [[i in b for b in buttons] for i in range(len(target))]
    from scipy.optimize import milp
    c = [1] * len(buttons)
    return milp(c, constraints=[matrix,target, target], integrality=[1]*len(buttons)).fun
    


def main():
    input_file = 'd10/input.txt'
    data = parse_input(input_file)
    sol = 0
    p2 = 0
    for entry in data:
        o_lights, o_buttons, joltage = entry
        goal = process_light(o_lights)
        buttons = process_buttons_bin(o_buttons)
        joltage = process_joltage(joltage)
        sol += solve_bfs(goal, buttons)
        buttons = process_buttons(o_buttons)
        p2+= solve_joltage(joltage, buttons)
    print(f"Solution part 1: {sol}")
    print(f"Solution part 2: {int(p2)}")


if __name__ == "__main__":
    main()