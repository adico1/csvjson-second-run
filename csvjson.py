"""Convert comma-separated CSV from stdin or a UTF-8 file into JSON."""
import argparse
import csv
import io
import json
from pathlib import Path
import sys


def convert(text):
    rows = csv.reader(io.StringIO(text, newline=""), strict=True)
    headers = next(rows, None)
    if headers is None:
        return []
    if not headers or any(not name.strip() for name in headers):
        raise ValueError("CSV headers must be nonempty")
    if len(headers) != len(set(headers)):
        raise ValueError("CSV headers must be unique")
    result = []
    for row in rows:
        if not row:
            continue
        if len(row) != len(headers):
            raise ValueError(f"CSV row ending at line {rows.line_num} has {len(row)} fields; expected {len(headers)}")
        result.append(dict(zip(headers, row)))
    return result


def main():
    parser = argparse.ArgumentParser(description="Convert CSV to a JSON array")
    parser.add_argument("file", nargs="?", help="UTF-8 CSV file; omit to read stdin")
    args = parser.parse_args()
    try:
        if args.file:
            with Path(args.file).open(encoding="utf-8", newline="") as source:
                text = source.read()
        else:
            text = sys.stdin.read()
        result = convert(text)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"csvjson: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
