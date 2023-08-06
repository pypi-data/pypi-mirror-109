def heapify(object, size, index):
    largest = index
    left_child = (2 * index) + 1
    right_child = (2 * index) + 2
    if left_child < size and object[left_child] > object[largest]:
        largest = left_child
    if right_child < size and object[right_child] > object[largest]:
        largest = right_child
    if largest != index:
        object[index], object[largest] = object[largest], object[index]
        heapify(object, size, largest)


def merge(left_list, right_list):
    sorted_list = []
    left_list_index = right_list_index = 0
    left_list_length, right_list_length = len(left_list), len(right_list)
    for _ in range(left_list_length + right_list_length):
        if left_list_index < left_list_length and right_list_index < right_list_length:
            if left_list[left_list_index] <= right_list[right_list_index]:
                sorted_list.append(left_list[left_list_index])
                left_list_index += 1
            else:
                sorted_list.append(right_list[right_list_index])
                right_list_index += 1
        elif left_list_index == left_list_length:
            sorted_list.append(right_list[right_list_index])
            right_list_index += 1
        elif right_list_index == right_list_length:
            sorted_list.append(left_list[left_list_index])
            left_list_index += 1
    return sorted_list
