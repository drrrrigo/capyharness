import subprocess
import tempfile
import unittest
from pathlib import Path

from aih.workspace import find_repository


class WorkspaceTests(unittest.TestCase):
    def test_find_repository_from_nested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "project"
            repository.mkdir()
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            nested = repository / "src" / "backend"
            nested.mkdir(parents=True)

            self.assertEqual(find_repository(nested), repository.resolve())

    def test_find_repository_returns_none_outside_git(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "ordinary-directory"
            directory.mkdir()

            self.assertIsNone(find_repository(directory))
