# Acme Inspect

Inspect a local data file and print a concise report.

## Prerequisites

Python 3.11 or newer.

## Installation

```sh
python -m pip install acme-inspect
```

## Usage

```sh
acme-inspect data.json
```

Use `acme-inspect --help` to list options.

## Configuration

The `ACME_INSPECT_FORMAT` environment variable selects the output format.

## Quick start

```sh
printf '{"ok": true}\n' > data.json
acme-inspect data.json
```

The command exits successfully and prints a report.
