# install-truth-guard

`install-truth-guard` is a CI-friendly checker for README install claims. It
parses Markdown for package-manager commands and verifies supported package
names against read-only registries, so documentation does not advertise install
paths before artifacts exist.

## Status

This repository is not published as a package. Use clone/local workflows only.

## What It Checks

Supported registry checks:

- npm commands: npx, global npm install, pnpm dlx, and yarn dlx.
- PyPI commands: pip install and uvx.

Parsed but unsupported by default:

- Cargo install commands.
- Docker pull and run commands.

Unsupported claims are advisory unless `--strict-unsupported` is enabled.

## Local Usage

From a clone of this repository:

```sh
python -m install_truth_guard check README.md
python -m install_truth_guard check README.md --json
python -m install_truth_guard check README.md --offline
```

For development, install the project in an isolated environment from the local
checkout, then run:

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## Options

- `--json`: emit machine-readable results.
- `--allow-unpublished NAME`: suppress an intentional unpublished claim.
- `--strict-unsupported`: fail on unsupported ecosystems.
- `--timeout SECONDS`: set the registry timeout.
- `--offline`: parse Markdown without contacting registries.

## Safety

The tool does not execute README commands. Registry checks are read-only HTTP
requests for npm and PyPI metadata.
