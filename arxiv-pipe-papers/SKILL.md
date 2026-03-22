---
name: arxiv-pipe-papers
description: Process multiple arXiv papers by parallel calling arxiv-pipe skill for each paper ID or URL. Use when the user provides a comma-separated list of arXiv IDs or URLs (e.g., "1706.03762, 2603.18656, https://arxiv.org/abs/1706.03762"). This skill triggers when the user wants to analyze multiple papers at once, compare papers, or generate a batch summary of several arXiv papers. Each paper is processed sequentially using the arxiv-pipe workflow.
argument-hint: "[ARXIV_IDS_OR_URLS] [SAVE_DIR]"
allowed-tools: Bash(*), Read, Write, Glob, Grep, WebSearch, WebFetch
---

# Arxiv-pipe-papers

Process multiple arXiv papers by parallel applying the arxiv-pipe workflow to each paper.

## Input Format

You will receive two arguments:

- **$0**: Comma-separated list of arXiv IDs or URLs. Accepts formats like:
  - Single ID: `1706.03762`
  - Multiple IDs: `1706.03762, 2603.18656, 2301.12345`
  - URLs: `https://arxiv.org/abs/1706.03762, https://arxiv.org/pdf/2603.18656`
  - Mixed: `1706.03762, https://arxiv.org/abs/2603.18656`
- **$1**: Optional local directory for storing downloaded files. Default: `papers/`

## Workflow

### Step 1: Processing Papers Using arxiv-pipe

1. Split **$0** into individual paper IDs (e.g., `2603.18656`, `1706.03762`, ...)
2. Launch parallel sub-agents (preferably `arxiv-paper-parser`) to concurrently process each paper via the `arxiv-pipe` skill
   - Pass the paper ID as the first argument
   - Pass **$1** as the second argument

### Step 2: Generate Combined Report

After all papers are processed, generate a summary table:

```
| # | arXiv ID | Title | PDF | TEX | BIB | Summary |
|---|----------|-------|-----|-----|-----|---------|
| 1 | 1706.03762 | ... | x MB | x KB | x KB | x KB |
| 2 | 2603.18656 | ... | x MB | x KB | x KB | x KB |
```

### Step 3: Output Location

All files are saved to **$1** (or default `papers/`):
- PDF: `{output_dir}/{id}.pdf`
- TEX: `{output_dir}/{id}/{id}_tex.txt`
- BIB: `{output_dir}/{id}/{id}_bib.txt`
- Summary: `{output_dir}/{id}.md`

## Error Handling

- **Invalid arXiv ID**: Skip and report, continue with remaining papers
- **Download failure**: Log error, continue with next paper
- **Missing LaTeX source**: Generate summary with available content, note limitations
- **Duplicate IDs**: Automatically deduplicate, process each only once
- **scripts/download_arxiv_paper.py not found**: Locate the script in the `arxiv-pipe` skill's installation directory.

## Example

Input: `1706.03762, 2603.18656, 2301.12345` (save to `papers/`)

Output:
```
Processing 3 papers:
[1/3] 1706.03762 - Downloading... Done
[1/3] 1706.03762 - Generating summary... Done
[2/3] 2603.18656 - Downloading... Done
[2/3] 2603.18656 - Generating summary... Done
[3/3] 2301.12345 - Downloading... Failed (invalid ID)
[3/3] 2301.12345 - Skipped

Summary table:
| # | arXiv ID | Title | PDF | TEX | BIB | Summary |
|---|----------|-------|-----|-----|-----|---------|
| 1 | 1706.03762 | Attention Is All You Need | 2.1 MB | 45 KB | 8 KB | 12 KB |
| 2 | 2603.18656 | LLaMA | 1.8 MB | 38 KB | 6 KB | 10 KB |

Files saved to: papers/
```
