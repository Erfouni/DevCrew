"""DevCrew — run an AI software team on a one-line project idea.

Usage:
    python main.py "Build a CLI expense tracker"

Once installed (`pip install -e .`), the same thing is available as `devcrew "..."`.
"""

import sys

from devcrew.cli import main

if __name__ == "__main__":
    sys.exit(main())
