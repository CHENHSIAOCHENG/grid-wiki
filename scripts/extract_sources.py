"""從《网格系统在平面设计中的应用》PDF 抽出中文文字層，依章節分組存成 raw/ 下的原始資料。
用法：python scripts/extract_sources.py <pdf 路徑>
規則沿用 RAG_01 notebook：略過 PDF 1-3 頁、跨頁切左右、去頁首頁碼、只留中文。"""
import re, sys
from pathlib import Path
import pymupdf

SKIP_PDF_PAGES = {1, 2, 3}
HEADER_BOTTOM, FOOTER_TOP = 110, 540
TOC = [(7,"前言"),(9,"关于本书"),(10,"网格与设计哲学"),(11,"编排设计中的网格"),(13,"网格的目的是什么？"),
 (15,"纸张的尺寸"),(17,"排版中的度量系统"),(19,"字体样式"),(30,"栏的宽度"),(34,"行距"),(39,"页边距"),
 (42,"页码"),(45,"正文与标题字体"),(49,"版心的结构"),(57,"网格的结构"),(72,"8 格网格系统中的文字与图片"),
 (76,"20 格网格系统中的文字与图片"),(87,"32 格网格系统中的文字与图片"),(97,"网格系统中的图片"),
 (99,"网格系统中的插图"),(101,"网格系统中的色块"),(104,"设计案例"),(133,"企业形象设计中的网格系统"),
 (141,"三维空间设计中的网格系统"),(149,"展览空间设计实例"),(158,"古代和现代的秩序系统"),(174,"后记"),
 (175,"参考文献"),(176,"艺术家列表")]
# 一份 source = 幾個相連章節（書頁起訖）
SOURCES = [
 ("01-grid-philosophy", "網格的理念與目的", 7, 14),
 ("02-paper-measure-type", "紙張、度量系統與字體", 15, 29),
 ("03-column-leading-margin", "欄寬、行距、頁邊距、頁碼與字體搭配", 30, 48),
 ("04-type-area-grid-construction", "版心與網格的建構", 49, 71),
 ("05-8-20-32-fields", "8／20／32 格網格中的文字與圖片", 72, 96),
 ("06-photo-illustration-tint", "網格中的照片、插圖與色塊", 97, 103),
 ("07-examples-corporate", "設計案例與企業形象", 104, 140),
 ("08-3d-exhibition", "三維空間與展覽設計", 141, 157),
 ("09-order-systems", "古代與現代的秩序系統、後記", 158, 174),
]
CJK = re.compile(r"[㐀-鿿豈-﫿　-〿＀-￯]")

def smart_join(a, b):
    a, b = a.rstrip(), b.strip()
    if not a or not b: return a or b
    if a.endswith("-") and re.match(r"[a-z]", b): return a[:-1] + b
    if CJK.match(a[-1]) or CJK.match(b[0]): return a + b
    return a + " " + b

def is_chinese(t):
    cs = [c for c in t if not c.isspace()]
    return bool(cs) and sum(bool(CJK.match(c)) for c in cs) / len(cs) >= 0.2

def section_of(p):
    cur = "前置页"
    for s, zh in TOC:
        if p >= s: cur = zh
    return cur

def pages(pdf_path):
    out = []
    with pymupdf.open(pdf_path) as pdf:
        for i, page in enumerate(pdf):
            if i + 1 in SKIP_PDF_PAGES: continue
            w = page.rect.width; spread = w > page.rect.height
            halves = {0: [], 1: []}
            for x0, y0, x1, y1, text, _, bt in page.get_text("blocks"):
                if bt != 0 or not text.strip() or y1 < HEADER_BOTTOM: continue
                if re.fullmatch(r"[\d\s]+", text) and y0 > FOOTER_TOP and abs((x0+x1)/2 - w/2) < 60: continue
                halves[1 if spread and (x0+x1)/2 >= w/2 else 0].append(text)
            for h, blocks in halves.items():
                if h == 1 and not spread: continue
                zh = ""
                for b in blocks:
                    if is_chinese(b):
                        for line in b.splitlines(): zh = smart_join(zh, line)
                if zh.strip(): out.append((2*i + h, i + 1, zh))
    return out

def main(pdf_path):
    raw = Path(__file__).resolve().parent.parent / "raw"; raw.mkdir(exist_ok=True)
    ps = pages(pdf_path)
    for slug, title, a, b in SOURCES:
        lines = [f"# {title}", "", f"來源：Josef Müller-Brockmann《网格系统在平面设计中的应用》中英對照版 PDF，書頁 {a}–{b}（只取中文文字層，未校對）", ""]
        last = None
        for bp, pp, t in ps:
            if not a <= bp <= b: continue
            sec = section_of(bp)
            if sec != last: lines += ["", f"## {sec}", ""]; last = sec
            lines += [f"[p.{bp}｜PDF {pp}] {t}", ""]
        text = "\n".join(lines)
        (raw / f"{slug}.md").write_text(text, encoding="utf-8")
        print(slug, len(text))

if __name__ == "__main__":
    main(sys.argv[1])
