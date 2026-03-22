# Nicy-Extension-Skills

> 自用科研 SOP 构建的 skills。

## Skills

### 论文处理

- `arxiv-pipe` 论文阅读总结管道。首先从 arxiv 上下载论文的 pdf、targ.gz 源文件，然后对 tex 源代码进行直接阅读、分析公式，输出 markdown 格式的论文总结。
  - `query-or-arxiv-id` 位置参数，搜索内容或arxiv 论文 ID。
  - `- dir: PATH` （可选，defult：`/papers`）论文下载位置

- `humanizer` 去除 AI 生成文本的痕迹，使文字读起来更自然 human-written。
  - argument: `[待润色文本]`

### Idea 探索

- `idea-discovery` 完整 idea 发现管道。串联 research-lit → idea-creator → novelty-check → research-review → research-refine，从宽泛研究方向出发，输出经验证的 IDEA_REPORT.md 和细化后的研究方案。
  - argument: `[研究方向]`

- `idea-creator` 在给定研究方向上生成并排序研究 idea，结合文献调研、可行性分析和 GPU pilot 验证。
  - argument: `[研究方向]`
  - 可选参数：`— pilot budget: Nh per idea, Nh total`

- `novelty-check` 查新：验证研究 idea 是否已在文献中出现过。通过多源检索（arXiv、Google Scholar、顶会）逐一核实核心技术创新点。
  - argument: `[method-or-idea-description]`

### 文献调研

- `research-lit` 搜索并分析研究论文，查找 related work，总结关键 ideas。支持 Zotero、Obsidian、本地 PDF 库和 Web 多源检索。
  - argument: `[paper-topic-or-url]`
  - 可选参数：`— sources: zotero,local,web,all`，`— arxiv download: true`

- `research-review` 通过 Codex MCP 调用 GPT 对研究 idea 进行深度批判性评审，输出结构化的评审意见和改进建议。

- `research-refine` 将模糊的研究方向细化为 problem-anchored、elegant、frontier-aware 的方法方案。经多轮 GPT-5.4 review 迭代，直到方案足够具体可实现。
  - 无位置参数，直接在对话中传入模糊的研究方向或初步方案

## How to create a Skill?

Skill can include multiple files in their directory.

```bash
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

A `SKILL.md` contains two types of content: **Reference content** and **Task conten**.  

**Reference content**

- `name` dispaly name for the skill.
- `description` what the skill does and when to use it.
- `argument-hint` hint shown during autocomplete to indicate expected arguments.
- `disable-model-invocation` (bool) set to `true` to prevent Claude from automatically loading this skill.
- `allowed-tools` tools claude can use without aksing permission when this skill is active.
  - Read, Grep, Glob, Write, Bash

- `context` set to `fork` to run in a forked subagent context.

## Claude Code's Bundled skills

- `/simplify [focus]` review your recently changed files fr code reuse, quality, and efficiency issues, then fix them. spawns 3 review agents in parallel, aggregates their findings, and applies fixes. Pass text to focus on specific concerns: `/simplify focus on memory efficiency`.

## Reference

- [Claude Code Docs](https://code.claude.com/docs/zh-CN/skills)
- [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
- [humanizer](https://github.com/blader/humanizer)

