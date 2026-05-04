# install-truth-guard

`install-truth-guard` 是一个适合 CI 使用的 README 安装声明检查工具。它会解析
Markdown 中的包管理器命令，并对已支持的生态进行只读注册表查询，避免文档在产物
发布前就宣称可以安装。

## 状态

本仓库尚未作为软件包发布。请只使用克隆仓库后的本地运行方式。

## 本地使用

在仓库克隆目录中运行：

```sh
python -m install_truth_guard check README.md
python -m install_truth_guard check README.md --json
python -m install_truth_guard check README.md --offline
```

已支持 npm 与 PyPI 查询。Cargo 和 Docker 声明会被解析，但默认只作为不支持项报告；
使用 `--strict-unsupported` 可让它们导致失败。
