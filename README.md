# Openresource-Wiki

[![Deploy](https://github.com/gy-hou/openresource-wiki/actions/workflows/deploy.yml/badge.svg)](https://github.com/gy-hou/openresource-wiki/actions/workflows/deploy.yml)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> AI 工具、Prompts、Skills 开源分享站

🌐 **在线访问**：https://gy-hou.github.io/openresource-wiki/

## 这是什么

一个开源的 AI 知识库，收录了：

- 📝 **博客** — 小红书热帖文字版、AI 热点解读、实操教程
- 💡 **Prompt 库** — 精心调试的 Prompt 合集
- 🛠️ **Skills 库** — Claude Skills 和自动化模板
- 🧰 **工具箱** — AI 工具推荐和对比
- 🚀 **项目** — 开源项目展示

## 本地开发

```bash
# 安装依赖（自动创建/修复 .venv）
make install

# 本地预览（自动选择空闲端口）
make serve

# 构建
make build

# 查看所有命令
make help
```

`make serve` 会优先使用项目内 `.venv` 的 `mkdocs`，避免全局环境冲突；如果 `8000` 端口被占用，会自动尝试 `8001`、`8002`...

## 贡献

欢迎贡献内容！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

内容部分采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 协议。
代码部分采用 MIT 协议。
