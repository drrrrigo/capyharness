import contextlib
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from aih.cli import main


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        original_directory = Path.cwd()
        self.addCleanup(os.chdir, original_directory)

    def test_status_command_in_repository(self) -> None:
        repository = self.directory / "example"
        repository.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "lesson", str(repository)], check=True)
        nested = repository / "src"
        nested.mkdir()
        os.chdir(nested)
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["status"])

        self.assertEqual(exit_code, 0)
        self.assertIn(f"Workspace: {repository.resolve()}", stdout.getvalue())
        self.assertIn("Repository: example", stdout.getvalue())
        self.assertIn("Branch: lesson", stdout.getvalue())
        self.assertIn("Untracked files: 0", stdout.getvalue())

    def test_status_command_outside_repository(self) -> None:
        directory = self.directory / "ordinary-directory"
        directory.mkdir()
        os.chdir(directory)
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = main(["status"])

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("No Git repository found", stderr.getvalue())
