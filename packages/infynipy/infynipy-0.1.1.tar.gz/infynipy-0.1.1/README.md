# Infynipy

[![PyPI](https://img.shields.io/pypi/v/infynipy.svg)](https://pypi.org/project/infynipy/)
[![Documentation Status](https://readthedocs.org/projects/infynipy/badge/?version=latest)](https://infynipy.readthedocs.io/en/latest/?badge=latest)

An API wrapper for the [Infynity][] mortgage broker system.

[Infynity]: https://api.infynity.com.au/v1/doc#!index.md

Infynipy currently supports the following endpoints:

* Client Accounts
* Financials
* Referrer and Referrer Groups

# Getting Started

Install using pip:

```
pip install infynipy
```

Basic usage:

```python
from infynipy import Infynity

client = Infynity("USERNAME", "API_KEY")
print(client.broker(10).individuals)  # Returns an array of Individual models

# To turn them into dictionaries
for individual in client.broker(10).individuals:
    print(individual.to_dict())
```

View the rest of the [documentation here.][]

[documentation here.]: https://infynipy.readthedocs.io

## Development

Clone from GitHub and run the tests:

```
git clone https://github.com/beanpuppy/infynipy.git
cd infynipy
```

Run the tests and linter:
```
tox
```

## License

MIT
