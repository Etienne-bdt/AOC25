import numpy as np

def parse_input(file_path: str): 
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = []
    for line in lines:
        #Remove \n and split by space
        parts = line.strip().split()
        data.append(parts)
    return np.array(data)

def compute_column(col):
    operator = col[-1]
    match operator:
        case '+':
            return np.sum(col[:-1].astype(int))
        case '*':
            return np.prod(col[:-1].astype(int))
        case _:
            raise ValueError(f"Unknown operator: {operator}")

def compute_array(array: np.ndarray):
    results = []
    for col in array.T:
        result = compute_column(col)
        results.append(result)
    return sum(results)

def read_cephalopod(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pre_data = np.array([line.strip('\n') for line in lines]).reshape(1,-1)
    for data in pre_data:
        split_data = np.array([list(item) for item in data])
    #add column of ' ' at the end for padding
    split_data = np.pad(split_data, ((0, 0), (0, 1)), mode='constant', constant_values=' ')
    return split_data

def ceph_to_int(cephalopod: np.ndarray) -> np.ndarray:
    char_arrays = [char for char in cephalopod[:,:-1].T]
    #Drop ''s in array
    int_arrays = []
    for char_array in char_arrays:
        sub_array = ''
        for char in char_array:
            if char != ' ':
                sub_array += char
        int_arrays.append(int(sub_array))
    return np.array(int_arrays)

def process_number_groups(cephalopod_data: np.ndarray):
    operators = cephalopod_data[-1, :]
    operator_indexes = np.where(np.isin(operators, ['+', '*']))[0]
    operator_indexes = np.concatenate((operator_indexes, [cephalopod_data.shape[1]]))
    all_ops = []
    for i in range(len(operator_indexes)-1):
        start_idx = operator_indexes[i]
        end_idx = operator_indexes[i+1]
        number_group = cephalopod_data[:-1, start_idx:end_idx]
        operator = operators[operator_indexes[i]]
        number_group = ceph_to_int(number_group)
        print(number_group)
        match operator:
            case '+':
                result = np.sum(number_group.astype(int))
            case '*':
                result = np.prod(number_group.astype(int))
            case _:
                raise ValueError(f"Unknown operator: {operator}")
        all_ops.append(result)
    print( all_ops)
    return np.sum(all_ops)
def main():
    input_file = 'd6/input.txt'
    array = parse_input(input_file)
    results = compute_array(array)
    print(results)

    cephalopod_data = read_cephalopod(input_file)
    result2 = process_number_groups(cephalopod_data)

    print(result2)
if __name__ == "__main__":
    main()