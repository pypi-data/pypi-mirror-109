# Lzip

A simple Python library to decode lzip files chunk by chunk.

```sh
pip install lzip
```

## Publish

1. Bump the version number in *setup.py*.

2. Install Cubuzoa in a different directory (https://github.com/neuromorphicsystems/cubuzoa) to build pre-compiled versions for all major operating systems. Cubuzoa depends on VirtualBox (with its extension pack) and requires about 75 GB of free disk space.
```
cd cubuzoa
python3 cubuzoa.py provision
python3 cubuzoa.py build /path/to/event_stream
```

3. Install twine
```
pip3 install twine
```

4. Upload the compiled wheels and the source code to PyPI:
```
python3 setup.py sdist --dist-dir wheels
python3 -m twine upload wheels/*
```
