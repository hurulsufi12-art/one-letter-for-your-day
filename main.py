"""One Letter for Your Day — entry program.

Writes exactly one letter, A to Z, to /output/entry.txt: the letter
standing for the word that describes the day. Stdlib only, deterministic.

The letter is U — for a day that went "unhinged": vivid (a day coming off
its hinges), funny at first read, and true to a real chaotic day. U is a
rare initial, so the word behind it lands at once, and it is not one of
the letters the rules prime (A for amazing, F for Friday-feeling, Z for
zero sleep), which the crowd will pile into.
"""
import os

TEXT = "U"


def main():
    # Enforce the scorer's gate (RULES.txt): UTF-8, exactly 1 character,
    # not whitespace-only; and the task: exactly ONE letter A-Z, nothing
    # else — no word, no gloss, no punctuation. Fail loudly instead of
    # writing an invalid entry.
    if len(TEXT) != 1 or not ("A" <= TEXT <= "Z"):
        raise SystemExit("entry text violates the 1-letter A-Z gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify: the file the grader reads must be byte-identical
    # to the gated text. Fail loudly instead of shipping a corrupt entry.
    with open(final_path, encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt read-back mismatch after atomic write")
    # Byte-length guard: the file on disk must hold exactly the gated
    # text's UTF-8 bytes — catches an encoding slip that a str read-back
    # alone would miss (e.g. a stray BOM written by another tool).
    if os.path.getsize(final_path) != len(TEXT.encode("utf-8")):
        raise SystemExit("entry.txt byte-length mismatch after atomic write")


if __name__ == "__main__":
    main()
