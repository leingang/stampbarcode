from pathlib import Path
import unittest

import stampbarcode
from typer.testing import CliRunner


class StampBarcodeTests(unittest.TestCase):
    runner = CliRunner()

    def test_generate_codes_increments_from_start(self) -> None:
        self.assertEqual(list(stampbarcode.generate_codes(100, 5)), [100, 101, 102, 103, 104])

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

    def test_cli_rejects_non_positive_num(self) -> None:
        result = self.runner.invoke(stampbarcode.app, ["--num", "0", "input.pdf"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value for", result.output)

    def test_run_raises_when_input_missing(self) -> None:
        with self.assertRaises(FileNotFoundError):
            stampbarcode.run(Path("does-not-exist.pdf"), 0, 1)


if __name__ == "__main__":
    unittest.main()
