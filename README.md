# CSVJSON

A Python 3.10+ CLI that converts CSV into a JSON array. Uses only the Python
standard library; no installation or API keys are needed.

```sh
python3 csvjson.py examples/people.csv
python3 csvjson.py examples/people-semicolon.csv --delimiter ';'
printf 'name|count\nAda|007\n' | python3 csvjson.py --delimiter '|'
python3 -m unittest discover -s tests -v
```

Input comes from a UTF-8 file or stdin. Comma is the default delimiter.
`--delimiter CHARACTER` may appear before or after the file argument. The delimiter
must be one printable ASCII punctuation character other than a double quote.
For punctuation that might be interpreted as an option, use `--delimiter=-`.

The first row supplies unique, nonblank field names. Values remain strings;
quoted delimiters, escaped quotes, multiline values and Unicode are supported.
Empty input or a header-only file produces `[]`. Blank data rows are ignored.
Invalid delimiters, invalid headers, mismatched field counts, malformed quotes
and unreadable files produce a message on stderr and exit code 2, without partial
JSON on stdout. Successful output is one JSON line followed by a newline, with
exit code 0. Default comma-separated behavior is preserved.

## Factory provenance

The delimiter feature was delivered by CrewAI run `4c1927a4ae2a` and promoted
byte-for-byte from its verified local artifact after three fresh trials completed:
`4c1927a4ae2a`, `9bf99ee9cc81`, and `5e9f8473078c`.
Each trial started from baseline `c43bfa62a1f2d28a10cf00e3f31987a4c5547b8f`,
passed 259 independent CLI scenarios and nine original tests against both candidate
and installed copies, and required no manual candidate repairs or operator retries.
Existing approval gates were reviewed by Codex under user authorization.

`tasks/add-delimiter.txt` is retained as the original completed task specification.
The repository now includes the original nine test methods plus three delimiter
regression methods covering every permitted punctuation character, invalid ASCII
categories, representative Unicode values, and file/option placement.

These three successful repetitions are evidence for this task and configuration,
not a general reliability guarantee for arbitrary projects. Delivery and promotion
are local; no public release or hosted service was created.
