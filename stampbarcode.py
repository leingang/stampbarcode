#!/usr/bin/env python3

from __future__ import annotations

import argparse
import io
from pathlib import Path
from typing import Iterable, Sequence


def generate_codes(start: int, num: int) -> Iterable[int]:
    return range(start + 1, start + num + 1)


def output_path_for(input_path: Path, code: int) -> Path:
    return input_path.with_name(f"{input_path.stem}-{code}.pdf")


def barcode_x_position(page_width: float, barcode_width: float, margin: float, page_number: int) -> float:
    is_recto = page_number % 2 == 1
    if is_recto:
        return margin
    return page_width - barcode_width - margin


def create_overlay(page_width: float, page_height: float, code: int, page_number: int) -> io.BytesIO:
    from reportlab.graphics.barcode import code39
    from reportlab.pdfgen import canvas

    packet = io.BytesIO()
    pdf_canvas = canvas.Canvas(packet, pagesize=(page_width, page_height))
    barcode = code39.Standard39(str(code), barWidth=0.6, barHeight=18, stop=1, humanReadable=True)

    margin = 18
    x = barcode_x_position(page_width, barcode.width, margin, page_number)
    y = max((page_height - barcode.height) / 2.0, margin)
    barcode.drawOn(pdf_canvas, x, y)

    pdf_canvas.save()
    packet.seek(0)
    return packet


def stamp_pdf(input_pdf: Path, output_pdf: Path, code: int) -> None:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    for page_number, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        overlay_stream = create_overlay(width, height, code, page_number)
        overlay_page = PdfReader(overlay_stream).pages[0]
        page.merge_page(overlay_page)
        writer.add_page(page)

    with output_pdf.open("wb") as output_stream:
        writer.write(output_stream)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="stampbarcode")
    parser.add_argument("pdf_file", type=Path, help="Source PDF file")
    parser.add_argument("--start", type=int, default=0, help="Starting barcode number")
    parser.add_argument("--num", type=int, default=1, help="How many stamped files to produce")
    args = parser.parse_args(argv)

    if args.num < 1:
        parser.error("--num must be greater than 0")
    return args


def run(args: argparse.Namespace) -> None:
    if not args.pdf_file.exists():
        raise FileNotFoundError(f"Input file does not exist: {args.pdf_file}")

    for code in generate_codes(args.start, args.num):
        output_pdf = output_path_for(args.pdf_file, code)
        stamp_pdf(args.pdf_file, output_pdf, code)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
