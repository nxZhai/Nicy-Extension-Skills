#!/usr/bin/env python3
"""Download an arXiv PDF and extract flattened LaTeX via arxiv-to-prompt."""

import argparse
import json
import pathlib
import subprocess
import sys
import urllib.request

from arxiv_to_prompt import process_latex_source

CACHE_DIR = pathlib.Path.home() / ".cache" / "arxiv-to-prompt"


def download_paper(
    aid: str,
    output_dir: pathlib.Path,
    skip_existing: bool = True,
) -> dict:
    """Download PDF + extract flattened LaTeX + collect bib for one paper.

    Layout: {id}.pdf and {id}.md in output_dir/, rest in output_dir/{id}/.
    """
    result = {"id": aid}

    # --- PDF → output_dir/{id}.pdf ---
    pdf_path = output_dir / f"{aid}.pdf"
    if skip_existing and pdf_path.exists() and pdf_path.stat().st_size > 10240:
        print(f"[skip] PDF exists: {pdf_path}")
    else:
        req = urllib.request.Request(
            f"https://arxiv.org/pdf/{aid}.pdf",
            headers={"User-Agent": "arxiv-pipe/1.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            pdf_path.write_bytes(r.read())
        print(f"[done] PDF: {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
    result["pdf_path"] = str(pdf_path)

    # --- Flattened LaTeX via arxiv-to-prompt → output_dir/{id}/{id}.tex ---
    sub_dir = output_dir / aid
    sub_dir.mkdir(parents=True, exist_ok=True)
    tex_path = sub_dir / f"{aid}_tex.txt"
    bib_path = sub_dir / f"{aid}_bib.txt"

    if skip_existing and tex_path.exists() and tex_path.stat().st_size > 0:
        print(f"[skip] TEX exists: {tex_path}")
    else:
        try:
            # Get LaTeX source without comments
            latex_source = process_latex_source(
                aid,
                keep_comments=False,
                use_cache=skip_existing,
            )
            tex_path.write_text(latex_source, encoding="utf-8")
            print(f"[done] TEX: {tex_path} ({tex_path.stat().st_size // 1024} KB)")
        except FileNotFoundError:
            print(
                f"[error] Failed to get LaTeX source for {aid}",
                file=sys.stderr,
            )
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print(f"[warn] arxiv-to-prompt timed out for {aid}", file=sys.stderr)
            result["tex_path"] = None
            result["bib_path"] = None
            return result
    result["tex_path"] = str(tex_path)

    # --- Collect .bib from arxiv-to-prompt cache ---
    cache_paper_dir = CACHE_DIR / aid
    if not bib_path.exists() and cache_paper_dir.exists():
        bib_files = sorted(cache_paper_dir.rglob("*.bib"))
        if bib_files:
            bib_contents = []
            for bf in bib_files:
                bib_contents.append(bf.read_text(encoding="utf-8", errors="replace"))
            bib_path.write_text("\n".join(bib_contents), encoding="utf-8")
            print(
                f"[done] BIB: {bib_path} ({bib_path.stat().st_size // 1024} KB, {len(bib_files)} sources)"
            )
    result["bib_path"] = str(bib_path) if bib_path.exists() else None
    result["cache_dir"] = str(cache_paper_dir)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Download an arXiv PDF and extract LaTeX via arxiv-to-prompt."
    )
    parser.add_argument("arxiv_id", help="arXiv paper ID (e.g., 1706.03762)")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="papers",
        help="Output directory (default: papers/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if files already exist",
    )
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = download_paper(
        args.arxiv_id,
        output_dir,
        skip_existing=not args.force,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
