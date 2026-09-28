"""File-based git readers (gitinfo.py): no git process involved."""
from gitinfo import (
    project_name,
    read_branch,
    read_origin_url,
    repo_url_from_workspace,
    repo_web_url,
)

CONFIG = """[core]
\trepositoryformatversion = 0
[remote "upstream"]
\turl = https://github.com/other/fork.git
[remote "origin"]
\turl = git@github.com:user/my-repo.git
\tfetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
\tremote = origin
"""


def make_repo(root, head="ref: refs/heads/main\n", config=CONFIG):
    git = root / ".git"
    git.mkdir(parents=True)
    (git / "HEAD").write_text(head, encoding="utf-8")
    (git / "config").write_text(config, encoding="utf-8")
    return git


class TestReadBranch:
    def test_branch_from_subdirectory(self, tmp_path):
        make_repo(tmp_path)
        sub = tmp_path / "src" / "pkg"
        sub.mkdir(parents=True)
        assert read_branch(str(sub)) == "main"

    def test_branch_with_slash(self, tmp_path):
        make_repo(tmp_path, head="ref: refs/heads/fix/kana-code-rpc-1.1.0\n")
        assert read_branch(str(tmp_path)) == "fix/kana-code-rpc-1.1.0"

    def test_detached_head(self, tmp_path):
        make_repo(tmp_path, head="012bac3f0000000000000000000000000000abcd\n")
        assert read_branch(str(tmp_path)) == ""

    def test_not_a_repo(self, tmp_path):
        assert read_branch(str(tmp_path / "nowhere")) == ""
        assert read_branch("") == ""


class TestOriginUrl:
    def test_origin_not_other_remotes(self, tmp_path):
        make_repo(tmp_path)
        assert read_origin_url(str(tmp_path)) == "git@github.com:user/my-repo.git"

    def test_no_origin(self, tmp_path):
        make_repo(tmp_path, config='[remote "upstream"]\n\turl = https://x.org/a/b\n')
        assert read_origin_url(str(tmp_path)) == ""

    def test_quoted_value(self, tmp_path):
        make_repo(tmp_path, config='[remote "origin"]\n\turl = "https://gitlab.com/g/p.git"\n')
        assert read_origin_url(str(tmp_path)) == "https://gitlab.com/g/p.git"


class TestLinkedWorktree:
    def test_head_from_worktree_config_from_common_dir(self, tmp_path):
        main_git = make_repo(tmp_path / "main")
        wt_git = main_git / "worktrees" / "feature"
        wt_git.mkdir(parents=True)
        (wt_git / "HEAD").write_text("ref: refs/heads/feature\n", encoding="utf-8")
        (wt_git / "commondir").write_text("../..\n", encoding="utf-8")
        checkout = tmp_path / "feature-checkout"
        checkout.mkdir()
        (checkout / ".git").write_text(f"gitdir: {wt_git}\n", encoding="utf-8")

        assert read_branch(str(checkout)) == "feature"
        assert read_origin_url(str(checkout)) == "git@github.com:user/my-repo.git"


class TestRepoWebUrl:
    def test_https_with_git_suffix(self):
        assert repo_web_url("https://github.com/user/repo.git") == "https://github.com/user/repo"

    def test_https_without_suffix(self):
        assert repo_web_url("https://gitlab.com/group/project") == "https://gitlab.com/group/project"

    def test_ssh_scp_form(self):
        assert repo_web_url("git@github.com:user/repo.git") == "https://github.com/user/repo"

    def test_ssh_url_form(self):
        assert repo_web_url("ssh://git@github.com/user/repo.git") == "https://github.com/user/repo"

    def test_empty_and_garbage(self):
        assert repo_web_url("") == ""
        assert repo_web_url("/local/path/to/repo") == ""

    def test_nested_group_path(self):
        assert repo_web_url("git@gitlab.com:group/subgroup/repo.git") == "https://gitlab.com/group/subgroup/repo"

    def test_userinfo_stripped_from_https(self):
        # Credentials embedded in a remote must never reach the button URL
        assert repo_web_url("https://user:token@github.com/user/repo.git") == "https://github.com/user/repo"
        assert repo_web_url("https://oauth2@gitlab.com/group/repo") == "https://gitlab.com/group/repo"


class TestWorkspaceRepo:
    def test_builds_url(self):
        repo = {"host": "github.com", "owner": "Linaqruf", "name": "kana-code-plugins"}
        assert repo_url_from_workspace(repo) == "https://github.com/Linaqruf/kana-code-plugins"

    def test_rejects_missing_or_unsafe(self):
        assert repo_url_from_workspace(None) == ""
        assert repo_url_from_workspace({"host": "github.com", "owner": "a"}) == ""
        assert repo_url_from_workspace({"host": "evil.com/x?", "owner": "a", "name": "b"}) == ""


class TestProjectName:
    def test_name_from_remote_url(self):
        assert project_name("/some/dir", "https://github.com/user/my-repo.git") == "my-repo"

    def test_name_from_ssh_remote(self):
        assert project_name("/some/dir", "git@github.com:user/other-repo.git") == "other-repo"

    def test_folder_fallback_when_no_remote(self):
        assert project_name("/some/dir/folder-name", "") == "folder-name"
