from sort_methods.help_func import merge, heapify


def bubble_sort(object: list):
    bubble = True
    while bubble:
        bubble = False
        for index in range(len(object) - 1):
            if object[index] > object[index + 1]:
                object[index], object[index + 1] = object[index + 1], object[index]
                bubble = True
    return object


def selection_sort(object: list):
    for i in range(len(object)):
        selected = i
        for j in range(i + 1, len(object)):
            if object[j] < object[selected]:
                selected = j
        object[i], object[selected] = object[selected], object[i]
    return object


def insertion_sort(object: list):
    for i in range(1, len(object)):
        insert = object[i]
        j = i - 1
        while j >= 0 and object[j] > insert:
            object[j + 1] = object[j]
            j -= 1
        object[j + 1] = insert
    return object


def heap_sort(object: list):
    n = len(object)
    for i in range(n, -1, -1):
        heapify(object, n, i)
    for i in range(n - 1, 0, -1):
        object[i], object[0] = object[0], object[i]
        heapify(object, i, 0)
    return object


def merge_sort(object: list):
    if len(object) <= 1:
        return object
    mid = len(object) // 2
    left_list = merge_sort(object[:mid])
    right_list = merge_sort(object[mid:])
    return merge(left_list, right_list)
