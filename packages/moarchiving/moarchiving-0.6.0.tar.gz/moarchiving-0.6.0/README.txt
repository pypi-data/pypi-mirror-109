
# Introduction

The [Python](https://www.python.org/) `class` `moarchiving.BiobjectiveNondominatedSortedList` implements a bi-objective non-dominated archive with `list` as parent class. It is heavily based on the [`bisect`](https://docs.python.org/3/library/bisect.html) module. It provides easy and fast access to the overall hypervolume, the contributing hypervolume of each element, and to the [uncrowded hypervolume improvement](https://arxiv.org/abs/1904.08823/) of any given point in objective space.

## Installation

Either simply via

```
pip install moarchiving
```

or from [GitHub](https://github.com/CMA-ES/moarchiving/) via

```
pip install git+https://github.com/CMA-ES/moarchiving.git@master
```

The single file [`moarchiving.py`](https://github.com/CMA-ES/moarchiving/moarchiving/moarchiving.py) (from the `moarchiving/` folder) can also be directly used by itself when copied in the current folder or in a path visible to Python (e.g. a path contained in `sys.path`).

