# print_hello
- This is simple python package to demonstrate how to upload package to PyPl
## file structure 
```
print_hello/
|-- LICENSE.txt
|-- README.md
|-- print_hello_hanlin
|   |-- __init__.py
|   |-- __pycache__
|   |   |-- __init__.cpython-36.pyc
|   |   `-- print_hello.cpython-36.pyc
|   `-- print_hello.py
`-- setup.py
```
## build package
```bash
$: python3 setup.py  sdist bdist_wheel
 
```
## upload package to pypi.org
```bash
$: python3  -m twine upload  dist/*
 
```
