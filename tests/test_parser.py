from install_truth_guard.parser import parse_markdown


def test_parse_fenced_and_inline_install_claims() -> None:
    markdown = """
# Demo

```sh
npx demo-tool --help
npm install -g @scope/demo-tool
pip install demo-tool
uvx demo-tool --version
cargo install demo-tool
docker pull ghcr.io/example/demo-tool:latest
```

Try `pnpm dlx @scope/demo-tool init` or `yarn dlx demo-tool doctor`.
"""

    claims = parse_markdown(markdown, file_path="README.md")

    observed = [(claim.ecosystem, claim.package, claim.command) for claim in claims]
    assert observed == [
        ("npm", "demo-tool", "npx demo-tool --help"),
        ("npm", "@scope/demo-tool", "npm install -g @scope/demo-tool"),
        ("pypi", "demo-tool", "pip install demo-tool"),
        ("pypi", "demo-tool", "uvx demo-tool --version"),
        ("cargo", "demo-tool", "cargo install demo-tool"),
        (
            "docker",
            "ghcr.io/example/demo-tool:latest",
            "docker pull ghcr.io/example/demo-tool:latest",
        ),
        ("npm", "@scope/demo-tool", "pnpm dlx @scope/demo-tool init"),
        ("npm", "demo-tool", "yarn dlx demo-tool doctor"),
    ]
    assert {claim.file for claim in claims} == {"README.md"}


def test_ignores_local_development_and_non_install_commands() -> None:
    markdown = """
Run `python -m install_truth_guard check README.md`.

```bash
npm test
python -m pytest
docker build .
pip install -e .
npm install
```
"""

    assert parse_markdown(markdown, file_path="README.md") == []
