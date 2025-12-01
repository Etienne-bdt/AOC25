import logging

logger = logging.getLogger(__name__)


def parse_input(file_path):
    """Reads a file and returns its content as a list of lines."""
    logger.info(f"Reading input file from {file_path}...")
    with open(file_path, "r") as file:
        lines = file.readlines()
    logger.debug(f"Read {len(lines)} lines from the input file.")
    logger.info("Processing input lines...")
    return [process_data(line.strip()) for line in lines]


def process_data(line):
    logger.debug(f"Processing line: {line}")
    direction = line[0]
    if direction == "L":
        dir_num = -1
    elif direction == "R":
        dir_num = 1
    else:
        raise ValueError(f"Invalid direction character: {direction}")
    steps = int(line[1:])
    return dir_num * steps


def overflow_cumsum(data):
    cumsum = [data[0]]
    number_of_overflows = 0
    for i in range(1, len(data)):
        logger.debug(f"Processing index {i} with value {data[i]} and current cumsum {cumsum[-1]}")
        while data[i] > 100 or data[i] < -100:
            logger.debug(f"Value {data[i]} out of bounds, adjusting...")
            if data[i] > 100:
                data[i] -= 100
                logger.debug(f"Decreased value at index {i} to {data[i]} due to number of turns overflow")
                number_of_overflows += 1
            elif data[i] < -100:
                data[i] += 100
                logger.debug(f"Increased value at index {i} to {data[i]} due to number of turns underflow")
                number_of_overflows += 1
        sum = cumsum[i - 1] + data[i]
        if sum >= 100:
            logger.debug(f"Overflow of dial at index {i}, adjusting sum {sum}")
            sum = sum - 100
            logger.debug(f"Adjusted sum at index {i} to {sum} ")
            if sum != 0 and cumsum[i - 1] != 0:
                logger.debug(f"Dial crossed zero at index {i}")
                number_of_overflows += 1
        elif sum < 0:
            logger.debug(f"Underflow of dial at index {i}, adjusting sum {sum}")
            sum = sum + 100
            if sum != 0 and cumsum[i - 1] != 0:
                logger.debug(f"Dial crossed zero at index {i}")
                number_of_overflows += 1
        cumsum.append(sum)
    return cumsum, number_of_overflows


def main():
    logger.info("Parsing input...")
    input_data = parse_input("d1/input.txt")
    input_data.insert(0, 50)  # Start from zero
    logger.info("Input initialized.")
    logger.info("Calculating cumulative sum with overflow handling...")
    cumsum, number_of_overflows = overflow_cumsum(input_data)
    num_zero = cumsum.count(0)
    logger.info(f"Answer to part 1 :Number of times the dial stopped on zero: {num_zero}")
    logger.info(f"Number of times the dial crossed zero: {number_of_overflows}")
    logger.info(f"Answer to part 2 : Total visits to zero: {num_zero + number_of_overflows}")


if __name__ == "__main__":
    # Print banner located at ../banner.txt
    with open("banner", "r") as banner_file:
        banner = banner_file.read()
    print(banner)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger.info("Starting Day 1...")
    main()
