# install-truth-guard

[English](README.md) | [中文](README-zh.md) | [日本語](README-jp.md)


`install-truth-guard` は README のインストール手順が実際の公開状態と合っているか
を確認する CI 向けツールです。Markdown 内のパッケージマネージャーコマンドを解析し、
対応済みの npm と PyPI について読み取り専用のレジストリ確認を行います。

## 状態

このリポジトリはまだパッケージとして公開されていません。クローンしたローカル環境で
利用してください。

## ローカルでの利用

リポジトリのクローン内で実行します。

```sh
python -m install_truth_guard check README.md
python -m install_truth_guard check README.md --json
python -m install_truth_guard check README.md --offline
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

Cargo と Docker の宣言は解析されますが、既定では未対応として通知されます。
`--strict-unsupported` を使うと失敗として扱えます。

## オプション

- `--json`: 機械可読な結果を出力します。
- `--allow-unpublished NAME`: 意図的に未公開のパッケージまたはイメージの宣言を許可します。
- `--ignore-ecosystem ECOSYSTEM`: レジストリ確認と出力の前に、指定したエコシステムの
  インストール宣言を除外します。複数回指定できます。例:
  `--ignore-ecosystem cargo --ignore-ecosystem docker`。
- `--strict-unsupported`: 未対応のエコシステムを失敗として扱います。
- `--timeout SECONDS`: レジストリ確認のタイムアウトを設定します。
- `--offline`: レジストリにアクセスせず、Markdown の解析だけを行います。
