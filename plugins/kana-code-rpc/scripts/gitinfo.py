"""
Git facts read from files, never from a git process.

The branch and the origin URL are plain text in `.git/HEAD` and
`.git/config`. Reading them costs a few file reads. Spawning git costs a
process, and on the statusline that ran on every render.
"""

import re
from pathlib import Path


def find_git_dir(start: str) -> Path | None:
    """Return the git dir of the repository that contains `start`, or None.

    Follows a `.git` *file* (`gitdir: <path>`), which linked worktrees and
    submodules use instead of a `.git` directory.
    """
    if not start:
        return None
    try:
        here = Path(start).absolute()
    except (OSError, ValueError):
        return None
    for directory in (here, *here.parents):
        dotgit = directory / ".git"
        try:
            if dotgit.is_dir():
                return dotgit
            if dotgit.is_file():
                text = dotgit.read_text(encoding="utf-8", errors="replace").strip()
                if not text.startswith("gitdir:"):
                    return None
                git_dir = Path(text[len("gitdir:"):].strip())
                if not git_dir.is_absolute():
                    git_dir = directory / git_dir
                return git_dir if git_dir.is_dir() else None
        except OSError:
            return None
    return None


def _common_dir(git_dir: Path) -> Path:
    """A linked worktree keeps HEAD in its own git dir but shares `config`
    with the main repository, named by the `commondir` file."""
    try:
        rel = (git_dir / "commondir").read_text(encoding="utf-8").strip()
    except OSError:
        return git_dir
    common = Path(rel)
    return common if common.is_absolute() else git_dir / common


def read_branch(start: str) -> str:
    """Current branch name, or '' for a detached HEAD or no repository."""
    git_dir = find_git_dir(start)
    if git_dir is None:
        return ""
    try:
        head = (git_dir / "HEAD").read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return ""
    prefix = "ref: refs/heads/"
    return head[len(prefix):] if head.startswith(prefix) else ""


_SECTION_RE = re.compile(r'^\s*\[\s*([^\s\]"]+)(?:\s+"((?:[^"\\]|\\.)*)")?\s*\]')
_URL_RE = re.compile(r'^\s*url\s*=\s*(.*?)\s*$', re.IGNORECASE)


def read_origin_url(start: str) -> str:
    """The `remote "origin"` URL from the repository's config, or ''."""
    git_dir = find_git_dir(start)
    if git_dir is None:
        return ""
    try:
        config = (_common_dir(git_dir) / "config").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    in_origin = False
    for line in config.splitlines():
        section = _SECTION_RE.match(line)
        if section:
            in_origin = section.group(1).lower() == "remote" and section.group(2) == "origin"
            continue
        if in_origin:
            m = _URL_RE.match(line)
            if m:
                value = m.group(1)
                if len(value) >= 2 and value[0] == value[-1] == '"':
                    value = value[1:-1]
                return value
    return ""


def repo_web_url(remote_url: str) -> str:
    """Convert a git remote URL to a clickable https URL, or '' if not derivable.

    Handles: https://host/owner/repo(.git), git@host:owner/repo(.git),
    ssh://git@host/owner/repo(.git).
    """
    if not remote_url:
        return ""
    url = remote_url.strip()
    m = re.match(r'^(?:ssh://)?git@([^:/]+)[:/](.+?)(?:\.git)?/?$', url)
    if m:
        return f"https://{m.group(1)}/{m.group(2)}"
    # Strip userinfo (user[:token]@host) so credentials never reach the button URL
    m = re.match(r'^https?://(?:[^@/]+@)?([^/]+)/(.+?)(?:\.git)?/?$', url)
    if m:
        return f"https://{m.group(1)}/{m.group(2)}"
    return ""


_SAFE_PART = re.compile(r'^[A-Za-z0-9._-]+$')


def repo_url_from_workspace(repo: dict | None) -> str:
    """Build the repository URL from the statusline's `workspace.repo`
    ({host, owner, name}), which Claude Code fills in from the remote."""
    if not isinstance(repo, dict):
        return ""
    host, owner, name = repo.get("host"), repo.get("owner"), repo.get("name")
    if not all(isinstance(p, str) and _SAFE_PART.match(p) for p in (host, owner, name)):
        return ""
    return f"https://{host}/{owner}/{name}"


def project_name(project_path: str, remote_url: str = "") -> str:
    """Repository name from the remote URL, else the folder name."""
    if remote_url:
        m = re.search(r'[/:]([^/:]+?)(?:\.git)?/?$', remote_url.strip())
        if m:
            return m.group(1)
    return Path(project_path).name if project_path else ""
