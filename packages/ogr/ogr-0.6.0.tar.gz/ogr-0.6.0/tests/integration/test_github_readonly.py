import os
import unittest

from ogr import GithubService
from ogr.persistent_storage import PersistentObjectStorage

DATA_DIR = "test_data"
PERSISTENT_DATA_PREFIX = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), DATA_DIR
)


class ReadOnly(unittest.TestCase):
    def setUp(self):
        self.token = os.environ.get("GITHUB_TOKEN")
        self.user = os.environ.get("GITHUB_USER")
        test_name = self.id() or "all"
        persistent_data_file = os.path.join(
            PERSISTENT_DATA_PREFIX, f"test_github_data_{test_name}.yaml"
        )
        PersistentObjectStorage().storage_file = persistent_data_file
        if PersistentObjectStorage().is_write_mode and (
            not self.user or not self.token
        ):
            raise EnvironmentError("please set GITHUB_TOKEN GITHUB_USER env variables")

        self.service = GithubService(token=self.token, read_only=True)

        self.colin_project = self.service.get_project(
            namespace="user-cont", repo="colin"
        )

    def tearDown(self):
        PersistentObjectStorage().dump()

    def test_pr_comments(self):
        pr_comments = self.colin_project.get_pr_comments(7)
        assert pr_comments
        assert len(pr_comments) == 2
        assert pr_comments[0].comment.endswith("I've just integrated your thoughts.")
        assert pr_comments[1].comment.startswith("Thank you!")

    def test_create_pr(self):
        pr = self.colin_project.pr_create("title", "text", "master", "souce_branch")
        assert pr.title == "title"

    def test_create_fork(self):
        fork = self.colin_project.fork_create()
        assert not fork.is_fork
