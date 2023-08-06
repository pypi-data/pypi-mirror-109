# Task

Create a hierarchical structure that has main and children and each has a count value. Call a function that flattens the structure and returns the structure back from the array. Create a library for this structure.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation Guide

git clone "url to current repository"<br/>
virtualenv venv<br/>
venv activate<br/>
pip install git+"url to current repository"

### Usage

```python
from solution.transposition import Transposition

# structure example
structure = {
    "name": "main",
    "children": {
        "first": {
            "count": 1,
            "children": {
                "third": {
                   "count": 3
                }
            }
        },
        "second": {
            "count": 2
        },
    }
}

# object initialization
tp = Transposition()

# transposition to flat array
flat_array = tp.struct_to_array(structure)

# back to structure
new_structure = tp.array_to_struct(flat_array)


```

### Tests

pip install pytest<br/>
pytest tests/test.py
