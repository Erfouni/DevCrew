"""Command-line entry point: `devcrew "your project idea"`."""

import argparse
import os
import sys

from dotenv import load_dotenv

from . import __version__
from .agents import DEFAULT_MODEL

OUTPUT_FILES = (
    ("01_plan.json", "Project Manager's plan"),
    ("02_code.py", "Developer's code"),
    ("03_test_report.json", "QA Tester's report"),
    ("04_review.json", "Code Reviewer's verdict"),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devcrew",
        description="Run an AI software team (plan -> code -> test -> review) on a one-line idea.",
    )
    parser.add_argument("idea", help='what to build, e.g. "a CLI expense tracker"')
    parser.add_argument(
        "-o",
        "--output-dir",
        default="output",
        help="folder for results, relative to the current directory (default: output)",
    )
    parser.add_argument(
        "-m", "--model", default=None, help=f"LLM to use (default: $MODEL or {DEFAULT_MODEL})"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # CrewAI only writes task output to relative paths: it rejects ".." and "~",
    # and silently drops the leading "/" of an absolute path.
    if (
        os.path.isabs(args.output_dir)
        or ".." in args.output_dir.split(os.sep)
        or (args.output_dir.startswith(("~", "$")))
    ):
        parser.error("--output-dir must be a relative path inside the current directory")

    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Missing OPENAI_API_KEY. Copy .env.example to .env and add your key.")

    os.makedirs(args.output_dir, exist_ok=True)

    # Imported here so `--help` and `--version` stay fast.
    from .crew import run

    print(f"\n🚀 DevCrew starting on: {args.idea}\n")
    run(args.idea, output_dir=args.output_dir, model=args.model)
    print(f"\n✅ Done. Check the {args.output_dir}/ folder:")
    for name, what in OUTPUT_FILES:
        print(f"   {name:<20}— {what}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
