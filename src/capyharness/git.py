"""Read branch and working tree information using the Git executable."""

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


class GitError(Exception):
    """Git could not provide information needed by the CLI."""


@dataclass(frozen=True)
class GitStatus:
    modified: int = 0
    untracked: int = 0
    staged: int = 0


def run_git(*arguments: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a fixed Git command in an explicit directory, capturing its output."""
    command = ["git", *arguments]
    logger.debug("Running %s in %s", command, cwd)
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise GitError("Git executable was not found. Install Git and try again.") from error


def _output_or_error(result: subprocess.CompletedProcess[str]) -> str:
    if result.returncode != 0:
        detail = result.stderr.strip() or "Git returned no error details."
        raise GitError(f"Git exited with code {result.returncode}: {detail}")
    return result.stdout


def get_branch(workspace: Path) -> str:
    """Return the branch name, including on a branch with no commits yet."""
    result = run_git("symbolic-ref", "--quiet", "--short", "HEAD", cwd=workspace)
    if result.returncode == 0:
        return result.stdout.strip()

    # A detached HEAD has no branch name, but it still has a commit.
    commit = _output_or_error(run_git("rev-parse", "--short", "HEAD", cwd=workspace))
    return f"(detached at {commit.strip()})"


def get_status(workspace: Path) -> GitStatus:
    """Count unstaged, untracked and staged file entries from Git porcelain output."""
    output = _output_or_error(
        run_git("status", "--porcelain=v1", "-z", "--untracked-files=all", cwd=workspace)
    )
    entries = output.split("\0")
    modified = untracked = staged = 0
    index = 0

    while index < len(entries) and entries[index]:
        entry = entries[index]
        if len(entry) < 4 or entry[2] != " ":
            raise GitError("Git returned an unexpected status entry.")

        index_status, worktree_status = entry[0], entry[1]
        if entry[:2] == "??":
            untracked += 1
        else:
            if index_status != " ":
                staged += 1
            if worktree_status != " ":
                modified += 1

        # In -z output, renames and copies carry a second, NUL-terminated path.
        if index_status in "RC" or worktree_status in "RC":
            index += 1
        index += 1

    return GitStatus(modified=modified, untracked=untracked, staged=staged)
