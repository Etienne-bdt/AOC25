def parse_input(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]

def find_voltage(line):
    line_sorted, indexes = zip(*sorted((char, idx) for idx, char in enumerate(line)))
    highest_voltage = line_sorted[-1]
    index_of_highest = indexes[-1]
    if index_of_highest == len(line) - 1:
        second_highest_voltage = line_sorted[-2]
        return int(second_highest_voltage+highest_voltage)
    else:
        first_occurrence = line.index(highest_voltage)
        sub_line = line[first_occurrence + 1:]
        second_highest_voltage = max(sub_line)
        return int(highest_voltage+second_highest_voltage)

def find_voltage_12(line, num_battery=1):
    if len(line) == 0:
        return ""
    elif num_battery == 12:
        return str(max(line))
    line_sorted, indexes = zip(*sorted((char, idx) for idx, char in enumerate(line)))
    unique_voltages = sorted(set(line_sorted))
    highest_voltage = unique_voltages.pop()
    first_occurrence = line.index(highest_voltage)
    while first_occurrence > len(line) - 13+num_battery:
        next_voltage = unique_voltages.pop()
        first_occurrence = line.index(next_voltage)
        highest_voltage = next_voltage
    return (highest_voltage+ find_voltage_12(line[first_occurrence + 1:], num_battery + 1))

    if index_of_highest == len(line) - 1:
        second_highest_voltage = line_sorted[-2]
        return int(second_highest_voltage+highest_voltage)
    else:
        first_occurrence = line.index(highest_voltage)
        sub_line = line[first_occurrence + 1:]
        second_highest_voltage = max(sub_line)
        return int(highest_voltage+second_highest_voltage)

def main():
    input_data = parse_input('d3/input.txt')
    lines_voltages = []
    for line in input_data:
        voltage = find_voltage(line)
        lines_voltages.append((line, voltage))
        print(f"line: {line} voltage: {voltage}")
    print(f"answer: {sum(int(voltage) for _, voltage in lines_voltages)}")
    print("Part 2")
    lines_voltages_12 = []
    for line in input_data:
        voltage = find_voltage_12(line)
        lines_voltages_12.append((line, voltage))
        print(f"line: {line} voltage: {voltage}")
    print(f"answer: {sum(int(voltage) for _, voltage in lines_voltages_12)}")
if __name__ == "__main__":
    main()