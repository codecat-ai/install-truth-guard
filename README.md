# install-truth-guard

[English](README.md) | [中文](README-zh.md) | [日本語](README-ja.md)

`install-truth-guard` is a CI-friendly checker for README install claims. It parses Markdown for package-manager commands and verifies supported package names against read-only registries, so documentation does not advertise install paths before artifacts exist.

## Problem and Motivation

README files often gain install commands before a package, image, or command is actually published. That can mislead users, break onboarding, and hide release-process gaps until someone tries the command in CI or during evaluation. `install-truth-guard` gives maintainers a small, safe check that reads Markdown, recognizes common install commands, and reports whether those claims are currently truthful.

## Status

This repository is not published as a package. Use clone/local workflows only.

## Features

- Detects npm-style claims such as `npx`, global `npm install`, `pnpm dlx`, and `yarn dlx`.
- Detects PyPI-style claims such as `pip install` and `uvx`.
- Parses Cargo and Docker claims as unsupported ecosystems by default, with an optional strict mode.
- Supports JSON output for CI automation and offline parsing when registry access is not desired.
- Allows intentionally unpublished names and repeatable ecosystem ignores for staged releases.

## What It Checks

Supported registry checks:

- npm commands: npx, global npm install, pnpm dlx, and yarn dlx.
- PyPI commands: pip install and uvx.

Parsed but unsupported by default:

- Cargo install commands.
- Docker pull and run commands.

Unsupported claims are advisory unless `--strict-unsupported` is enabled.

## Installation

No package-registry release is published yet. Clone the repository and run the CLI from the source checkout:

```sh
git clone https://github.com/codecat-ai/install-truth-guard.git
cd install-truth-guard
python -m install_truth_guard check README.md
```

For development, create an isolated environment and install local development dependencies from the checkout before running tests.

## Quick Start

```sh
python -m install_truth_guard check README.md
python -m install_truth_guard check README.md --json
python -m install_truth_guard check README.md --offline
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

## Examples

Check a README while ignoring Docker claims that are intentionally documented but not enforced yet:

```sh
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

Treat unsupported Cargo or Docker claims as CI failures:

```sh
python -m install_truth_guard check README.md --strict-unsupported
```

Allow one intentionally unpublished package name during a staged release:

```sh
python -m install_truth_guard check README.md --allow-unpublished example-package
```

## Configuration

All configuration is currently passed through CLI flags:

- `--json`: emit machine-readable results.
- `--allow-unpublished NAME`: suppress an intentional unpublished claim.
- `--ignore-ecosystem ECOSYSTEM`: omit parsed claims for an ecosystem before registry checks and output. Repeat to ignore multiple ecosystems, for example `--ignore-ecosystem cargo --ignore-ecosystem docker`.
- `--strict-unsupported`: fail on unsupported ecosystems.
- `--timeout SECONDS`: set the registry timeout.
- `--offline`: parse Markdown without contacting registries.

A reusable project policy file is planned in the roadmap.

## Development

Install from a local checkout in an isolated Python environment, then run:

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## Testing

The test suite covers Markdown command extraction, supported and unsupported ecosystem handling, JSON output, offline mode, allow-list behavior, and CLI filtering such as `--ignore-ecosystem`.

## Safety

The tool does not execute README commands. Registry checks are read-only HTTP requests for npm and PyPI metadata.

## Roadmap

Maturity: `maintenance`

Planned cadence: every 2-4 weeks, plus urgent fixes for broken registry checks, README truthfulness regressions, or CI failures.

Now:

- Keep source-checkout usage documentation truthful until a package registry release is explicitly approved and verified.
- Maintain the portfolio-standard roadmap and cadence notes.

Next:

- Add a documented configuration file for repeated allow/ignore policies across multiple README files.
- Add GitHub Actions annotation output for CI runs.
- Expand offline examples for npm, PyPI, Cargo, and Docker claim handling.

Later:

- Evaluate safe read-only Cargo and Docker existence checks.
- Add a multi-file scan mode for translated README variants and documentation folders.
- Review whether the project should move to `mature-low-frequency` once the remaining roadmap items become nice-to-have options.

See [ROADMAP.md](ROADMAP.md) for maintenance triggers, cadence-review notes, and completion-review rules.

## Contributing

Issues and focused pull requests are welcome. Please keep changes small, add behavior-focused tests for CLI or parser changes, and avoid documenting package-registry install commands unless the package has actually been published and verified.

## License

MIT. See [LICENSE](LICENSE).

This project is written and maintained with AI assistance, with human-readable docs and tests kept as the source of truth.
