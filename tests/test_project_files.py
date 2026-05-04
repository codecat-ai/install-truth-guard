from pathlib import Path


def test_required_project_files_exist() -> None:
    required = [
        "pyproject.toml",
        "README.md",
        "README-zh.md",
        "README-jp.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        ".github/workflows/ci.yml",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/pull_request_template.md",
    ]

    missing = [path for path in required if not Path(path).exists()]

    assert missing == []
