# blast

Usage:

```bash
blast dump gamma0 \
    | blast dump bit 3 \
    | blast analysis individualized
```

## Development

Requires:

- Docker
- [Poetry](https://python-poetry.org/)

Technologies:

- Python
- Docker
- [Poetry](https://python-poetry.org/)

## Build

To build a Docker image tagged `blast:${version}` (where `${version}` is defined by `pyproject.toml`) run the following;

```bash
./app.sh build
```

## Run

```bash
./app.sh run <args>
```
