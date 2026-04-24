# stampbarcode
Duplicate a PDF with serial barcode stamps

## Installation

```bash
pipx install .
```

## Usage

```bash
stampbarcode [--start N] [--num N] file.pdf
```

This produces files named `<stem>-<code>.pdf` in the same directory as `file.pdf`.
Each output file is a stamped copy using a Code39 barcode (with the number shown
as human-readable text), and the barcode is placed on the inside edge of each page:
left for recto pages and right for verso pages.

The first generated barcode is exactly `--start`, and `--num` controls how many
consecutive codes are produced.
