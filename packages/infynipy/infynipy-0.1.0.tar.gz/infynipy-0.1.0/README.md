# Infynipy

[![Documentation Status](https://readthedocs.org/projects/infynipy/badge/?version=latest)](https://infynipy.readthedocs.io/en/latest/?badge=latest)

An API wrapper for the [Infynity][] mortgage broker system.

[Infynity]: https://api.infynity.com.au/v1/doc#!index.md

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
