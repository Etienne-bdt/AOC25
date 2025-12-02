import logging
from functools import cache

logger = logging.getLogger(__name__)

def parse_input(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    tuples = lines[0].split(",")
    return process_tuples(tuples)


def process_tuples(tuples):
    processed = []
    for tup in tuples:
        a, b = tup.split("-")
        processed.append((a, b))
    return processed


def invalid_ids_p1(tuples):
    invalid = []
    for a, b in tuples:
        for i in range(int(a), int(b) + 1):
            len_id = len(str(i))
            if len_id % 2 != 0:
                continue
            else:
                first_half = str(i)[:len_id // 2]
                second_half = str(i)[len_id // 2:]
                if first_half == second_half:
                    invalid.append(i)
    return invalid


def invalid_id_p2(tuples):
    invalid = []
    for a, b in tuples:
        for i in range(int(a), int(b) + 1):
            str_id = str(i)
            for j in range(len(str_id)):
                logger.debug(f"Checking ID: {str_id}, substring length: {j+1}, pattern: {str_id[:j+1]}")
                if pattern_check(j, str_id):
                    invalid.append(i)
                    break
    return invalid

@cache
def pattern_check(sub_len, id):
    replicate_times = len(id)/(sub_len+1)
    if replicate_times.is_integer() and replicate_times > 1:
        if id == id[:sub_len+1] * int(replicate_times):
            return True
    return False

def main():
    logger.info("Starting the program...")
    tuples = parse_input("d2/input.txt")
    logger.debug(f"Processed tuples: {tuples}")
    part1 = sum(invalid_ids_p1(tuples))
    logger.info(f"Part 1 result: {part1}")
    part2 = sum(invalid_id_p2(tuples))
    logger.info(f"Part 2 result: {part2}")

if  __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()