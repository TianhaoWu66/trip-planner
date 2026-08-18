# -*- coding: utf-8 -*-
"""Convert a markdown travel-guide file to print-ready HTML (A4, Chinese-friendly).

Supports: h1-h3, blockquote, tables, bullet lists, hr, inline code/bold,
and simple ```mermaid flowchart LR``` blocks (rendered as a linear flow).
"""
import re
import html
import sys

CSS = '''
@page { size: A4; margin: 13mm 11mm 15mm 11mm; }
* { box-sizing: border-box; }
body { font-family: "Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif; font-size: 10.5pt; color:#1f2937; line-height:1.55; margin:0; }
h1 { font-size: 19pt; color:#b45309; border-bottom:3px solid #f59e0b; padding-bottom:6px; margin:0 0 12px; }
h2 { font-size: 13.5pt; color:#92400e; margin:18px 0 8px; padding:5px 10px; background:#fff7ed; border-left:5px solid #f59e0b; page-break-after:avoid; }
h3 { font-size: 11.5pt; color:#b45309; margin:12px 0 6px; page-break-after:avoid; }
p { margin:6px 0; }
table { width:100%; border-collapse:collapse; margin:8px 0; font-size:9pt; }
th { background:#ffedd5; color:#7c2d12; font-weight:600; }
td, th { border:1px solid #d6d3d1; padding:4px 6px; vertical-align:top; text-align:left; }
tr { page-break-inside:avoid; }
blockquote { background:#f8fafc; border-left:4px solid #94a3b8; margin:8px 0; padding:6px 10px; color:#475569; font-size:9.5pt; }
ul { margin:6px 0 6px 18px; padding:0; }
li { margin:2px 0; }
strong { color:#9a3412; }
hr { border:none; border-top:1px dashed #d6d3d1; margin:12px 0; }
code { background:#f1f5f9; padding:0 3px; border-radius:3px; font-size:9pt; }
.flow { display:flex; flex-wrap:wrap; align-items:center; gap:5px 3px; margin:10px 0; padding:10px; background:#fafaf9; border:1px solid #e7e5e4; border-radius:8px; }
.flow .node { background:#fff7ed; border:1px solid #f59e0b; border-radius:6px; padding:4px 8px; font-size:9pt; font-weight:600; color:#7c2d12; white-space:pre-line; text-align:center; }
.flow .edge { color:#b45309; font-size:8.5pt; white-space:nowrap; }
.flow .edge::before { content:"\\2192 "; }
.footer { text-align:center; color:#a8a29e; font-size:8.5pt; margin-top:16px; border-top:1px solid #e7e5e4; padding-top:6px; }
'''


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s


def render_table(rows):
    parsed = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip('|').split('|')]
        parsed.append(cells)
    body = [c for c in parsed if not (len(c) == len(parsed[0]) and all(re.fullmatch(r':?-{2,}:?', x or '') for x in c))]
    if not body:
        return ''
    header, rows2 = body[0], body[1:]
    thead = '<thead><tr>' + ''.join(f'<th>{inline(h)}</th>' for h in header) + '</tr></thead>'
    tbody = '<tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>' for row in rows2) + '</tbody>'
    return f'<table>{thead}{tbody}</table>'


def render_flow(lines):
    """Parse simple mermaid flowchart LR lines into an ordered flow strip."""
    node_re = re.compile(r'^\s*([A-Za-z0-9_]+)\s*\[(.*?)\]\s*-->\s*(?:\|(.*?)\|)?\s*([A-Za-z0-9_]+)\s*\[(.*?)\]\s*$')
    nodes, edges = {}, []
    for line in lines:
        m = node_re.match(line)
        if not m:
            continue
        a, la, lab, b, lb = m.groups()
        nodes.setdefault(a, la)
        nodes.setdefault(b, lb)
        edges.append((a, b, lab or ''))
    if not edges:
        return '<div class="flow"></div>'
    # Walk the chain from the first edge start; append stragglers in order.
    order, seen = [], set()
    start = edges[0][0]
    queue = [start]
    while queue:
        cur = queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        order.append(cur)
        for a, b, _ in edges:
            if a == cur and b not in seen:
                queue.append(b)
    for a, b, _ in edges:
        for n in (a, b):
            if n not in seen:
                seen.add(n)
                order.append(n)
    parts = []
    for n in order:
        parts.append(f'<span class="node">{html.escape(nodes.get(n, n))}</span>')
        for a, b, lab in edges:
            if a == n and b in order and order.index(b) == order.index(n) + 1:
                parts.append(f'<span class="edge">{html.escape(lab)}</span>')
    return '<div class="flow">' + ''.join(parts) + '</div>'


def parse(md_text):
    lines = md_text.split('\n')
    out, i, in_mermaid = [], 0, False
    mermaid_buf = []
    while i < len(lines):
        line = lines[i]
        if line.startswith('```mermaid'):
            in_mermaid, i = True, i + 1
            mermaid_buf = []
            continue
        if in_mermaid:
            if line.startswith('```'):
                out.append(render_flow(mermaid_buf))
                in_mermaid = False
            else:
                mermaid_buf.append(line)
            i += 1
            continue
        if line.startswith('# '):
            out.append(f'<h1>{inline(line[2:].strip())}</h1>')
        elif line.startswith('## '):
            out.append(f'<h2>{inline(line[3:].strip())}</h2>')
        elif line.startswith('### '):
            out.append(f'<h3>{inline(line[4:].strip())}</h3>')
        elif line.strip() == '---':
            out.append('<hr>')
        elif line.startswith('> '):
            q = []
            while i < len(lines) and lines[i].startswith('> '):
                q.append(inline(lines[i][2:].strip()))
                i += 1
            out.append('<blockquote>' + '<br>'.join(q) + '</blockquote>')
            continue
        elif line.startswith('|'):
            tbl = []
            while i < len(lines) and lines[i].startswith('|'):
                tbl.append(lines[i])
                i += 1
            out.append(render_table(tbl))
            continue
        elif line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append(inline(lines[i][2:].strip()))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>')
            continue
        elif line.strip():
            out.append(f'<p>{inline(line.strip())}</p>')
        i += 1
    return '\n'.join(out)


def md_to_html(md_path, title=None):
    text = open(md_path, encoding='utf-8').read()
    if title is None:
        m = re.search(r'^#\s+(.+)$', text, re.M)
        title = m.group(1).strip() if m else '旅行攻略'
    body = parse(text)
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}<div class="footer">{html.escape(title)} · 数据核实时间以攻略内标注为准</div></body></html>'''


if __name__ == '__main__':
    md_path, out_path = sys.argv[1], sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md_to_html(md_path, title))
    print('HTML written:', out_path)

