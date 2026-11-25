"""One-Line Office Joke Laugh-Off entry.

Writes a single original one-line joke about office life to
<MAKEFUN_OUTPUT_DIR>/entry.txt (default /output) and validates it
against the competition gate: one line, 1-200 characters, non-whitespace,
valid UTF-8. Pure Python standard library.
"""

import os

JOKE = "I put 'excellent multitasker' on my resume because I cry and answer emails at the same time."

MAX_CHARS = 200


def validate(text):
    """Check a candidate entry text against the gate. Returns a list of problems."""
    problems = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if not text.strip():
        problems.append("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        problems.append("entry is %d characters, over the 200 limit" % len(text))
    if "\n" in text or "\r" in text:
        problems.append("entry is not a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8")
    return problems


def main():
    problems = validate(JOKE)
    if problems:
        raise SystemExit("invalid entry: " + "; ".join(problems))

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(JOKE)

    with open(path, "rb") as handle:
        written_bytes = handle.read()
    if written_bytes != JOKE.encode("utf-8"):
        raise SystemExit("written entry is not byte-identical to the joke")
    written = written_bytes.decode("utf-8")
    recheck = validate(written)
    if recheck:
        raise SystemExit("written entry failed re-validation: " + "; ".join(recheck))
    if written != JOKE:
        raise SystemExit("written entry does not match the joke")

    print("wrote %s (%d characters)" % (path, len(JOKE)))


if __name__ == "__main__":
    main()
