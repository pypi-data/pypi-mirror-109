# Introduction

actl is a command line application engine for Python, it provides an utility and library for the development of modular command line applications.

##  Features

- [x] 2 lines of code for the `main` function
- [x] Uses [Click] for modular command line definitions
- [x] Automatic loaded command modules «from *commands/\*.py*»

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


@click.command()
def hello():
    print("Hello")
```

Test the app:
```sh
python main.py
```
