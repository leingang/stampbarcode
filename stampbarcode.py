#!/usr/bin/env python3

from __future__ import annotations

import io
from pathlib import Path

import typer

BARCODE_BAR_WIDTH = 0.6
BARCODE_BAR_HEIGHT = 18
BARCODE_MARGIN = 18

app = typer.Typer(add_completion=False)


def generate_codes(start: int, num: int) -> range:
    return range(start, start + num)


def output_path_for(input_path: Path, code: int) -> Path:
    return input_path.with_name(f"{input_path.stem}-{code}.pdf")


def create_overlay(page_width: float, page_height: float, code: int, page_number: int) -> io.BytesIO:
    from reportlab.graphics.barcode import code39
    from reportlab.pdfgen import canvas

    packet = io.BytesIO()
    pdf_canvas = canvas.Canvas(packet, pagesize=(page_width, page_height))
    barcode = code39.Standard39(
        str(code),
        barWidth=BARCODE_BAR_WIDTH,
        barHeight=BARCODE_BAR_HEIGHT,
        stop=1,
        humanReadable=True,
    )

    is_recto = page_number % 2 == 1
    pdf_canvas.saveState()
    if is_recto:
        # Counterclockwise (+90°): barcode runs vertically on the left (recto) edge.
        # After translate(tx,ty) + rotate(90), local (x,y) maps to page (tx-y, ty+x).
        # Barcode occupies page_x in [tx-H, tx], page_y in [ty, ty+W].
        tx = BARCODE_MARGIN + barcode.height
        ty = (page_height - barcode.width) / 2
        pdf_canvas.translate(tx, ty)
        pdf_canvas.rotate(90)
    else:
        # Clockwise (-90°): barcode runs vertically on the right (verso) edge.
        # After translate(tx,ty) + rotate(-90), local (x,y) maps to page (tx+y, ty-x).
        # Barcode occupies page_x in [tx, tx+H], page_y in [ty-W, ty].
        tx = page_width - BARCODE_MARGIN - barcode.height
        ty = (page_height + barcode.width) / 2
        pdf_canvas.translate(tx, ty)
        pdf_canvas.rotate(-90)
    barcode.drawOn(pdf_canvas, 0, 0)
    pdf_canvas.restoreState()

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


def run(pdf_file: Path, start: int, num: int) -> None:
    if not pdf_file.exists():
        raise FileNotFoundError(f"Input file does not exist: {pdf_file}")

    for code in generate_codes(start, num):
        output_pdf = output_path_for(pdf_file, code)
        stamp_pdf(pdf_file, output_pdf, code)


@app.command()
def main(
    pdf_file: Path = typer.Argument(..., help="Source PDF file"),
    start: int = typer.Option(0, "--start", help="Starting barcode number"),
    num: int = typer.Option(1, "--num", min=1, help="How many stamped files to produce"),
) -> None:
    run(pdf_file, start, num)


if __name__ == "__main__":
    app()
