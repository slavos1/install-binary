# Notes

Install binary from GitHub to `~/.local/bin`.

The binaries can be packaged either in a [tarball](https://github.com/starship/starship/releases) or as a [direct binary](https://github.com/direnv/direnv/releases).

See also [ARCHITECTURE.md](ARCHITECTURE.md).

## Prerequisites

* [`hatch`](https://hatch.pypa.io/) -- install via `pipx hatch` or `pip install --user hatch`

## How to use

```console
# to install via pipx locally
make deploy
```

## Develop

```console
make fmt
hatch run test
make help
make mypy
hatch run cli
```
