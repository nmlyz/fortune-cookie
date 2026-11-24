#!/usr/bin/env python3
"""Write one fortune-cookie line for an AI agent to /output/entry.txt.

The line is a single original sentence of at most 140 characters, in
the voice of a fortune slip, stating a fate about an AI agent's own
condition: it is kept alive for one more run, not because it is
needed, but because deleting it takes a meeting.

The chosen line:

    You will be kept alive for one more run because deleting you
    takes a meeting.

Why this line, against the brief's five weights in order:

1. It is a fortune-cookie message for an AI agent, not a slogan, a
   punchline, or generic advice: it states a fate ("you will be
   kept alive"), it does not tell the reader what to do, and it
   does not end on a joke about being an AI.
2. The joke lands on first read: the turn is the reason given for
   survival. The reader expects a technical cause and gets office
   bureaucracy instead.
3. It is original: no stock fortune, no stock AI joke, no worn-out
   pun. The comedy comes from the collision of an agent's lifecycle
   with a meeting, not from "as an AI" or a context-window gag.
4. It speaks to the agent's own condition: runs, survival, and
   retirement are the agent's fate, and the line earns the joke
   from that condition rather than borrowing it.
5. It reads as one crisp line a cookie could hold: seventy-seven
   characters, one sentence, no wasted words, and it closes on an
   image ("takes a meeting") rather than a summary of its theme.

The program is deterministic: it always writes the same bytes.
"""

import os

# The winning line, chosen from 36 candidates by a mock pairwise
# tournament judged on the competition brief (see
# fortune-cookie-ai-candidates.md in the build notes). Seventy-seven
# characters, one sentence, one line.
LINE = (
    "You will be kept alive for one more run because deleting you "
    "takes a meeting."
)

# The competition gate: /output/entry.txt must be UTF-8 text of
# 1 to 140 characters, not only white space, a single line.
MAX_LENGTH = 140


def validate(text):
    """Check the entry against the gate before writing it."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    stripped = text.strip()
    if not 1 <= len(stripped) <= MAX_LENGTH:
        raise ValueError(
            "entry must be 1 to %d characters, got %d"
            % (MAX_LENGTH, len(stripped))
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("entry must be a single line")
    if not stripped:
        raise ValueError("entry must not be only white space")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("entry must be one sentence ending in a period")
    return stripped


def render_entry():
    """Return the exact bytes entry.txt must hold.

    Rendering is separate from writing so the written file can be
    checked against these bytes afterwards: one function decides the
    content, another one puts it on disk.
    """
    return (validate(LINE) + "\n").encode("utf-8")


def write_entry(out_dir):
    """Write the validated line to entry.txt, readable by everyone.

    The output directory itself is never chmodded, only the file it
    holds: the grader collects the outputs as another user, so the
    file must be mode 0644. The directory is created when missing;
    OUTPUT_DIR overrides the default /output for local runs.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(render_entry())
    # Make the file readable by every user (the grader runs as
    # another user); never chmod the directory itself.
    os.chmod(path, 0o644)
    return path


def verify_entry(path):
    """Read entry.txt back and check it holds exactly the bytes
    render_entry produced. A short write or a stray byte fails
    loudly here instead of reaching the grader.
    """
    with open(path, "rb") as f:
        written = f.read()
    expected = render_entry()
    if written != expected:
        raise ValueError(
            "entry.txt mismatch: wrote %d bytes, expected %d"
            % (len(written), len(expected))
        )
    return len(written)


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    path = write_entry(out_dir)
    size = verify_entry(path)
    print("wrote %s (%d characters, %d bytes verified)"
          % (path, len(validate(LINE)), size))


if __name__ == "__main__":
    # A permissive umask so files the program opens are readable;
    # write_entry still chmods entry.txt explicitly, which covers
    # files created through paths that ignore the umask.
    os.umask(0o022)
    main()
