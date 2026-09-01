# Acme Parse

Parse small text documents with a predictable Python API.

## Prerequisites

Python 3.11 or newer.

## Installation

```sh
python -m pip install acme-parse
```

## Quick start

```python
import acme_parse

document = acme_parse.parse("hello")
print(document.text)
```

The command prints `hello`.

## Usage

See the [API reference](docs/api.md) for parser options.

## Development

Run `python -m unittest` from the repository root.

## License

See [LICENSE](LICENSE).
