import unittest
from sort_methods import sorter


class test_sorter(unittest.TestCase):

    objects = {
        'test': [[11, 14, 10, 4, 3, 3], [14, 1, 10, 11, 11, 1, 10, 5, 1], [14, 12, 12, 3, 6, 9, 6, 2, 10],
                 [2, 14, 3, 11, 1, 5, 14, 3, 3, 3], [9, 12, 6, 1, 7, 14, 5, 14], [6, 12, 6, 1, 9, 4, 11, 8],
                 [7, 11, 14, 3, 3, 3, 9, 7, 11, 9], [7, 3, 8, 6, 9, 8, 5, 12, 10, 14], [9, 9, 2, 9, 10, 11]],
        'result': [[3, 3, 4, 10, 11, 14], [1, 1, 1, 5, 10, 10, 11, 11, 14], [2, 3, 6, 6, 9, 10, 12, 12, 14],
                   [1, 2, 3, 3, 3, 3, 5, 11, 14, 14], [1, 5, 6, 7, 9, 12, 14, 14], [1, 4, 6, 6, 8, 9, 11, 12],
                   [3, 3, 3, 7, 7, 9, 9, 11, 11, 14], [3, 5, 6, 7, 8, 8, 9, 10, 12, 14], [2, 9, 9, 9, 10, 11]]
    }

    def test_bubble(self):
        for index in range(len(self.objects['test'])):
            self.assertEqual(sorter.bubble_sort(self.objects['test'][index]), self.objects['result'][index])

    def test_selection(self):
        for index in range(len(self.objects['test'])):
            self.assertEqual(sorter.selection_sort(self.objects['test'][index]), self.objects['result'][index])

    def test_insertion(self):
        for index in range(len(self.objects['test'])):
            self.assertEqual(sorter.insertion_sort(self.objects['test'][index]), self.objects['result'][index])

    def test_heap(self):
        for index in range(len(self.objects['test'])):
            self.assertEqual(sorter.heap_sort(self.objects['test'][index]), self.objects['result'][index])

    def test_merge(self):
        for index in range(len(self.objects['test'])):
            self.assertEqual(sorter.merge_sort(self.objects['test'][index]), self.objects['result'][index])
