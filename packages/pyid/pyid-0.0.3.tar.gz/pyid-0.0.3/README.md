# PyID
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

Turn any python object into an exactly equivalent object with an `id` attribute.

## Example

```python
import random
import pyid


mylist = [random.sample(range(10), k=3) for i in range(20)]


# Uses python uuid module to assign ID by default
mylist = [pyid.idfy(item) for item in mylist]
for item in mylist:
    print(item, item.id)


# Assign a custom ID
mylist = [pyid.idfy(item, 'myid') for item in mylist]
for item in mylist:
    print(item, item.id)
```

## Installation

```bash
pip install pyid
```

## Motivation

When referencing related objects, we use unique IDs. In python, we might handle this pattern with a dictionary mapping IDs to objects, or use an item's position in a list as its ID. Either case requires we create variables separate from the object to represent those IDs, and that each time we iterate we explicitly include the ID by iterating with the ID dict or the enumerate function for lists. I built this to test the idea that having an ID attribute is easier and cleaner.

## How it works

It takes the `type` of the passed object, creates a subclass of that type, with an ID attribute, and copies the data from the passed object into an instance that new subclass. If a custom ID is not passed, the python uuid module is used to assign one.