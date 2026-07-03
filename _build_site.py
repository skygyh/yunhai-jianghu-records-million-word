#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import html
import re

BASE = Path(__file__).resolve().parent
SITE = BASE / "site"
BOOK_TITLE = "云海江湖录·百万字长篇版"
ORDERED_FILES = [
    "百万字版创作总纲.md",
    "楔子.md",
    "第一卷_钟山雨.md",
    "第二卷_乌衣巷.md",
    "第三卷_清溪渡.md",
    "第四卷_石门栈.md",
    "第五卷_秦淮血.md",
    "第六卷_苍山雪.md",
    "第七卷_玄岳雷.md",
    "第八卷_江山残.md",
    "第九卷_古寺寒.md",
    "第十卷_永乐网.md",
    "第十一卷_玄岳劫.md",
    "第十二卷_云海无涯.md",
    "附录_谱录.md",
]

CSS = """
:root{--bg:#f6f1e7;--fg:#33302b;--muted:#8a8273;--rule:#ddd2bd;--accent:#8a5a2b;--quote:#efe7d6;--link:#6b4a2b;--card:#fbf7ef;}
body.dark{--bg:#17150f;--fg:#dcd6c8;--muted:#938b79;--rule:#39342a;--accent:#cd9f5e;--quote:#211e17;--link:#d9b277;--card:#1d1a14;}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;background:var(--bg);color:var(--fg);transition:background .3s,color .3s;font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC","STSong","SimSun",Georgia,serif;}
a{color:var(--link);text-decoration:none;}
a:hover{text-decoration:underline;}
.page{max-width:860px;margin:0 auto;padding:0 24px 96px;}
.cover{padding:12vh 0 6vh;text-align:center;border-bottom:1px solid var(--rule);}
.book-title{font-size:2.8rem;letter-spacing:.28em;text-indent:.28em;margin:0 0 .4em;font-weight:700;}
.book-sub{color:var(--accent);font-size:1.08rem;letter-spacing:.16em;margin:.3em 0;}
.book-meta{color:var(--muted);font-size:.92rem;letter-spacing:.12em;margin-top:1.8em;}
.toolbar{position:fixed;right:20px;bottom:20px;display:flex;flex-direction:column;gap:10px;z-index:60;}
.fab{width:46px;height:46px;border-radius:50%;border:1px solid var(--rule);background:var(--quote);color:var(--fg);font-size:1.18rem;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(0,0,0,.15);}
.fab:hover{border-color:var(--accent);color:var(--accent);text-decoration:none;}
.section{padding:5vh 0;border-bottom:1px solid var(--rule);}
.toc-title{font-size:1.55rem;text-align:center;letter-spacing:.4em;text-indent:.4em;color:var(--accent);margin-bottom:1.2em;}
.toc-list{list-style:none;padding:0;margin:0;}
.toc-vol{margin:1em 0 .2em;font-size:1.15rem;font-weight:700;}
.toc-sub{list-style:none;padding-left:1.4em;margin:.35em 0 .85em;columns:2;column-gap:2em;}
.toc-chap{margin:.18em 0;font-size:.96rem;break-inside:avoid;}
.content{padding-top:4vh;}
.content p{margin:.15em 0;text-indent:2em;text-align:justify;font-size:1.12rem;line-height:2.02;letter-spacing:.012em;}
.content ul,.content ol{padding-left:1.6em;line-height:1.95;}
.content li{margin:.5em 0;text-align:justify;}
h2.vol{font-size:2.1rem;text-align:center;letter-spacing:.45em;text-indent:.45em;color:var(--accent);margin:14vh 0 6vh;padding-bottom:.6em;border-bottom:1px solid var(--rule);}
h2.vol:first-of-type{margin-top:3vh;}
h3.chap{font-size:1.45rem;text-align:center;font-weight:700;letter-spacing:.06em;line-height:1.8;margin:7vh 0 3.6vh;}
h4.cat{font-size:1.12rem;color:var(--accent);letter-spacing:.12em;margin:2.4em 0 .8em;}
hr.orn{border:none;text-align:center;margin:2.6em 0;height:1em;}
hr.orn::before{content:"❖";color:var(--muted);letter-spacing:1em;font-size:1rem;}
blockquote{background:var(--quote);border-left:3px solid var(--accent);margin:2.5em 0;padding:1em 1.4em;border-radius:6px;}
blockquote p{text-indent:0;margin:.5em 0;font-size:1rem;line-height:1.9;}
em{font-style:normal;color:var(--muted);letter-spacing:.08em;}
strong{color:var(--accent);}
.nav{display:flex;justify-content:space-between;gap:16px;margin:24px 0 0;flex-wrap:wrap;}
.nav a{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border:1px solid var(--rule);border-radius:999px;background:var(--card);}
.nav a:hover{border-color:var(--accent);text-decoration:none;}
.index-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:28px;}
.card{display:block;padding:18px;border:1px solid var(--rule);border-radius:16px;background:var(--card);min-height:132px;}
.card:hover{border-color:var(--accent);text-decoration:none;transform:translateY(-1px);}
.card-title{font-size:1.08rem;font-weight:700;color:var(--accent);margin-bottom:10px;}
.card-meta{font-size:.92rem;color:var(--muted);line-height:1.8;}
.card-detail{margin-top:14px;border-top:1px solid var(--rule);padding-top:12px;}
.card-detail summary{cursor:pointer;color:var(--fg);font-size:.96rem;}
.card-detail summary:hover{color:var(--accent);}
.chapter-links{list-style:none;padding:10px 0 0 0;margin:0;columns:2;column-gap:1.4em;}
.chapter-link{margin:.28em 0;break-inside:avoid;line-height:1.7;font-size:.92rem;}
.chapter-link a{color:var(--link);}
.footer{text-align:center;color:var(--muted);letter-spacing:.3em;text-indent:.3em;padding:7vh 0 10vh;}
@media(max-width:680px){.book-title{font-size:2.15rem;letter-spacing:.18em;text-indent:.18em;}.toc-sub{columns:1;}.content p{font-size:1.06rem;}.fab{width:42px;height:42px;}.page{padding:0 18px 88px;}.chapter-links{columns:1;}}
"""

JS = """
const themeBtn = document.getElementById('themeBtn');
function setTheme(dark){
  document.body.classList.toggle('dark', dark);
  if(themeBtn){ themeBtn.textContent = dark ? '☀' : '☾'; }
  try{ localStorage.setItem('yh_long_dark', dark ? '1' : '0'); }catch(e){}
}
if(themeBtn){
  themeBtn.addEventListener('click', function(){ setTheme(!document.body.classList.contains('dark')); });
}
try{ setTheme(localStorage.getItem('yh_long_dark') === '1'); }catch(e){ setTheme(false); }
"""


def inline(text: str) -> str:
    value = html.escape(text, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*(.+?)\*", r"<em>\1</em>", value)
    return value


def parse_markdown(raw_text: str):
    elems = []
    sec = 0
    lines = [line.rstrip() for line in raw_text.split("\n")]
    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", raw)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            sec += 1
            elems.append({"t": f"h{level}", "text": text, "id": f"sec{sec}"})
            i += 1
            continue
        if re.match(r"^-{3,}$", s):
            elems.append({"t": "hr"})
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            elems.append({"t": "bq", "lines": block})
            continue
        if re.match(r"^- ", s):
            items = []
            while i < len(lines) and re.match(r"^- ", lines[i].strip()):
                items.append(re.sub(r"^- ", "", lines[i].strip()))
                i += 1
            elems.append({"t": "ul", "items": items})
            continue
        if re.match(r"^\d+\.\s", s):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s", "", lines[i].strip()))
                i += 1
            elems.append({"t": "ol", "items": items})
            continue
        elems.append({"t": "p", "text": s})
        i += 1
    return elems


def render_quote(lines):
    parts = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        parts.append(f"<p>{inline(s)}</p>")
    return "".join(parts)


def render_body(elems):
    out = []
    for elem in elems:
        t = elem["t"]
        if t == "h2":
            out.append(f'<h2 id="{elem["id"]}" class="vol">{inline(elem["text"])}</h2>')
        elif t == "h3":
            out.append(f'<h3 id="{elem["id"]}" class="chap">{inline(elem["text"])}</h3>')
        elif t == "h4":
            out.append(f'<h4 id="{elem["id"]}" class="cat">{inline(elem["text"])}</h4>')
        elif t == "hr":
            out.append('<hr class="orn">')
        elif t == "p":
            out.append(f'<p>{inline(elem["text"])}</p>')
        elif t == "ul":
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in elem["items"]) + '</ul>')
        elif t == "ol":
            out.append('<ol>' + ''.join(f'<li>{inline(x)}</li>' for x in elem["items"]) + '</ol>')
        elif t == "bq":
            out.append(f'<blockquote>{render_quote(elem["lines"])}</blockquote>')
    return "\n".join(out)


def toc_pairs(elems):
    return [(elem["t"], elem["text"], elem["id"]) for elem in elems if elem["t"] in {"h2", "h3"}]


def render_toc(pairs):
    out = ['<div class="toc-title">目录</div>', '<ul class="toc-list">']
    opened = False
    for level, text, sid in pairs:
        if level == 'h2':
            if opened:
                out.append('</ul></li>')
            out.append(f'<li class="toc-vol"><a href="#{sid}">{html.escape(text)}</a>')
            out.append('<ul class="toc-sub">')
            opened = True
        else:
            out.append(f'<li class="toc-chap"><a href="#{sid}">{html.escape(text)}</a></li>')
    if opened:
        out.append('</ul></li>')
    out.append('</ul>')
    return '\n'.join(out)


def render_page(title, subtitle, meta, toc_html, body_html, prev_link, next_link):
    nav = ['<div class="nav">']
    if prev_link:
        nav.append(f'<a href="{prev_link[0]}">← {html.escape(prev_link[1])}</a>')
    else:
        nav.append('<span></span>')
    nav.append('<a href="index.html">返回索引</a>')
    if next_link:
        nav.append(f'<a href="{next_link[0]}">{html.escape(next_link[1])} →</a>')
    else:
        nav.append('<span></span>')
    nav.append('</div>')
    return f'''<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div id="top"></div>
<div class="toolbar">
<button id="themeBtn" class="fab" title="昼夜切换">☾</button>
<a href="#top" class="fab" title="返回顶部">↑</a>
<a href="#toc" class="fab" title="目录">☰</a>
</div>
<div class="page">
<header class="cover">
<h1 class="book-title">{html.escape(title)}</h1>
<p class="book-sub">{html.escape(subtitle)}</p>
<p class="book-meta">{html.escape(meta)}</p>
</header>
<section id="toc" class="section">
{toc_html}
</section>
<main class="content">
{body_html}
{''.join(nav)}
</main>
<footer class="footer">— 云海江湖录·百万字长篇版 —</footer>
</div>
<script>{JS}</script>
</body>
</html>'''


def page_info(md_path: Path):
    raw = md_path.read_text(encoding='utf-8')
    elems = parse_markdown(raw)
    pairs = toc_pairs(elems)
    h2 = next((e['text'] for e in elems if e['t'] == 'h2'), md_path.stem)
    chapter_count = sum(1 for e in elems if e['t'] == 'h3')
    chapter_items = [(e['text'], e['id']) for e in elems if e['t'] == 'h3']
    non_space = len(re.sub(r'\s+', '', raw))
    return {
        'path': md_path,
        'stem': md_path.stem,
        'title': h2,
        'elems': elems,
        'pairs': pairs,
        'chapter_count': chapter_count,
        'chapter_items': chapter_items,
        'non_space': non_space,
    }


def render_index(pages):
    cards = []
    for page in pages:
        meta = f"{page['path'].name}"
        if page['chapter_count']:
            meta += f" · {page['chapter_count']}个章节标题"
        meta += f" · 约{page['non_space']}字"
        chapter_detail = ''
        if page['chapter_items']:
            chapter_links = ''.join(
                f'<li class="chapter-link"><a href="{html.escape(page["stem"])}.html#{sid}">{html.escape(text)}</a></li>'
                for text, sid in page['chapter_items']
            )
            chapter_detail = (
                '<details class="card-detail">'
                '<summary>每回索引</summary>'
                f'<ul class="chapter-links">{chapter_links}</ul>'
                '</details>'
            )
        cards.append(
            f'<div class="card">'
            f'<a href="{html.escape(page["stem"])}.html">'
            f'<div class="card-title">{html.escape(page["title"])}</div>'
            f'<div class="card-meta">{html.escape(meta)}</div>'
            '</a>'
            f'{chapter_detail}'
            '</div>'
        )
    return f'''<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{BOOK_TITLE}</title>
<style>{CSS}</style>
</head>
<body>
<div class="toolbar">
<button id="themeBtn" class="fab" title="昼夜切换">☾</button>
<a href="#top" class="fab" title="返回顶部">↑</a>
</div>
<div id="top"></div>
<div class="page">
<header class="cover">
<h1 class="book-title">{BOOK_TITLE}</h1>
<p class="book-sub">楔子 · 十二卷 · 谱录 · 创作总纲</p>
<p class="book-meta">Markdown 与 HTML 同步保留，可直接本地浏览与部署</p>
</header>
<section class="section">
<div class="toc-title">阅读索引</div>
<div class="index-grid">{''.join(cards)}</div>
</section>
<footer class="footer">— 站点索引 —</footer>
</div>
<script>{JS}</script>
</body>
</html>'''


def main():
    SITE.mkdir(parents=True, exist_ok=True)
    pages = []
    for name in ORDERED_FILES:
        path = BASE / name
        if path.exists():
            pages.append(page_info(path))
    for idx, page in enumerate(pages):
        prev_link = None if idx == 0 else (f'{pages[idx - 1]["stem"]}.html', pages[idx - 1]['title'])
        next_link = None if idx == len(pages) - 1 else (f'{pages[idx + 1]["stem"]}.html', pages[idx + 1]['title'])
        html_text = render_page(
            page['title'],
            BOOK_TITLE,
            f'{page["path"].name} · 约{page["non_space"]}字',
            render_toc(page['pairs']),
            render_body(page['elems']),
            prev_link,
            next_link,
        )
        (SITE / f'{page["stem"]}.html').write_text(html_text, encoding='utf-8')
    (SITE / 'index.html').write_text(render_index(pages), encoding='utf-8')
    print(f'生成页面: {len(pages)}')
    for page in pages:
        print(f'{page["path"].name} -> site/{page["stem"]}.html')
    print('索引页: site/index.html')


if __name__ == '__main__':
    main()
