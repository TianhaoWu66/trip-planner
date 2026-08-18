# -*- coding: utf-8 -*-
"""Build an A4 PDF from a markdown travel guide.

Pipeline: markdown -> HTML (md_to_html.py) -> Edge headless print-to-pdf
-> QA (pdfplumber page count / size). Prints the output path on success.

Usage:
    python build_pdf.py input.md output.pdf [--title "Guide Title"]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

from md_to_html import md_to_html

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/microsoft-edge",
    "/usr/bin/microsoft-edge-stable",
]
EDGE_NAMES = ["msedge", "microsoft-edge", "microsoft-edge-stable"]


def find_edge():
    for c in EDGE_CANDIDATES:
        if os.path.exists(c):
            return c
    for name in EDGE_NAMES:
        p = shutil.which(name)
        if p:
            return p
    return None


def qa_pdf(pdf_path, min_size=10_000):
    try:
        import pdfplumber
    except ImportError:
        return None
    pages = pdfplumber.open(pdf_path).pages
    return len(pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md")
    ap.add_argument("output_pdf")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    if not os.path.exists(args.input_md):
        sys.exit("input markdown not found: " + args.input_md)
    edge = find_edge()
    if not edge:
        sys.exit("Edge not found; install Microsoft Edge or use another PDF pipeline.")

    workdir = tempfile.mkdtemp(prefix="trip-planner-")
    try:
        html_path = os.path.join(workdir, "guide.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(md_to_html(args.input_md, args.title))
        profile = os.path.join(workdir, "edge-profile")
        cmd = [
            edge, "--headless=new", "--disable-gpu", "--no-first-run",
            "--disable-extensions", "--no-pdf-header-footer",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={os.path.abspath(args.output_pdf)}",
            "file:///" + html_path.replace("\\", "/"),
        ]
        subprocess.run(cmd, check=False, timeout=120)
        if not os.path.exists(args.output_pdf) or os.path.getsize(args.output_pdf) < 1_000:
            sys.exit("PDF not produced by Edge headless; check Edge invocation.")
        pages = qa_pdf(args.output_pdf)
        print(f"PDF written: {os.path.abspath(args.output_pdf)}")
        if pages:
            print(f"QA ok: {pages} page(s)")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
