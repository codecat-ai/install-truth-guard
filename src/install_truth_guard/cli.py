from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from install_truth_guard.parser import parse_markdown
from install_truth_guard.registry import FAILURE_STATUSES, Lookup, check_claims


def main(argv: Sequence[str] | None = None, *, lookup: Lookup | None = None) -> int:
    parser = build_parser()
    normalized_argv = _normalize_argv(sys.argv[1:] if argv is None else list(argv))
    args = parser.parse_args(normalized_argv)

    paths = args.paths or [Path("README.md")]
    claims = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        claims.extend(parse_markdown(text, file_path=str(path)))
    ignored_ecosystems = set(args.ignore_ecosystem)
    claims = [claim for claim in claims if claim.ecosystem not in ignored_ecosystems]

    results = check_claims(
        claims,
        lookup=lookup,
        timeout=args.timeout,
        allow_unpublished=set(args.allow_unpublished),
        strict_unsupported=args.strict_unsupported,
        offline=args.offline,
    )

    failures = sum(result.status in FAILURE_STATUSES for result in results)
    if args.json:
        print(_json_payload(results, failures))
    else:
        print(_human_output(results, failures))

    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="install-truth-guard",
        description="Verify README package-manager install claims against registries.",
    )
    subparsers = parser.add_subparsers(dest="command")
    check_parser = subparsers.add_parser("check", help="check Markdown install claims")
    _add_check_arguments(check_parser)
    return parser


def _normalize_argv(argv: list[str]) -> list[str]:
    if not argv or argv[0] not in {"check", "-h", "--help"}:
        return ["check", *argv]
    return argv


def _add_check_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="*", type=Path, metavar="MARKDOWN")
    parser.add_argument("--json", action="store_true", help="emit JSON output")
    parser.add_argument(
        "--allow-unpublished",
        action="append",
        default=[],
        metavar="NAME",
        help="allow a package or image name that is intentionally unpublished",
    )
    parser.add_argument(
        "--strict-unsupported",
        action="store_true",
        help="treat unsupported ecosystems as failures",
    )
    parser.add_argument("--timeout", type=float, default=5.0, help="registry timeout in seconds")
    parser.add_argument(
        "--offline", action="store_true", help="parse only and skip registry checks"
    )
    parser.add_argument(
        "--ignore-ecosystem",
        action="append",
        default=[],
        metavar="ECOSYSTEM",
        help="omit parsed install claims for an ecosystem before checking",
    )


def _json_payload(results, failures: int) -> str:
    payload = {
        "summary": {"total": len(results), "failures": failures},
        "claims": [
            {
                "file": result.claim.file,
                "line": result.claim.line,
                "ecosystem": result.claim.ecosystem,
                "package": result.claim.package,
                "command": result.claim.command,
                "status": result.status,
                "reason": result.reason,
            }
            for result in results
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _human_output(results, failures: int) -> str:
    if not results:
        return "No install claims found."

    lines = []
    for result in results:
        claim = result.claim
        lines.append(
            f"{claim.file}:{claim.line} [{result.status}] "
            f"{claim.ecosystem}:{claim.package} - {result.reason}"
        )
    lines.append(f"Summary: {len(results)} claim(s), {failures} failure(s).")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
