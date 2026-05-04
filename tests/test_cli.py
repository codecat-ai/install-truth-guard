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


def test_cli_allow_unpublished_turns_missing_into_success(tmp_path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Install with `pip install planned-tool`.\n", encoding="utf-8")

    exit_code = cli.main(
        ["check", str(readme), "--allow-unpublished", "planned-tool"],
        lookup=lambda ecosystem, package, timeout: False,
    )

    assert exit_code == 0


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
