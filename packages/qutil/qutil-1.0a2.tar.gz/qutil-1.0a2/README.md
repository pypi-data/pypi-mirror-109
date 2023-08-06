# qutil

qutil is a simple library to test and execute SQL scripts from python

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install qutil.

```bash
pip install qutil
```

# Local Build

### Compile
```bash
#file build on /build 
python setup.py sdist 

#.tar.gz build on /dist
python setup.py sdist bdist_wheel
```

### Install
```bash
pip install dist/qutil-[version].tar.gz 
```
<!-- 
### Upload (Dev) 
```bash
twine upload dist/*
```
 -->

