# Git Toolbox

A library and tools for working with git.

## Tools

* *git-heatmap*: Get a heatmap of which source file and which test files are changed together.


## Contributors Guide
### Testing

Testing is done via `pytest`.

To run the test with code coverage:

```
$ pip install -r requirements.txt
$ pytest --cov=src --cov-report=html
```

This will generate an html coverage report in `htmlcov/` directory.
