### A module for visualization of a nested python data structure
***

a nested python objects including list, tuple, dictionary, tensor, ndarray to data-tree, and make a quick peek out of its structure

```
data = a list of 10 lists of 3 dicts of 2 keys : list of 2 strings

dv.viz(data)

$ list of 10
$ └── list of 3
$     └── dict of 2
$         ├── train : ['data1', 'data2']
$         └── test : ['data3', 'data4']

```

### How to use
***
#### install
```
$ pip install dstree
```
#### import and quick_start
```python
import dstree as dst

data = dst.get_example_data()
tree = dst.viz(data)

```
#### usage in detail
```python
import dstree as dst
dst.quick_start() # Copy & Paste console output to implement tutorial codes
```

### Note
this package is built based on treelib & graphviz syntax  
supports int, str, float, list, tuple, dict, Tensor, ndarray, Series, DataFrame datatype  
custom Dataset class will be supported in soon  