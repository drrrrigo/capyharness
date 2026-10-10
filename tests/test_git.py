import subprocess
import tempfile
import unittest
from pathlib import Path

from capyharness.git import GitStatus, get_branch, get_status


class GitTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repository = Path(temporary.name) / "project"
        self.repository.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "lesson", str(self.repository)], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repository, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.invalid"],
            cwd=self.repository,
            check=True,
        )

    def commit(self, filename: str) -> None:
        subprocess.run(["git", "add", filename], cwd=self.repository, check=True)
        subprocess.run(["git", "commit", "-qm", "Initial commit"], cwd=self.repository, check=True)

    def test_get_branch_before_first_commit(self) -> None:
        self.assertEqual(get_branch(self.repository), "lesson")

    def test_get_status_counts_unstaged_untracked_and_staged(self) -> None:
        tracked = self.repository / "tracked.txt"
        tracked.write_text("original\n")
        self.commit("tracked.txt")

        tracked.write_text("changed\n")
        (self.repository / "staged.txt").write_text("staged\n")
        subprocess.run(["git", "add", "staged.txt"], cwd=self.repository, check=True)
        (self.repository / "untracked.txt").write_text("untracked\n")

        self.assertEqual(
            get_status(self.repository), GitStatus(modified=1, untracked=1, staged=1)
        )

    def test_get_status_skips_second_path_of_rename(self) -> None:
        (self.repository / "old.txt").write_text("file\n")
        self.commit("old.txt")
        subprocess.run(["git", "mv", "old.txt", "new.txt"], cwd=self.repository, check=True)

        self.assertEqual(get_status(self.repository), GitStatus(staged=1))
