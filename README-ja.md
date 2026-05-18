# install-truth-guard

[English](README.md) | [中文](README-zh.md) | [日本語](README-ja.md)

`install-truth-guard` は README のインストール手順が実際の公開状態と合っているかを確認する CI 向けツールです。Markdown 内のパッケージマネージャーコマンドを解析し、対応済みのエコシステムについて読み取り専用のレジストリ確認を行います。

## 問題と動機

README には、パッケージ、イメージ、コマンドが実際に公開される前にインストール手順が追加されることがあります。その結果、利用者を混乱させ、導入体験を壊し、CI や評価時に誰かがコマンドを試すまでリリース手順の抜けが見えにくくなります。`install-truth-guard` は Markdown を読み、よく使われるインストールコマンドを認識し、その説明が現在の公開状態と一致しているかを安全に報告します。

## 状態

このリポジトリはまだパッケージとして公開されていません。クローンしたローカル環境で利用してください。

## 機能

- `npx`、グローバル `npm install`、`pnpm dlx`、`yarn dlx` などの npm 系の宣言を検出します。
- `pip install`、`uvx` などの PyPI 系の宣言を検出します。
- Cargo と Docker の宣言は既定で未対応エコシステムとして解析し、必要に応じて厳格モードで失敗扱いにできます。
- CI 自動化向けの JSON 出力と、レジストリへアクセスしないオフライン解析に対応します。
- 段階的なリリースに使えるよう、有意に未公開の名前の許可と、エコシステム単位の繰り返し除外に対応します。

## 確認内容

対応済みのレジストリ確認：

- npm コマンド: npx、グローバル npm install、pnpm dlx、yarn dlx。
- PyPI コマンド: pip install、uvx。

既定では解析されるが未対応のもの：

- Cargo install コマンド。
- Docker pull と run コマンド。

未対応の宣言は、`--strict-unsupported` を有効にしない限り通知扱いです。

## インストール

パッケージレジストリ向けのリリースはまだ公開されていません。リポジトリをクローンし、ソースチェックアウトから CLI を実行してください。

```sh
git clone https://github.com/codecat-ai/install-truth-guard.git
cd install-truth-guard
python -m install_truth_guard check README.md
```

開発時は、隔離された Python 環境でローカルチェックアウトから開発依存関係をインストールしてからテストを実行します。

## クイックスタート

```sh
python -m install_truth_guard check README.md
python -m install_truth_guard check README.md --json
python -m install_truth_guard check README.md --offline
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

## 例

意図的に記載しているものの、まだ強制確認しない Docker 宣言を除外して README を確認します。

```sh
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

未対応の Cargo または Docker 宣言を CI 失敗として扱います。

```sh
python -m install_truth_guard check README.md --strict-unsupported
```

段階的リリース中に、意図的に未公開のパッケージ名を 1 つ許可します。

```sh
python -m install_truth_guard check README.md --allow-unpublished example-package
```

## 設定

現在の設定はすべて CLI フラグで指定します。

- `--json`: 機械可読な結果を出力します。
- `--allow-unpublished NAME`: 意図的に未公開のパッケージまたはイメージの宣言を許可します。
- `--ignore-ecosystem ECOSYSTEM`: レジストリ確認と出力の前に、指定したエコシステムのインストール宣言を除外します。複数回指定できます。例: `--ignore-ecosystem cargo --ignore-ecosystem docker`。
- `--strict-unsupported`: 未対応のエコシステムを失敗として扱います。
- `--timeout SECONDS`: レジストリ確認のタイムアウトを設定します。
- `--offline`: レジストリにアクセスせず、Markdown の解析だけを行います。

再利用可能なプロジェクトポリシーファイルはロードマップに含まれています。

## 開発

隔離された Python 環境でローカルチェックアウトからインストールし、次を実行します。

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## テスト

テストスイートは、Markdown コマンド抽出、対応済みおよび未対応エコシステムの扱い、JSON 出力、オフラインモード、許可リスト、`--ignore-ecosystem` などの CLI フィルタリングをカバーします。

## 安全性

このツールは README 内のコマンドを実行しません。レジストリ確認は npm と PyPI メタデータへの読み取り専用 HTTP リクエストです。

## ロードマップ

成熟度: `maintenance`

予定 cadence: 2-4 週ごとの保守に加え、レジストリ確認、README の正確性、CI に問題が出た場合は緊急対応します。

現在：

- パッケージレジストリ公開が明示的に承認され検証されるまで、ソースチェックアウトでの利用手順を正確に保ちます。
- ポートフォリオ標準のロードマップと cadence メモを維持します。

次：

- 複数 README に共通する許可/除外ポリシー向けの設定ファイルを文書化します。
- CI 実行向けに GitHub Actions annotation 出力を追加します。
- npm、PyPI、Cargo、Docker 宣言のオフライン処理例を増やします。

後で：

- 安全な読み取り専用 Cargo と Docker 存在確認を評価します。
- 翻訳 README とドキュメントフォルダ向けの複数ファイルスキャンを追加します。
- 残るロードマップ項目が任意の改善だけになったら、`mature-low-frequency` への移行を検討します。

保守トリガー、cadence レビュー、完了レビュー規則は [ROADMAP.md](ROADMAP.md) を参照してください。

## コントリビューション

Issue と焦点を絞った pull request を歓迎します。CLI やパーサーの動作を変える場合は、振る舞いを確認するテストを追加してください。パッケージが実際に公開され検証されるまでは、パッケージマネージャーのインストールコマンドを文書化しないでください。

## ライセンス

MIT。詳しくは [LICENSE](LICENSE) を参照してください。

このプロジェクトは AI の支援を受けて作成・保守されており、読みやすいドキュメントとテストを事実の基準にしています。
