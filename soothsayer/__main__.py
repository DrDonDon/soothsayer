"""Cross-platform entrypoint: `python -m soothsayer ...` (works on Windows too)."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
