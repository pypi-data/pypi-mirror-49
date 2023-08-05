# Jupyter Source Magic

A Jupyter Notebook %%magic to quickly edit and run source code.

- Both saves and evaluates source code when cell is run
- Accepts and evaluates other cell magic annotations, without saving them
- Deals with existing files and monitors external changes

Disclaimer
----------

This is an experimental project. Use at your own risk.

Usage
------

Load extension inside a Jupyter notebook:

```
%load_ext jupytersourcemagic
```

Add code with Cell magic:

```
%%source path/to/source.py
# code to run
```

Run to save and evaluate.

Examples
--------

Save and run a script:

```
%%source path/to/source.py
print('hello')
```

Load an existing source to edit.

```
%loadsource path/to/source.py
## when run, cell contents will be replaced with path/to/source.py
```

Handle other cell magic annotations:

```
%%source path/to/source.sh
%%bash
echo 'hello'
```

Help
-----

Display usage and configuration options:

```
%%source?
```

Installation
------------

Install and activate dependencies:

- [ipywidgets](https://github.com/jupyter-widgets/ipywidgets)
- [jupyter-interval-widget](https://github.com/srizzo/jupyter-interval-widget)

Then:

    $ pip install jupyter-source-magic
