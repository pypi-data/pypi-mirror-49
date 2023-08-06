# entry-logger-sanic
![PyPI](https://img.shields.io/pypi/v/entry-logger-sanic.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/entry-logger-sanic.svg)

A logger for Sanic based EntryDSM service

## Install
```bash
pip install entry-logger-sanic
```

## Feature
- Request logging
- System logging
- File saving in NDJSON format

## Usage
```python
from sanic import Sanic
from entry_logger_sanic import set_logger

app = Sanic("SERVICE NAME")  # please specify service name!
set_logger(app)

...
```

## Versioning
```
{Major}.{Minor}.{Patch}
```
ex: 0.2.3

- Major: without subcompatibility
- Minor: with partial subcompatibility
- Patch: with full subcompatibility

## Maintainer

- Seonghyeon Kim - [NovemberOscar](https://github.com/NovemberOscar)