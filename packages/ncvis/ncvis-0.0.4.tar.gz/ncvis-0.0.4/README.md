[![PyPI](https://img.shields.io/pypi/v/ncvis.svg)](https://pypi.python.org/pypi/ncvis/)
![GitHub](https://img.shields.io/github/license/alartum/ncvis.svg)
# ncvis

ncvis is a Python module for data visualization written in C++ with parallelism support.

# Installation

Install **numpy** and **cython** packages:
```bash
pip install numpy cython
```

Install **ncvis** package:
```bash
pip install ncvis
```

# Usage

Import the module and use it as you would use any of **sklearn** models:
```python
import ncvis

vis = ncvis.NCVis()
Y = vis.fit(X)
```