"""The command-line interface for AI Dev Harness."""

import argparse
import logging
import sys
from pathlib import Path
from collections.abc import Sequence

from aih.git import GitError, get_branch, get_status
from aih.workspace import find_repository


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aih", description="AI Dev Harness")
    parser.add_argument("--verbose", action="store_true", help="show debug logging")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("status", help="show Git workspace information")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    if args.command is None:
        parser.print_help()
        return 0

    try:
        workspace = find_repository(Path.cwd())
        if workspace is None:
            print("No Git repository found for the current directory.", file=sys.stderr)
            return 1

        branch = get_branch(workspace)
        status = get_status(workspace)
    except GitError as error:
        print(f"Unable to inspect Git repository: {error}", file=sys.stderr)
        return 1

    print(
        f"AI Dev Harness\n\n"
        f"Workspace: {workspace}\n"
        f"Repository: {workspace.name}\n"
        f"Branch: {branch}\n"
        f"Working tree:\n"
        f"  Modified files: {status.modified}\n"
        f"  Untracked files: {status.untracked}\n"
        f"  Staged files: {status.staged}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
