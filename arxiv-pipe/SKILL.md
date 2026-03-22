---
name: arxiv-pipe
description: Download PDF and LaTeX source files for a paper from arXiv, perform a comprehensive reading and analysis, and generate a detailed summary note. use when the user provides a URL or ID of an arxiv paper(e.g. "1706.03762", "arxiv.org/abs/1706.03762", "arxivg.org/pdf/1706.03762", "https://arxiv.org/abs/1706.03762", "https://arxiv.org/pdf/1706.03762")
argument-hint: "[ARXIV_ID_OR_URL] [SAVE_DIR]"
allowed-tools: Bash(*), Read, Write, Glob, Grep, WebSearch, WebFetch
---

# Arxiv-pipe

You will be given two arguments: 

- **$0**, a URL or ID of an arxiv paper
- **$1**, optional, local directory for storing downloaded files. Default: `papers/`

Download PDF and LaTeX scource files for **$0**, analysis, and generate a detailed summary note, and save them into **$0**.

## Workflow 1: Downlad PDF and LaTeX source files

Extract the paper ID (e.g., 1706.03762) from **$0**. Use the [Download Script](scripts/download_arxiv_paper.py) to download PDF and LaTeX source files, process the LaTeX source code, and then save the results to the specified **$1** directory.

```
python download_arxiv_paper.py <arxiv_id> [-o DIR] [--force]
```

| Argument | Default | Description |
|---|---|---|
| `arxiv_id` (required) | — | arXiv paper ID |
| `-o`, `--output-dir` | `papers/` | Output directory |
| `--force` | off | Re-download even if cached |

Output: 

- `pdf`: "$1/{id}.pdf"
- `tex_txt`: "$1/{id}/{id}_tex.txt"
- `bib_txt`: "$1/{id}/{id}_bib.txt"

## Workflow 2: Generate Chinese Summary

**Important**: Use Write tool to write markdown directly to `.md` file. Do NOT use Python heredoc or temp scripts.

### Step1 : Read ann summary

Read `tex_txt` and `bib_tex` for structured analysis data, then generate markdown with these sections:
- Header links (arXiv ID $1, GitHub Link if found in `tex_txt`)
- 研究背景与动机 (3-5 sentences Chinese)
- 摘要 (full abstract)
- 论文总结 (2-4 paragraphs Chinese)
- 创新范式分析（For details, see [reference.md](research_paradigms_reference.md)）
- 方法论详解
  - **核心方法流程** (step-by-step in Chinese)：在描述每个步骤时将相关公式自然地嵌入到对应步骤的上下文中，不要单独罗列公式
- 实验分析
  - **实验类型分类**: SOTA / Ablation / Generalization / Efficiency 等
  - **使用的数据集** (in Chinese)
- 实验资源
  - **Backbone**: 使用的基础模型及版本
  - **Baseline**: 对比的基线方法列表，标注出处年份
  - **数据集**: 使用的评估基准及规模
  - **训练资源**: GPU 型号 × 数量（如 4×NVIDIA A100 80GB），标注训练/推理时长（从实验、附录章节查找是否有相关内容）
  - **超参数**: 关键超参数设置（如 learning rate, batch size, epochs, 特有超参）
- 关键贡献 (3-5 bullets)
- 主要实验结果
- 局限性与未来工作
- 参考论文 (读取 `bib_txt`, plain text: Author. "Title." Venue, Year.)

**要求**:
1. 所有中文内容用中文撰写
2. GitHub 链接在开头部分添加
3. 核心公式必须融入方法流程的对应步骤中，不要单独罗列或硬编码
4. Baseline 和数据集在最后以纯文本列表形式列出，不使用 markdown link 格式
5. 实验必须分类（SOTA/消融/泛化/效率等）

### Step 2: Save Summary

Use Write tool to write markdown to `$1/{id}.md`.

### Step 3: Report

```
| arXiv ID | Title | PDF | TEX | BIB | Summary |
|----------|-------|-----|-----|-----|---------|
| xxx      | ...   | x MB| x KB| x KB| x KB   |
```

## Error Handling

- **arxiv-to-prompt 未安装**: 提示 `pip install arxiv-to-prompt`
- **文件已存在**: 跳过下载但覆盖 .md（重新生成）