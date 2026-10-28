"""Convert comma-separated CSV from stdin or a UTF-8 file into JSON."""
import argparse
import csv
import io
import json
from pathlib import Path
import sys
import string

# Allowed delimiters: single printable ASCII punctuation character, excluding double quote
_ALLOWED_DELIMITERS = set(string.punctuation) - {'"'}


def validate_delimiter(value):
    if not isinstance(value, str) or len(value) != 1:
        raise argparse.ArgumentTypeError(
            "--delimiter must be a single printable ASCII punctuation character (except double quote)")
    if value not in _ALLOWED_DELIMITERS:
        raise argparse.ArgumentTypeError(
            "--delimiter must be a single printable ASCII punctuation character (except double quote)")
    # Only allow ASCII
    if ord(value) < 33 or ord(value) > 126:
        raise argparse.ArgumentTypeError(
            "--delimiter must be a single printable ASCII punctuation character (except double quote)")
    return value


def convert(text, delimiter=','):
    rows = csv.reader(io.StringIO(text, newline=""), strict=True, delimiter=delimiter)
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
    parser.add_argument(
        "--delimiter",
        metavar="CHARACTER",
        type=validate_delimiter,
        default=",",
        help="Single printable ASCII punctuation character (except double quote) to use as delimiter (default: ',')"
    )
    args = parser.parse_args()
    try:
        if args.file:
            with Path(args.file).open(encoding="utf-8", newline="") as source:
                text = source.read()
        else:
            text = sys.stdin.read()
        result = convert(text, delimiter=args.delimiter)
    except argparse.ArgumentTypeError as exc:
        print(f"csvjson: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"csvjson: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
