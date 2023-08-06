[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![boggle_test Actions Status](https://github.com/euanacampbell/boggle_solver/workflows/boggle_test/badge.svg)](https://github.com/euanacampbell/boggle_solver/actions)

A recursive method for finding all words in a given square grid.

## Installation

```bash
>> pip3 install boggle-solver
```

```python
from boggle_solver.grid import Grid
```

## Usage
Create a 2-dimensional array and pass this into the package.

```python
grid = [
            ['M','A','P'],
            ['E','T','E'],
            ['D','E','N'],
     ]

grid=Grid(grid)
```

To confirm this worked, the below function can be used.

```python
grid.print_grid()
```

Now you can search for all words. This will take ~10 seconds for a 3x3 grid.

```python
grid.find_all_words()
```
