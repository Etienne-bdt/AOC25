import numpy as np

def parse_input(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    ranges = lines.index('')  # Find the index of the empty line separating ranges and numbers
    range_lines = lines[:ranges]
    number_lines = lines[ranges + 1:]
    ranges = list(set([parse_range(line) for line in range_lines]))
    return ranges, [int(num) for num in number_lines]

def parse_range(line):
    parts = line.split('-')
    begin = int(parts[0])
    end = int(parts[1])
    return range(begin, end + 1)

def ranges_overlap(r1, r2):
    return r1.start <= r2.stop and r2.start <= r1.stop
def merge_ranges(r1, r2):
    new_start = min(r1.start, r2.start)
    new_end = max(r1.stop - 1, r2.stop - 1)
    return range(new_start, new_end + 1)

def combine_ranges(ranges):
    combined = []
    for r in ranges:
        merged = False
        for i, cr in enumerate(combined):
            if ranges_overlap(r, cr):
                combined[i] = merge_ranges(r, cr)
                merged = True
                break
        if not merged:
            combined.append(r)
    return combined

def len_ranges(ranges):
    total = 0
    for r in ranges:
        total += len(r)
    return total

def main():
    ranges, numbers = parse_input("d5/input.txt")
    ranges = combine_ranges(ranges)
    while True:
        new_ranges = combine_ranges(ranges)
        if len(new_ranges) == len(ranges):
            break
        ranges = new_ranges
    count = 0
    for number in numbers:
        for r in ranges:
            if number in r:
                count += 1
                break

    print(count)
    print(len_ranges(ranges))

if __name__ == "__main__":
    main()