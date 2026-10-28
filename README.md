# CSVJSON — second factory project

A small Python 3.10+ CLI that converts comma-separated CSV into a JSON array.
Uses only the Python standard library. No installation or API keys are needed.

```sh
python3 csvjson.py examples/people.csv
printf 'name,count\nAda,007\n' | python3 csvjson.py
python3 -m unittest discover -s tests -v
```

The first row supplies unique, nonblank field names. Values remain strings;
quoted commas, escaped quotes, multiline values and Unicode are supported.
Empty input or a header-only file produces `[]`. Blank data rows are ignored.
Invalid headers, mismatched field counts, malformed quotes and unreadable files
produce a message on stderr and exit code 2, without partial JSON on stdout.
Successful output is one JSON line followed by a newline, with exit code 0.

## First factory task

See `tasks/add-delimiter.txt`. The baseline intentionally supports commas only;
the factory will add an optional `--delimiter` flag. This is an unimplemented
feature, not a deliberately broken baseline.

Before executing that task, configure project-specific independent acceptance
checks and local ZIP/install/observation adapters in the factory repository.
Keep those checks outside the candidate worktree. Existing tests must remain
green; the new checks must fail on this baseline and pass on the delivered CLI.
No public hosting or network service is part of this task.
