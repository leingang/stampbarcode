# stampbarcode
Duplicate a PDF with serial barcode stamps

## Installation

```bash
pipx install .
```

## Development

Use the repo-local virtual environment for tests and editable installs:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -q
```

## Usage

```bash
stampbarcode [--start N] [--number N] [--position inside|outside|left|right|top|bottom] file.pdf
```

This produces files named `<stem>-<code>.pdf` in the same directory as `file.pdf`.
Each output file is a stamped copy using a Code39 barcode (with the number shown
as human-readable text), and `--position` controls where the barcode is placed.
The default is `inside`: left on recto pages and right on verso pages.

Other position modes are `outside`, `left`, `right`, `top`, and `bottom`.

The first generated barcode is exactly `--start`, and `--number` controls how many
consecutive codes are produced.
