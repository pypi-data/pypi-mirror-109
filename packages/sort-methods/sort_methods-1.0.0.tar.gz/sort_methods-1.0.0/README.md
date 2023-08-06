# Sort_methods - it`s a python package for list's sorting
## Installing
pip install sort_methods
## Guide
```python
from sort_methods import sorter

sorter.bubble_sort(object) # bubble-method of sorting, object - list
sorter.selection_sort(object) # selection-method of sorting, object - list
sorter.insertion_sort(object) # insertion-method of sorting, object - list
sorter.heap_sort(object) # heap-method of sorting, object - list
sorter.merge_sort(object) # merge-method of sorting, object - list
```
## All functions, beside merge_sort( ) can sort lists of strings

```python
from sort_methods import sorter

chars = ['e', 'a', 'c', 'b']
sorter.bubble_sort(chars)
sorter.selection_sort(chars)
sorter.insertion_sort(chars)
sorter.heap_sort(chars)
# after any of this operations list 'chars' will be like this: ['a', 'b', 'c', 'e']
```
