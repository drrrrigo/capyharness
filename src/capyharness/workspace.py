"""Locate the Git workspace containing a directory."""

import logging
from pathlib import Path

from capyharness.git import run_git

logger = logging.getLogger(__name__)


def find_repository(path: Path) -> Path | None:
    """Return the Git working tree root, or None outside a repository."""
    directory = path.resolve()
    result = run_git("rev-parse", "--show-toplevel", cwd=directory)
    if result.returncode != 0:
        logger.debug("Git did not find a working tree at %s: %s", directory, result.stderr.strip())
        return None

    root = Path(result.stdout.strip()).resolve()
    logger.debug("Git workspace for %s is %s", directory, root)
    return root