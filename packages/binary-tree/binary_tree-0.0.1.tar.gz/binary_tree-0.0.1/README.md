<div style="text-align:center"><span> <h1>Binary_tree</h1></span></div>

---

Binary_tree is a simple package to create sort and search data with binary trees.

##install

---

```
pip install --upgrade binary_tree
```

## usage

---

-   To create a tree use the tree object
-   Get a sorted array using the tree traverse function
-   Search an item (True/False) via the tree search function

####example

```python
import binary_tree as bt
tree1 = bt.tree([1, 6, 3, 9])
print(tree1.traverse())

# returns [1, 3, 6, 9]
print(tree1.search(6))

#returns True
```

#####credits
**Creator**: Ofri Kirshen
