import subprocess


def get_git_info() -> dict:
    """
    Returns Git version information based on setuptools_scm and Git CLI.

    This function collects metadata from both setuptools_scm and native Git commands
    to provide details about the current repository state.

    Returns:
        dict: A dictionary with the following keys:
            - version (str): The version string as determined by setuptools_scm,
              typically based on Git tags and commit history.
              Example: '1.2.3', '0.1.dev4+gabc1234'
            - branch (str): The current Git branch name.
              Example: 'main', 'feature/new-ui'
            - commit (str): The short SHA of the current Git commit.
              Example: 'abc1234'
            - tag (str): The most recent Git tag reachable from the current commit.
              Example: 'v1.2.3'

    Notes:
        - If the repository is not a valid Git repository or commands fail,
          fallback values like 'unknown' will be returned.
        - setuptools_scm must be installed and properly configured to extract the version.

    Example:
        >>> info = get_git_info()
        >>> print(f"Version: {info['version']} | Branch: {info['branch']} | Commit: {info['commit']} | Tag: {info['tag']}")
    """
    try:
        import setuptools_scm

        version = setuptools_scm.get_version()
    except Exception:
        version = "unknown"

    try:
        branch = (
            subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        )
    except Exception:
        branch = "unknown"

    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        commit = "unknown"

    try:
        tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        tag = "unknown"

    return {
        "version": version,
        "branch": branch,
        "commit": commit,
        "tag": tag,
    }
