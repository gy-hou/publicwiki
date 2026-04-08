---
date: 2026-03-16
authors:
  - gy-hou
categories:
  - AI 工具
slug: karpathy-ai-auto-research-trendr
tags:
  - Karpathy
  - TrendR
  - Agentic RAG
---

# Karpathy AI 自动实验启发：让 AI 自动写综述

> 让 AI agent 自己搜索、筛选、精读、写综述，再自动沉淀到 Obsidian。

<!-- more -->

Karpathy 开源了 `autoresearch`，核心思路是让 AI agent 自己改代码、跑训练、评估结果。

我的需求更偏研究效率：自动写文献综述、持续总结最新动态。  
所以我做了 **TrendR**，也感谢大家支持 2.0 版本更新。

你只要说一句：

> 调研 agentic RAG 2025 最新进展

然后它会自己完成这条链路：

- 并行搜索 9 个学术数据库（arXiv / Semantic Scholar 等）
- 自动评分（1-5）、去重、筛选候选论文
- 精读高分论文，提取结构化笔记（研究问题 / 方法 / 结果 / 局限）
- 生成完整文献综述（分类框架 + 研究空白分析 + BibTeX）
- 自动归档到 Obsidian，论文池跨项目持久化

想查之前做过的研究？直接跟 AI 说“查之前搜过关于 XXX 的论文”，可以秒级返回。要看详细分析，去 Obsidian 打开对应论文卡片就行。

---

## 实测（今天刚跑完）

- 主题：agentic RAG 2025 最新进展
- 搜到 81 篇候选论文
- 精读 11 篇，生成结构化笔记 + 对比矩阵
- 产出 14KB 完整综述
- 等待时间：约 30 分钟

---

已开源：[gy-hou/trendr](https://github.com/gy-hou/trendr)，几分钟就能配好。

如果你有 Claude Opus 4.6 API 或 Semantic Scholar API，效果会更好。  
也可以直接让 OpenClaw 这样切换：

```text
将 agent lead API 切换为 Claude Opus 4.6 key XXXXX；
Semantic Scholar API key XXXX。
```

如果你有改进想法，欢迎 PR。
