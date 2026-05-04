from install_truth_guard.parser import InstallClaim
from install_truth_guard.registry import CheckResult, check_claims


def claim(ecosystem: str, package: str) -> InstallClaim:
    return InstallClaim(
        file="README.md",
        line=1,
        ecosystem=ecosystem,
        package=package,
        command=f"{ecosystem} {package}",
    )


def test_supported_registry_success_and_missing_with_fake_client() -> None:
    calls: list[tuple[str, str, float]] = []

    def fake_lookup(ecosystem: str, package: str, timeout: float) -> bool:
        calls.append((ecosystem, package, timeout))
        return package == "published"

    results = check_claims(
        [claim("npm", "published"), claim("pypi", "missing")],
        lookup=fake_lookup,
        timeout=2.5,
    )

    assert calls == [("npm", "published", 2.5), ("pypi", "missing", 2.5)]
    assert [result.status for result in results] == ["verified", "missing"]
    assert results[1].reason == "artifact was not found in registry"


def test_allow_unpublished_suppresses_missing_supported_claim() -> None:
    results = check_claims(
        [claim("npm", "planned")],
        lookup=lambda ecosystem, package, timeout: False,
        allow_unpublished={"planned"},
    )

    assert results == [
        CheckResult(
            claim=claim("npm", "planned"),
            status="allowed",
            reason="package is listed in --allow-unpublished",
        )
    ]


def test_unsupported_and_offline_modes_do_not_lookup() -> None:
    calls: list[str] = []

    unsupported = check_claims(
        [claim("cargo", "demo")],
        lookup=lambda ecosystem, package, timeout: calls.append(package) or True,
    )
    offline = check_claims(
        [claim("npm", "demo")],
        lookup=lambda ecosystem, package, timeout: calls.append(package) or True,
        offline=True,
    )

    assert calls == []
    assert unsupported[0].status == "unsupported"
    assert offline[0].status == "unchecked"


def test_strict_unsupported_is_failure_status() -> None:
    results = check_claims([claim("docker", "demo/image")], strict_unsupported=True)

    assert results[0].status == "unsupported-failure"
