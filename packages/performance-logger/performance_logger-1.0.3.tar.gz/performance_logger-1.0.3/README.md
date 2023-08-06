# performance_logger

## Table of Contents
  * [Installation](#installation)
  * [Quick start](#quick-start)
  * [Features](#features)
  
## Installation

Download using pip via pypi.

```bash
$ pip install performance-logger --upgrade
```
(Mac/homebrew users may need to use ``pip3``)


## Quick start
```python
from performance_logger.main import perf_logger

@perf_logger('datetime')
def test_fun():
    return "it will log the time performance of test_fun using datetime format"

@perf_logger('ns')
def test_fun2():
    return "it will log the time performance of test_fun2 using nano seconds"
```

## Features
  * Simple decorator functions for performance checking of functions
  * You can use parameter to choose logged performace format