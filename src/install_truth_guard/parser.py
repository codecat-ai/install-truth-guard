from __future__ import annotations

import re
import shlex
from dataclasses import dataclass


@dataclass(frozen=True)
class InstallClaim:
    file: str
    line: int
    ecosystem: str
    package: str
    command: str


_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_SUPPORTED_COMMANDS = {"npm", "npx", "pnpm", "yarn", "pip", "uvx", "cargo", "docker"}


def parse_markdown(markdown: str, *, file_path: str = "README.md") -> list[InstallClaim]:
    claims: list[InstallClaim] = []
    in_fence = False

    for line_number, line in enumerate(markdown.splitlines(), start=1):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue

        if in_fence:
            claim = parse_command(line.strip(), file_path=file_path, line=line_number)
            if claim is not None:
                claims.append(claim)
            continue

        for match in _INLINE_CODE_RE.finditer(line):
            claim = parse_command(match.group(1).strip(), file_path=file_path, line=line_number)
            if claim is not None:
                claims.append(claim)

    return claims


def parse_command(command: str, *, file_path: str, line: int) -> InstallClaim | None:
    if not command:
        return None

    try:
        parts = shlex.split(command)
    except ValueError:
        return None

    if not parts or parts[0] not in _SUPPORTED_COMMANDS:
        return None

    package = _package_from_parts(parts)
    if package is None:
        return None

    ecosystem = _ecosystem_for(parts[0])
    return InstallClaim(
        file=file_path,
        line=line,
        ecosystem=ecosystem,
        package=package,
        command=command,
    )


def _ecosystem_for(command: str) -> str:
    if command in {"npm", "npx", "pnpm", "yarn"}:
        return "npm"
    if command in {"pip", "uvx"}:
        return "pypi"
    return command


def _package_from_parts(parts: list[str]) -> str | None:
    command = parts[0]

    if command == "npm":
        if len(parts) >= 4 and parts[1] == "install" and parts[2] == "-g":
            return _valid_package(parts[3])
        if len(parts) >= 4 and parts[1] == "install" and parts[2] == "--global":
            return _valid_package(parts[3])
        return None

    if command == "npx" and len(parts) >= 2:
        return _valid_package(_skip_leading_options(parts[1:]))

    if command in {"pnpm", "yarn"} and len(parts) >= 3 and parts[1] == "dlx":
        return _valid_package(_skip_leading_options(parts[2:]))

    if command == "pip" and len(parts) >= 3 and parts[1] == "install":
        package = _skip_leading_options(parts[2:])
        if package in {".", "-e"}:
            return None
        return _valid_package(package)

    if command == "uvx" and len(parts) >= 2:
        return _valid_package(_skip_leading_options(parts[1:]))

    if command == "cargo" and len(parts) >= 3 and parts[1] == "install":
        return _valid_package(_skip_leading_options(parts[2:]))

    if command == "docker" and len(parts) >= 3 and parts[1] in {"pull", "run"}:
        return _valid_package(
            _skip_docker_run_options(parts[2:] if parts[1] == "run" else parts[2:])
        )

    return None


def _skip_leading_options(parts: list[str]) -> str | None:
    iterator = iter(parts)
    for part in iterator:
        if part in {"-e", "--editable"}:
            return None
        if part.startswith("-"):
            continue
        return part
    return None


def _skip_docker_run_options(parts: list[str]) -> str | None:
    options_with_values = {
        "-e",
        "--env",
        "-p",
        "--publish",
        "-v",
        "--volume",
        "--name",
        "--network",
    }
    index = 0
    while index < len(parts):
        part = parts[index]
        if part in options_with_values:
            index += 2
            continue
        if part.startswith("--") and "=" in part:
            index += 1
            continue
        if part.startswith("-"):
            index += 1
            continue
        return part
    return None


def _valid_package(package: str | None) -> str | None:
    if not package or package.startswith("-"):
        return None
    if package in {".", "./", "../"}:
        return None
    return package
