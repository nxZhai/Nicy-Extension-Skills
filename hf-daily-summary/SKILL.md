---
name: hf-daily-summary
description: Fetch daily trending papers from Hugging Face (hf.co/papers), extract their paper IDs, and process them using arxiv-pipe-papers to download PDFs, extract LaTeX sources, and generate summaries. Triggers when user says "daily papers", "Hugging Face daily", "hf daily papers", "今日热门论文", "Hugging Face 每日热门", or wants to summarize today's trending AI papers from Hugging Face.
argument-hint: "[LIMIT] [SAVE_DIR]"
allowed-tools: Bash(*), Read, Write, Glob, Grep
---

# Hugging Face Daily Papers Summary

Fetch and summarize the daily trending papers from Hugging Face.

## Input Format

You may receive two optional arguments:
- **$0**: Number of papers to fetch (default: 10, max: 100)
- **$1**: Local directory for storing downloaded files (default: `hf-daily-papers/`)

## Workflow

### Step 1: Fetch Daily Papers from Hugging Face API

Get the trending papers from Hugging Face:

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/daily_papers?p=0&limit=${LIMIT:-10}&sort=trending"
```

The `$HF_TOKEN` environment variable must be set. If not set, inform the user to set it first.

### Step 2: Parse Response and Extract Paper IDs

The API returns a JSON array where each entry has a `paper` object containing the paper data. For each entry, extract `paper.id` — this is the arXiv-style ID (e.g., `2412.20138`).

Example response structure:
```json
[
  {
    "paper": {
      "id": "2412.20138",
      "title": "Paper Title",
      "authors": [...],
      ...
    },
    "publishedAt": "2024-12-28T07:54:06.000Z",
    "title": "Paper Title"
  },
  ...
]
```

Build a comma-separated list of paper IDs, e.g., `2412.20138,2403.08299,2603.15031`

### Step 3: Call arxiv-pipe-papers Skill

Use the Skill tool to invoke `arxiv-pipe-papers` with the extracted paper IDs:

```
Skill: arxiv-pipe-papers
Args: <comma-separated-paper-ids> <save_dir>
```

For example, if you extracted `2412.20138,2403.08299,2603.15031` and want to save to `hf-daily-papers/`:

```
Skill: arxiv-pipe-papers
Args: "2412.20138,2403.08299,2603.15031" "hf-daily-papers/"
```

### Step 4: Report Results

After arxiv-pipe-papers completes, summarize:
- Number of papers processed
- Output directory location
- Any failures or errors

## Error Handling

- **HF_TOKEN not set**: Tell the user to export HF_TOKEN before running
- **API request failed**: Report error and suggest checking network or token validity
- **No papers returned**: Inform user and suggest trying a different date or filter
- **arxiv-pipe-papers failed**: Report partial results if any papers were processed

## Example

User says: "Summarize today's trending papers from Hugging Face"

Assistant:
1. Fetches top 10 trending papers
2. Extracts IDs: `2412.20138, 2403.08299, 2603.15031, ...`
3. Calls arxiv-pipe-papers to download and summarize each
4. Reports: "Processed 10 papers, saved to hf-daily-papers/"
