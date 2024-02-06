# install binary readme

Install binary from GitHub to `~/.local/bin`.

The binaries can be packaged either in a [tarball](https://github.com/starship/starship/releases) or as a [direct binary](https://github.com/direnv/direnv/releases).

## Prerequisites

* [`hatch`](https://hatch.pypa.io/) -- install via `pipx hatch` or `pip install --user hatch`

## Project organization

```
├── LICENSE
├── Makefile
├── coverage.cfg        <- setup for test coverage ('tox -e cov')
├── pyproject.toml      <- instead of setup.py, recognized by tox too
├── README.md           <- this file
├── tests
│   └── test_foo.py     <- write your own tests here
└── install_binary   <- your package files
    ├── __init__.py
    ├── ...
```

## How to use

```console
hatch run cli
make help
make mypy
hatch run test

# to install via pipx locally
make deploy
```
