# IPython Namespaces

Extension for IPython/Jupyter Notebooks that adds namespaces that you can enter and re-enter.

## Usage (in a Jupyter Notebook)

Load the extension:

```python
%load_ext ipython-namespaces
```

Use the `space` cell magic:

```
foo = 23
```

```
%%space dustin

bar = 42
foo, bar
```

`(23, 42)`

```
foo, bar
```

`NameError: name 'bar' is not defined`

```
%%space dustin

foo, bar
```

`(23, 42)`

```
from ipython_namespaces import Namespaces

Namespaces.dustin['bar']
```

`42`

## Features

1. Separate namespaces within one Jupyter Notebook
2. Access to other namespaces via the `Namespaces` class
3. Unchanged behavior of `display` – the value of the last line in a cell is displayed
4. Unchanged behavior of tracebacks – the problematic line in one’s own code is highlighted

## Acknowledgements

Thanks to Davide Sarra and the Jupyter Spaces extension for the inspiration!