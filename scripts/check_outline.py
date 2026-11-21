"""檢查簡報與 wiki 的對應。
用法：python scripts/check_outline.py <outline.md> [slides.md]
1. outline 每頁的「來源:」列出的 wiki 頁面要存在，括號裡的書頁要出現在該頁的出處。
2. outline 每頁（條列與 Notes）的數字，要能在引用的 wiki 頁面內文找到（不算出處標記）。
3. 有給 slides.md 時，畫面與講稿中的數字要能在 outline 找到。
有 ERROR 時 exit code 1。"""
import re, sys
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent / "wiki"
CITE = re.compile(r"\[p\.(\d+)(?:[–-](\d+))?\]")
NUM = re.compile(r"\d+(?:\.\d+)?")

def wiki_pages():
    return {p.stem: p.read_text(encoding="utf-8") for p in WIKI.rglob("*.md")}

def cited_pages(text):
    out = set()
    for a, b in CITE.findall(text):
        out |= set(range(int(a), int(b or a) + 1))
    return out

def sections(outline):
    parts = re.split(r"^## ", outline, flags=re.M)[1:]
    return [("## " + p.splitlines()[0], p) for p in parts]

def main(outline_path, slides_path=None):
    sys.stdout.reconfigure(encoding="utf-8")
    pages = wiki_pages()
    outline = Path(outline_path).read_text(encoding="utf-8")
    errors, checked = [], 0
    for head, body in sections(outline):
        src = re.search(r"^來源[:：](.*)$", body, re.M)
        if not src:
            errors.append(f"{head}: 沒有「來源:」"); continue
        names = re.findall(r"([a-z0-9]+(?:-[a-z0-9]+)*)(?:（書頁 ([^）]+)）)?", src.group(1))
        pool = ""
        for name, bp in names:
            if name not in pages:
                errors.append(f"{head}: wiki 沒有頁面 {name}"); continue
            pool += CITE.sub("", pages[name])
            for n in re.findall(r"\d+", bp):
                if int(n) not in cited_pages(pages[name]):
                    errors.append(f"{head}: {name} 的出處裡沒有書頁 {n}")
        content = "\n".join(l for l in body.splitlines()[1:]
                            if l.startswith("- ") or l.startswith("Notes:"))
        content = re.sub(r"^## \d+\.", "", content)
        for num in sorted(set(NUM.findall(content)), key=float):
            checked += 1
            if num not in pool:
                errors.append(f"{head}: 數字 {num} 在引用的 wiki 頁面找不到")
    if slides_path:
        slides = Path(slides_path).read_text(encoding="utf-8")
        slides = re.sub(r"^---\n.*?\n---\n", "", slides, flags=re.S | re.M)
        slides = re.sub(r"^(layout|section|image|unit|source):.*$", "", slides, flags=re.M)
        visible = re.sub(r"<br>|:span=\"\d+\"|:rows=\"\d+\"|span=\"\d+\"", "", slides)
        for num in sorted(set(NUM.findall(visible)), key=float):
            checked += 1
            if num not in outline:
                errors.append(f"slides.md: 數字 {num} 在 outline.md 找不到")
    print(f"檢查數字 {checked} 個｜ERROR {len(errors)}")
    print("\n".join(f"ERROR {e}" for e in errors))
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main(*sys.argv[1:])
