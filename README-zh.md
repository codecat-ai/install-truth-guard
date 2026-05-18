# install-truth-guard

[English](README.md) | [中文](README-zh.md) | [日本語](README-ja.md)

`install-truth-guard` 是一个适合 CI 使用的 README 安装声明检查工具。它会解析 Markdown 中的包管理器命令，并对已支持的生态进行只读注册表查询，避免文档在产物发布前就宣称可以安装。

## 问题与动机

README 经常在软件包、镜像或命令真正发布前就加入安装命令。这会误导用户、破坏上手体验，也会让发布流程中的缺口直到有人在 CI 或评估时运行命令才暴露出来。`install-truth-guard` 提供一个小而安全的检查：读取 Markdown、识别常见安装命令，并报告这些声明当前是否真实。

## 状态

本仓库尚未作为软件包发布。请只使用克隆仓库后的本地运行方式。

## 功能

- 检测 `npx`、全局 `npm install`、`pnpm dlx`、`yarn dlx` 等 npm 风格声明。
- 检测 `pip install`、`uvx` 等 PyPI 风格声明。
- 默认把 Cargo 和 Docker 声明解析为未支持生态，也可使用严格模式让其失败。
- 支持 JSON 输出，便于 CI 自动化；也支持不访问注册表的离线解析。
- 支持允许有意未发布的名称，并可重复忽略指定生态，适合分阶段发布。

## 检查内容

已支持的注册表检查：

- npm 命令：npx、全局 npm install、pnpm dlx、yarn dlx。
- PyPI 命令：pip install、uvx。

默认会解析但尚未支持：

- Cargo install 命令。
- Docker pull 和 run 命令。

除非启用 `--strict-unsupported`，未支持声明只作为提示。

## 安装

目前尚未发布任何包管理器版本。请克隆仓库并在源码检出目录中运行 CLI：

```sh
git clone https://github.com/codecat-ai/install-truth-guard.git
cd install-truth-guard
python -m install_truth_guard check README.md
```

开发时，请在隔离的 Python 环境中从本地检出安装开发依赖后再运行测试。

## 快速开始

```sh
python -m install_truth_guard check README.md
python -m install_truth_guard check README.md --json
python -m install_truth_guard check README.md --offline
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

## 示例

检查 README，同时忽略有意记录但暂不强制校验的 Docker 声明：

```sh
python -m install_truth_guard check README.md --ignore-ecosystem docker
```

把未支持的 Cargo 或 Docker 声明视为 CI 失败：

```sh
python -m install_truth_guard check README.md --strict-unsupported
```

在分阶段发布期间允许一个有意尚未发布的包名：

```sh
python -m install_truth_guard check README.md --allow-unpublished example-package
```

## 配置

目前所有配置都通过 CLI 标志传入：

- `--json`：输出机器可读的结果。
- `--allow-unpublished NAME`：允许一个有意尚未发布的包或镜像声明。
- `--ignore-ecosystem ECOSYSTEM`：在注册表检查和输出前忽略指定生态的安装声明。可重复使用，例如 `--ignore-ecosystem cargo --ignore-ecosystem docker`。
- `--strict-unsupported`：将不支持的生态视为失败。
- `--timeout SECONDS`：设置注册表超时时间。
- `--offline`：只解析 Markdown，不访问注册表。

路线图中计划加入可复用的项目策略文件。

## 开发

在隔离的 Python 环境中从本地检出安装后运行：

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## 测试

测试套件覆盖 Markdown 命令提取、已支持与未支持生态处理、JSON 输出、离线模式、允许列表行为，以及 `--ignore-ecosystem` 等 CLI 过滤逻辑。

## 安全

本工具不会执行 README 中的命令。注册表检查只是对 npm 和 PyPI 元数据发起只读 HTTP 请求。

## 路线图

成熟度：`maintenance`

计划节奏：每 2-4 周维护一次；如果注册表检查、README 真实性或 CI 出现问题，则优先处理。

现在：

- 在软件包注册表发布获得明确批准并完成验证前，保持源码检出用法文档真实准确。
- 维护符合组合标准的路线图和节奏说明。

下一步：

- 为多个 README 文件中的重复允许/忽略策略添加文档化配置文件。
- 为 CI 运行添加 GitHub Actions annotation 输出。
- 扩展示例，展示 npm、PyPI、Cargo、Docker 声明在离线模式下的处理方式。

以后：

- 评估安全的只读 Cargo 和 Docker 存在性检查。
- 为翻译版 README 和文档目录添加多文件扫描模式。
- 当剩余路线图项目只剩可选增强时，评估是否转入 `mature-low-frequency`。

维护触发器、节奏复审说明和完成复审规则见 [ROADMAP.md](ROADMAP.md)。

## 贡献

欢迎提交 issue 和聚焦的小型 pull request。CLI 或解析器行为变更请添加行为测试；除非包已经发布并验证，否则不要记录包管理器安装命令。

## 许可证

MIT。见 [LICENSE](LICENSE)。

本项目在 AI 协助下编写和维护，并以可读文档与测试作为事实来源。
