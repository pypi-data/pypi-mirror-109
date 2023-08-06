# Introduction

actl is a command line application engine for Python, it provides an utility and library for the development of modular command line applications.

##  Features

- [x] Automatic load of [Click] commands «from *commands/\*.py*»
- [x] Verbosity level control with *-vv...* for the *verbose()* function

[click]: https://click.palletsprojects.com/


## Installation

actl is avaiable from the official Python Package Index (PIP), you can install it from the terminal:
```bash
pip install actl
```

##  Hello World
main.py
```python
import actl

actl.main(__name__, __file__)
```

_commands/hello.py_
```python
import click
from actl import verbose


@click.command()
def hello():
        verbose("Running in verbose")
        print("Hello")
```

Test the app:
```sh
python main.py
python main.py hello
python main.py -v hello
```
