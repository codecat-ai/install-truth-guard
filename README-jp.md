# install-truth-guard

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
```

Cargo と Docker の宣言は解析されますが、既定では未対応として通知されます。
`--strict-unsupported` を使うと失敗として扱えます。
