from collections import namedtuple

import numpy as np
from treelib import Node, Tree
from numpy import ndarray
from torch import Tensor
from pandas import Series, DataFrame
from dataclasses import dataclass
from itertools import islice
from collections import defaultdict
from graphviz import Source, Digraph, Graph
from typing import *

# namespace를 사용하는 몇 함수 및 기능 부
NoneType = type(None)

mapping_type2type = {list: tuple, float: int, DataFrame: ndarray}
mapping_type2size = {int: 0, np.number : 0, NoneType: 0}
terminal_classes = {int, str, float}
defined_classes = {int, str, float, list, tuple, dict, Tensor, ndarray, Series, DataFrame}

defined_classes.update(mapping_type2type.keys())
defined_classes.update(mapping_type2size.keys())
defined_classes.update(terminal_classes)

Tree_fold_meta = namedtuple("Tree_fold_meta", ("parent_nid", "child_node", "child_subtree"))
tree_repo = defaultdict(Tree_fold_meta)

class Custom_class():
    def __init__(self, data):
        self.data = data
    def __getitem__(self, index):
        return self.data[index]
    def __len__(self):
        return len(self.data)
        # return self.data.shape

class Undefined_class():
    def __init__(self, data):
        self.data = data
    def __getitem__(self, index):
        return self.data[index]
    def __len__(self):
        return len(self.data)

def get_n_items(d, i, j):
    return dict(islice(d.items(), i, j))

def struct2msg(dtype, dsize):
    if dtype in terminal_classes:
        msg = f"{dtype.__name__}"
    else:
        msg = f"<{dtype.__name__}> of {' x '.join((str(ds) for ds in dsize))}"
    return msg

def contents2msg(contents, max_print_of_contents, print_rawString):
    sc = str(contents)
    if isinstance(contents, str):
        if print_rawString:
            msg = f"{repr(sc)}"[:max_print_of_contents]
        else:
            msg = f"'{sc}'"[:max_print_of_contents]
    else:
        msg = sc[:max_print_of_contents]

    if len(sc) > max_print_of_contents:
        msg += " ..."
    return msg

def get_example_data(data="woz_data_dir"):
    import os
    import pickle
    import json
    from dataclasses import asdict
    from sklearn.datasets import load_iris
    import pandas as pd

    directory = dict(
        woz_data_dir= "woz_train_en.json",
        feature_dataset_example='feature_dataset_example.pkl',
        iris = 'iris',
        ice = 'train_data.csv'
    )


    global DSTInputExample

    @dataclass
    class DSTInputExample:
        guid: str
        context_turns: List[str]
        current_turn: List[str]
        label: Optional[List[str]] = None

        def to_dict(self):
            return asdict(self)

        def to_json_string(self):
            """Serializes this instance to a JSON string."""
            return json.dumps(self.to_dict(), indent=2) + "\n"

    home = os.path.dirname(__file__)

    if data == "woz_data_dir":
        with open(os.path.join(home, "dstree", directory[data]), 'r', encoding='utf-8') as f:
            example_data = json.load(f)
    elif data == "feature_dataset_example":
        with open(os.path.join(home, "dstree", directory[data]), mode='rb+') as f:
            example_data = pickle.load(f)
    elif data == 'iris':
        example_data = load_iris()
    elif data == 'ice':
        example_data = pd.read_csv(os.path.join(home, 'dstree', directory[data]))
    else:
        return None

    return example_data

@dataclass
class default_options:

    compress_level = 5

    # compress_level 이 명시되지 않았을 떄의 기본값들

    max_print_of_contents = 100
    id_pool = list(range(int(1e7), -1, -1))

    print_tag = False
    print_terminal_contents = True

    main_axis = 0
    # default_main_axis = "smallest"

    max_children_search_threshold = 10 # recommended between 10 to 100
    # default_search_threshold = "maximal"

    print_max_children = {"depth_multiplier" : 1, "upperbound_constant" : 5, "exclude_parent_classes" : [dict, Undefined_class]}
    # print_max_children = {"upperbound_constant" : 1}

    print_rawString = True

@dataclass
class Options():
    def __init__(self, compress_level = None):
        # generate_msg_options
        self.max_print_of_contents = default_options.max_print_of_contents
        self.id_pool = default_options.id_pool

        self.print_tag = default_options.print_tag
        self.print_terminal_contents = default_options.print_terminal_contents

        self.main_axis = default_options.main_axis

        self.max_children_search_threshold = default_options.max_children_search_threshold
        self.print_max_children = default_options.print_max_children

        self.print_rawString = default_options.print_rawString
        # compress 설정에 따른 후처리
        if not compress_level:
            compress_level = default_options.compress_level
        compress(self, compress_level)

def compress(cls: Options, compress_level):
    if compress_level == 1:
        cls.print_tag = True
        cls.print_terminal_contents = True
        cls.max_print_of_contents = 70

        cls.print_max_children = {"depth_multiplier": 5, "upperbound_constant": 8, "exclude_parent_classes": [dict, Undefined_class]}
    elif compress_level == 2:
        cls.print_tag = True
        cls.print_terminal_contents = True
        cls.max_print_of_contents = 60

        cls.print_max_children = {"depth_multiplier": 3, "upperbound_constant": 5, "exclude_parent_classes": [dict, Undefined_class]}
    elif compress_level == 3:
        cls.print_tag = False
        cls.print_terminal_contents = False
        cls.max_print_of_contents = 50

        cls.print_max_children = {"depth_multiplier": 1, "upperbound_constant": 1, "exclude_parent_classes": [dict, Undefined_class]}

def source2graph(file_path):
    src = Source.from_file(file_path)
    lst = str(src).splitlines()
    HasComment = (lst[0].find('//') != -1)

    IsDirectGraph = True
    skipIndex = 0

    if HasComment:
        skipIndex = 1
        if lst[skipIndex].find('graph {') != -1:
            IsDirectGraph = False
    else:
        if lst[0].find('graph {') != -1:
            IsDirectGraph = False

    if IsDirectGraph:
        g = Digraph()
    else:
        g = Graph()

    g.body.clear()

    s = str()
    for i in range(len(lst)):
        if ((i > skipIndex) and (i != len(lst) - 1)):
            if HasComment:
                g.comment = lst[0].replace('//', '')
            g.body.append(lst[i])
    return g

def to_graphviz(tree:Tree, data_property = "long", file_path = "source.gv") -> Union[Graph, Digraph]:
    for node in tree.all_nodes_itr():
        node.tag = getattr(node.data, data_property)
    tree.to_graphviz(file_path, shape = "plaintext")
    g = source2graph(file_path)
    g.graph_attr['rankdir'] = "LR"
    return g

def type_mapping(dtype):
    for dc in defined_classes:
        if issubclass(dtype, dc):
            dtype = dc
    while dtype in mapping_type2type.keys():
        dtype = mapping_type2type[dtype]
    if dtype not in defined_classes:
        return Undefined_class
    return dtype
def size_mapping(dtype):
    # mapping with subtype equality
    if np.number in mapping_type2size.keys():
        if np.issubdtype(dtype, np.number):
            return mapping_type2size[np.number]
    # mapping with type equality
    if dtype in mapping_type2size.keys():
        size = mapping_type2size[dtype]
    else:
        size = None
    return size

def size(cls):
    dtype = type(cls)
    dtype = type_mapping(dtype)
    size = size_mapping(dtype)
    if size is None:
        if dtype in (ndarray, DataFrame, Tensor):
            size = tuple(cls.shape)
        else:
            if hasattr(cls, "__len__"):
                size = cls.__len__()
            else:
                if dtype == Undefined_class:
                    cls = cls.__dict__
                    size = cls.__len__()
    if isinstance(size, int) :
        size = (size,)

    return size

def size_scalar(size:tuple, options:Options):
    if size == ():
        return 0
    ma = options.main_axis
    if ma == str and ma.lower() == "smallest":
        return min(size)
    else:
        return size[ma]

class Dnode(Node):

    data = namedtuple("data", ["short", "long", "memo"])

    def __init__(self, tag=None, identifier=None, expanded=True, data=data(None,None,None), contents = None, options = None, fold = False, key = None):
        if options is None:
            options = Options()

        if identifier is None:
            identifier = options.id_pool.pop()
        super().__init__(tag, identifier, expanded, data)
        self.options = options
        self.contents = contents
        self.fold = fold
        self.size = size(contents)
        self.dtype = type(contents)
        self.dtype_mapped = type_mapping(self.dtype)
        self.key = key
        self.is_terminal = False
    def __repr__(self):
        name = self.__class__.__name__
        kwargs = [
            "tag={0}".format(self.tag),
            "identifier={0}".format(self.identifier),
            "data.short={0}".format(self.data.short)
        ]

        return "%s(%s)" % (name, ", ".join(kwargs))

def i2j_children(node:Dnode, i, j = None) -> Union[Iterable, Dict]:
    children = None

    if j is None:
        j = i + 1

    cls = node.contents
    dtype = type(cls)
    dtype = type_mapping(dtype)

    if dtype in (ndarray,):
        if node.options.main_axis == "smallest":
            ma = cls.shape.index(min(cls.shape))
        else:
            ma = node.options.main_axis
        children = cls.take(list(range(i, min(j, cls.shape[ma]))), ma)
    elif dtype in (Tensor,):
        # options.main_axis == "smallest" is not implemented for tensor yet
        children = cls[i:j]
    elif dtype in (tuple,):
        children = cls[i:j]
    elif dtype in (dict,):
        children = get_n_items(cls, i, j)
    elif dtype in terminal_classes:
        children = ()
    elif dtype in (Undefined_class,):
        children = get_n_items(cls.__dict__, i, j)
    return children

def get_value_from_key(cls:Union[Dict, DataFrame, Undefined_class], key, namespace = 'either'):
    value = None
    if namespace.lower() == 'either':
        if hasattr(cls, "__getitem__"):
            value = cls.__getitem__(key)
        elif hasattr(cls, "__getattribute__"):
            value = cls.__getattribute__(key)
        else:
            raise Exception(f"both __getitem__ and __getattribute__ for {type(cls)} object is not defined.")
    elif namespace.lower() == "item":
        assert hasattr(cls, "__getitem__"), f"__getitem__ for {type(cls)} object is not defined."
        value = [cls.__getitem__(key)]
    elif namespace.lower() == 'attribute':
        assert hasattr(cls, "getattribute"), f"__getattribute__ for {type(cls)} object is not defined."
    else:
        raise Exception('invalid namespace specified')

    return value

def is_terminal(node:Dnode):
    if node.dtype_mapped in terminal_classes:
        return True
    elif size_scalar(node.size, node.options) == 0:
        return True
    else:
        return False

def update_msg(parent_node:Union[Dnode, None], child_node:Dnode):
    '''
    long : key : type - size
    terminal_node.long : key : contents
    short : key : type - size
    '''
    if parent_node is not None:
        parent_dtype = parent_node.dtype
        parent_dtype_mapped = parent_node.dtype_mapped
        parent_size = parent_node.size

    child_dtype = child_node.dtype
    child_dtype_mapped = child_node.dtype_mapped

    child_size = child_node.size

    long = short = memo = ""

    if child_node.options.print_tag:
        long += str(child_node.tag) + " "
        short += str(child_node.tag) + " "

    if child_node.key:
        long += child_node.key + " : "
    short += struct2msg(child_dtype, child_size) + " "

    if child_node.options.print_terminal_contents and child_node.is_terminal == True:
        long += contents2msg(child_node.contents, child_node.options.max_print_of_contents, child_node.options.print_rawString)
    else:
        long += struct2msg(child_dtype, child_size) + " "

    child_node.data = child_node.data._replace(long = long.strip(), short = short.strip(), memo = memo.strip())

def fold_and_out(tree:Tree, nid):
    if tree.contains(nid):
        tree_repo[nid] = Tree_fold_meta(tree.parent(nid), tree[nid], tree.remove_subtree(nid))
def fold(tree:Tree, nid):
    children = tree.children(nid)
    for childNode in children:
        fold_and_out(tree, childNode.identifier)
def unfold(tree:Tree, nid):
    trp:Tree_fold_meta = tree_repo[nid]
    tree.add_node(trp.child_node, parent = trp.parent_nid)
    tree.merge(nid, trp.child_subtree)

def is_parent_of_terminals(tree:Tree, childNodes:list):
    is_terminals = [childNode.is_terminal for childNode in childNodes]
    if all(is_terminals):
        return True
    else:
        return False

def get_out_children_thres(tree, childNodes, max_children_policy):
    if childNodes is None:
        return 0
    mcp = max_children_policy

    thres = []
    m = mcp.get("depth_multiplier")
    if m:
        depth = tree.depth(childNodes[0])
        m_depth = int(depth*m)

        thres.append(m_depth)
    ub_c = mcp.get("upperbound_constant")
    if ub_c:
        thres.append(ub_c)

    return min(thres)

def generate_tree(root_obj):
    tree = Tree()

    root_node = Dnode(contents=root_obj)

    tree.add_node(root_node)

    stack = [root_node]

    while stack:
        parent_node = stack.pop()
        children = i2j_children(parent_node, 0, parent_node.options.max_children_search_threshold)
        if children is None or len(children) == 0:
            continue
        # Key-Value pair type
        if parent_node.dtype_mapped in (dict, Undefined_class) or parent_node.dtype is DataFrame:
            for child_key in children:
                child_value = get_value_from_key(parent_node.contents, child_key, 'either')
                child_node = Dnode(contents=child_value, key=child_key)
                tree.add_node(child_node, parent=parent_node)
                update_msg(parent_node, child_node)

                if is_terminal(child_node):
                    child_node.is_terminal = True
                else:
                    stack.append(child_node)
        # Others
        else:
            for child in children:
                child_node = Dnode(contents=child)
                tree.add_node(child_node, parent=parent_node)
                update_msg(parent_node, child_node)
                if is_terminal(child_node):
                    child_node.is_terminal = True
                else:
                    stack.append(child_node)
    return tree

def fold_tree(tree):
    parent_node = tree[tree.root]
    stack = [parent_node]
    update_msg(None, parent_node)

    while stack:
        parent_node = stack.pop()
        childNodes = tree.children(parent_node.identifier)

        if childNodes and is_parent_of_terminals(tree, childNodes):
            parent_node.fold = True
            parent_node.is_terminal = True
            pid = parent_node.identifier
            fold(tree, pid)
            update_msg(tree.parent(pid), parent_node)

        elif childNodes:
            pmc = parent_node.options.print_max_children

            if parent_node.dtype_mapped in pmc.get("exclude_parent_classes"):
                out_children = ()
                in_children = childNodes
            else:
                out_children_thres = get_out_children_thres(tree, childNodes, pmc)
                in_children = childNodes[:out_children_thres]
                out_children = childNodes[out_children_thres:]

            for out_child in out_children:
                out_child.fold = True
                fold_and_out(tree, out_child.identifier)
            for in_child in in_children:
                stack.append(in_child)
                update_msg(parent_node, in_child)

if __name__ == "__main__":
    default_options.compress_level = 0
    default_options.max_print_of_contents = 20
    default_options.max_children_search_threshold = 20
    default_options.print_max_children = {"depth_multiplier" : 1, "upperbound_constant" : 5, "exclude_parent_classes" : [dict, Undefined_class]}
    default_options.print_tag = True

    # root_obj = get_example_data("ice")
    # root_obj = get_example_data("woz_data_dir")
    # root_obj = get_example_data("iris")
    root_obj = get_example_data("feature_dataset_example")

    tree = generate_tree(root_obj)
    fold_tree(tree)

    tree.show(data_property = "long")