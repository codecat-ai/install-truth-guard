import json

from install_truth_guard import cli


def test_cli_json_output_includes_claim_fields(tmp_path, capsys) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Install with `npx published-tool`.\n", encoding="utf-8")

    exit_code = cli.main(
        ["check", str(readme), "--json"],
        lookup=lambda ecosystem, package, timeout: True,
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["summary"] == {"total": 1, "failures": 0}
    assert payload["claims"][0] == {
        "file": str(readme),
        "line": 1,
        "ecosystem": "npm",
        "package": "published-tool",
        "command": "npx published-tool",
        "status": "verified",
        "reason": "artifact exists in registry",
    }


def test_cli_json_output_omits_ignored_ecosystems_before_lookup(tmp_path, capsys) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join(
            [
                "Install with `npx published-tool`.",
                "Install with `pip install ignored-tool`.",
                "Install with `cargo install ignored-crate`.",
            ]
        ),
        encoding="utf-8",
    )
    calls: list[tuple[str, str]] = []

    exit_code = cli.main(
        [
            "check",
            str(readme),
            "--json",
            "--ignore-ecosystem",
            "pypi",
            "--ignore-ecosystem",
            "cargo",
        ],
        lookup=lambda ecosystem, package, timeout: calls.append((ecosystem, package)) or True,
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert calls == [("npm", "published-tool")]
    assert payload["summary"] == {"total": 1, "failures": 0}
    assert [claim["ecosystem"] for claim in payload["claims"]] == ["npm"]
    assert [claim["package"] for claim in payload["claims"]] == ["published-tool"]


def test_cli_missing_supported_claim_exits_one(tmp_path, capsys) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Install with `pip install missing-tool`.\n", encoding="utf-8")

    exit_code = cli.main(
        ["check", str(readme)],
        lookup=lambda ecosystem, package, timeout: False,
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "missing-tool" in captured.out
    assert "missing" in captured.out


def test_cli_human_output_reports_no_claims_when_all_claims_are_ignored(tmp_path, capsys) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "Install with `cargo install ignored-crate`.\nRun with `docker run ignored/image`.\n",
        encoding="utf-8",
    )

    exit_code = cli.main(
        ["check", str(readme), "--ignore-ecosystem", "cargo", "--ignore-ecosystem", "docker"],
        lookup=lambda ecosystem, package, timeout: False,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "No install claims found."


def test_cli_allow_unpublished_turns_missing_into_success(tmp_path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Install with `pip install planned-tool`.\n", encoding="utf-8")

    exit_code = cli.main(
        ["check", str(readme), "--allow-unpublished", "planned-tool"],
        lookup=lambda ecosystem, package, timeout: False,
    )

    assert exit_code == 0


def test_cli_offline_omits_ignored_ecosystems(tmp_path, capsys) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "Install with `pip install kept-tool`.\nInstall with `npx ignored-tool`.\n",
        encoding="utf-8",
    )

    exit_code = cli.main(
        ["check", str(readme), "--offline", "--ignore-ecosystem", "npm"],
        lookup=lambda ecosystem, package, timeout: False,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "pypi:kept-tool" in captured.out
    assert "npm:ignored-tool" not in captured.out
    assert "Summary: 1 claim(s), 0 failure(s)." in captured.out


def test_cli_offline_reports_unchecked_and_does_not_lookup(tmp_path, capsys) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Install with `npx demo-tool`.\n", encoding="utf-8")
    calls: list[str] = []

    exit_code = cli.main(
        ["check", str(readme), "--offline", "--json"],
        lookup=lambda ecosystem, package, timeout: calls.append(package) or True,
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert calls == []
    assert payload["claims"][0]["status"] == "unchecked"
