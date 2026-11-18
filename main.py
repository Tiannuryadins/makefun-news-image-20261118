#!/usr/bin/env python3
"""The World in One Image — Wednesday, 18 November 2026.

make.fun competition news-image-20261118: "Sum up 18 November's world
news in one image". Running this file copies the newspaper poster that
ships beside it (world_news_18_nov_2026.png) to /output/entry.png.

The poster was drawn at build time by render_poster.py (Pillow). This
file only ever reads that PNG and writes its bytes elsewhere, using the
standard library alone — no Pillow, no network, no randomness. The
grader runs `python3 -P -s`, where third-party packages do not exist, so
stdlib-only is what makes the entry work here.

Gate: a whole PNG, at most 1 MiB, at most 1024x1024 px. This poster is
1024x1024 and well under the byte cap. Both grader runs write the same
fixed bytes, so the two runs are identical by construction.

Usage:
    python3 main.py                  -> /output/entry.png
    python3 main.py out.png          -> the given path
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py

If /output cannot be created or written, ./output/entry.png is used.

Author: Januar (@januar). Payout wallet (reference only, unused here):
FM6M2TMzjhzj7QztEV91bAwV4N2bApYd2AZpZLcHyeKm
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

POSTER = "world_news_18_nov_2026.png"
TARGET = "entry.png"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def load_poster():
    """The poster PNG that ships next to this file, as bytes."""
    path = Path(__file__).resolve().parent / POSTER
    try:
        return path.read_bytes()
    except OSError as exc:
        raise SystemExit(f"error: cannot read {POSTER}: {exc}")


def read_ihdr(blob):
    """Width and height from a PNG's IHDR chunk, stdlib only."""
    if blob[:8] != PNG_MAGIC or len(blob) < 33:
        raise SystemExit("error: not a valid PNG file")
    (size, kind) = struct.unpack(">I4s", blob[8:16])
    if kind != b"IHDR" or size != 13:
        raise SystemExit("error: PNG has no IHDR chunk first")
    return struct.unpack(">II", blob[16:24])


def pick_destination(argv):
    """Where entry.png goes: argv, then MAKEFUN_OUTPUT_DIR, then /output."""
    if len(argv) > 1:
        return Path(argv[1])
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(wanted, exist_ok=True)
        probe = Path(wanted) / ".makefun_write_test"
        probe.touch()
        probe.unlink()
    except OSError:
        wanted = Path.cwd() / "output"
        os.makedirs(wanted, exist_ok=True)
    return Path(wanted) / TARGET


def main(argv):
    blob = load_poster()
    width, height = read_ihdr(blob)
    if len(blob) > MAX_BYTES or width > MAX_SIDE or height > MAX_SIDE:
        print(f"error: poster is {width}x{height}, {len(blob)} bytes — "
              f"over the 1 MiB / 1024x1024 gate", file=sys.stderr)
        return 1
    dest = pick_destination(argv)
    dest.write_bytes(blob)
    digest = hashlib.sha256(blob).hexdigest()[:16]
    print(f"wrote {dest} — PNG {width}x{height}, {len(blob):,} bytes, "
          f"sha256={digest}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
