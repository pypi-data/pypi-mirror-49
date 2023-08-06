hello package example

deployment:
```
rm -rf dist
python3 setup.py sdist
twine upload dist/*
```

local installation:
```
pip uninstall preved && python3 setup.py install
```
