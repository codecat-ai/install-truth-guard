from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from install_truth_guard.parser import InstallClaim

Lookup = Callable[[str, str, float], bool]
SUPPORTED_ECOSYSTEMS = {"npm", "pypi"}
FAILURE_STATUSES = {"missing", "lookup-error", "unsupported-failure"}


@dataclass(frozen=True)
class CheckResult:
    claim: InstallClaim
    status: str
    reason: str


def check_claims(
    claims: list[InstallClaim],
    *,
    lookup: Lookup | None = None,
    timeout: float = 5.0,
    allow_unpublished: set[str] | None = None,
    strict_unsupported: bool = False,
    offline: bool = False,
) -> list[CheckResult]:
    lookup = lookup or registry_lookup
    allowed = allow_unpublished or set()
    results: list[CheckResult] = []

    for claim in claims:
        if claim.package in allowed:
            results.append(
                CheckResult(claim, "allowed", "package is listed in --allow-unpublished")
            )
            continue

        if offline:
            results.append(CheckResult(claim, "unchecked", "offline mode skips registry checks"))
            continue

        if claim.ecosystem not in SUPPORTED_ECOSYSTEMS:
            status = "unsupported-failure" if strict_unsupported else "unsupported"
            reason = "registry checks for this ecosystem are not supported yet"
            results.append(CheckResult(claim, status, reason))
            continue

        try:
            exists = lookup(claim.ecosystem, claim.package, timeout)
        except LookupError as exc:
            results.append(CheckResult(claim, "lookup-error", str(exc)))
            continue

        if exists:
            results.append(CheckResult(claim, "verified", "artifact exists in registry"))
        else:
            results.append(CheckResult(claim, "missing", "artifact was not found in registry"))

    return results


def registry_lookup(ecosystem: str, package: str, timeout: float) -> bool:
    if ecosystem == "npm":
        url = f"https://registry.npmjs.org/{quote(package, safe='')}"
    elif ecosystem == "pypi":
        url = f"https://pypi.org/pypi/{quote(package, safe='')}/json"
    else:
        raise LookupError(f"unsupported ecosystem: {ecosystem}")

    request = Request(
        url, headers={"Accept": "application/json", "User-Agent": "install-truth-guard"}
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            if response.status == 404:
                return False
            if response.status >= 400:
                raise LookupError(f"registry returned HTTP {response.status}")
            json.load(response)
            return True
    except HTTPError as exc:
        if exc.code == 404:
            return False
        raise LookupError(f"registry returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise LookupError(f"registry lookup failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise LookupError("registry lookup timed out") from exc
