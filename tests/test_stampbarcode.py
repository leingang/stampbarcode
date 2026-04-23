from pathlib import Path
import unittest

import stampbarcode


class StampBarcodeTests(unittest.TestCase):
    def test_generate_codes_increments_from_start(self) -> None:
        self.assertEqual(list(stampbarcode.generate_codes(100, 5)), [101, 102, 103, 104, 105])

    def test_output_path_for_uses_stem_and_code(self) -> None:
        source = Path("/tmp/document.pdf")
        self.assertEqual(
            stampbarcode.output_path_for(source, 123),
            Path("/tmp/document-123.pdf"),
        )

    def test_barcode_x_position_inside_edge(self) -> None:
        page_width = 500
        barcode_width = 100
        margin = 20
        self.assertEqual(stampbarcode.barcode_x_position(page_width, barcode_width, margin, 1), 20)
        self.assertEqual(stampbarcode.barcode_x_position(page_width, barcode_width, margin, 2), 380)

    def test_parse_args_rejects_non_positive_num(self) -> None:
        with self.assertRaises(SystemExit):
            stampbarcode.parse_args(["--num", "0", "input.pdf"])

    def test_run_raises_when_input_missing(self) -> None:
        args = stampbarcode.argparse.Namespace(pdf_file=Path("does-not-exist.pdf"), start=0, num=1)
        with self.assertRaises(FileNotFoundError):
            stampbarcode.run(args)


if __name__ == "__main__":
    unittest.main()
