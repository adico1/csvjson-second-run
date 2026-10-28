"""Regression tests for the factory-delivered delimiter feature."""
import csv
import io
import json
from pathlib import Path
import string
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'csvjson.py'


class DelimiterTests(unittest.TestCase):
    def cli(self, text, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], input=text,
                              text=True, capture_output=True, timeout=5)

    def test_every_allowed_punctuation_delimiter(self):
        for delimiter in string.punctuation.replace('"', ''):
            with self.subTest(delimiter=delimiter):
                stream = io.StringIO(newline='')
                rows = [['name', 'note'], ['שלום', f'007{delimiter}"quoted"\nnext']]
                csv.writer(stream, delimiter=delimiter, lineterminator='\n').writerows(rows)
                result = self.cli(stream.getvalue(), '--delimiter=' + delimiter)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                self.assertEqual(json.loads(result.stdout), [dict(zip(rows[0], rows[1]))])

    def test_invalid_categories_are_rejected_even_on_empty_input(self):
        allowed = set(string.punctuation) - {'"'}
        invalid = [chr(n) for n in range(1, 128) if chr(n) not in allowed]
        invalid += ['', ';;', 'é', '；', 'Ω', '中', '😀', '\u00a0', '\u2003']
        for delimiter in invalid:
            with self.subTest(delimiter=delimiter):
                result = self.cli('', '--delimiter=' + delimiter)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertIn('delimiter', result.stderr)

    def test_file_input_and_both_option_positions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.csv'
            for delimiter in (';', '|'):
                path.write_text(f'name{delimiter}count\nAda{delimiter}007\n', encoding='utf-8')
                for args in (['--delimiter', delimiter, str(path)], [str(path), '--delimiter', delimiter]):
                    with self.subTest(args=args):
                        result = self.cli('', *args)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(result.stderr, '')
                        self.assertEqual(json.loads(result.stdout), [{'name': 'Ada', 'count': '007'}])


if __name__ == '__main__':
    unittest.main()
