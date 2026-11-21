"""檢查 wiki/：連結、出處、數字、index、孤兒頁、簡體字。
用法：python scripts/lint_wiki.py [--quiet]
結果寫到 stdout（UTF-8），有 ERROR 時 exit code 1。"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI, RAW = ROOT / "wiki", ROOT / "raw"
SPECIAL = {"index", "log"}
REQUIRED_FM = ("title", "type", "sources", "updated")
CITE = re.compile(r"\[p\.(\d+)(?:[–-](\d+))?\]")
LINK = re.compile(r"\[\[([^\]|]+)\]\]")
NUM = re.compile(r"\d+(?:\.\d+)?")
DERIVED = "〔推算〕"
# 只收繁體文章裡幾乎不會出現的簡體字
SIMPLIFIED = set("网们这为个来对时说设计书页边图节栏线统号间应该关东会样进过还将与发现实际构单择级专处这读览论认识论标题导华")

def planned_pages():
    """討論稿「預計頁面：」列出的頁面：還沒建立時只算 WARN。"""
    names = set()
    for f in (ROOT / "discussions").glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if "預計頁面" in line:
                names |= set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+|[a-z]{4,}", line))
    return names

CN_NUM = {"十六": "16", "十二": "12", "十": "10", "一": "1", "二": "2", "两": "2", "三": "3", "四": "4",
          "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}

def with_arabic(text):
    """原文常寫「四栏」「八格」，另外補一份換成阿拉伯數字的版本，避免誤判。"""
    out = text
    for cn, d in CN_NUM.items():
        out = re.sub(cn + r"(?=[栏格行种个点页])", d, out)
    return text + " | " + out

def load_raw_pages():
    pages = {}
    for f in RAW.glob("*.md"):
        for m in re.finditer(r"\[p\.(\d+)｜PDF \d+\] (.*)", f.read_text(encoding="utf-8")):
            pages[int(m.group(1))] = pages.get(int(m.group(1)), "") + with_arabic(m.group(2))
    return pages

def parse(path):
    text = path.read_text(encoding="utf-8")
    fm, body = {}, text
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        body = text[m.end():]
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); fm[k.strip()] = v.strip()
    return fm, body

def main():
    raw = load_raw_pages()
    planned = planned_pages()
    files = {p.stem: p for p in WIKI.rglob("*.md")}
    errors, warns = [], []
    incoming = {s: 0 for s in files}
    for stem, path in files.items():
        rel = path.relative_to(ROOT).as_posix()
        fm, body = parse(path)
        for target in LINK.findall(body):
            if target not in files:
                if target in planned:
                    warns.append(f"{rel}: [[{target}]] 尚未建立（討論稿已規劃）")
                else:
                    errors.append(f"{rel}: 斷掉的連結 [[{target}]]")
            elif target != stem and stem not in SPECIAL:
                incoming[target] += 1
        if stem in SPECIAL:
            continue
        for k in REQUIRED_FM:
            if k not in fm:
                errors.append(f"{rel}: frontmatter 缺 {k}")
        section = ""
        for n, line in enumerate(body.splitlines(), 1):
            s = line.strip()
            if s.startswith("#"):
                section = s; continue
            if not s or s.startswith("範圍：") or "相關" in section or s.startswith("|") or len(s) < 12:
                continue
            for ch in set(s) & SIMPLIFIED:
                warns.append(f"{rel}:{n}: 疑似簡體字「{ch}」")
            cites = CITE.findall(s)
            if not cites and DERIVED not in s:
                errors.append(f"{rel}:{n}: 事實句沒有書頁出處 → {s[:40]}")
                continue
            if DERIVED in s or "原文疑誤" in section:
                continue
            pool = ""
            for a, b in cites:
                for p in range(int(a), int(b or a) + 1):
                    pool += raw.get(p, "")
            check = LINK.sub("", CITE.sub("", s))
            for num in NUM.findall(check):
                if num not in pool:
                    errors.append(f"{rel}:{n}: 數字 {num} 在引用書頁 {cites} 的原文找不到")
    index_text = (WIKI / "index.md").read_text(encoding="utf-8") if (WIKI / "index.md").exists() else ""
    for stem in files:
        if stem not in SPECIAL and f"[[{stem}]]" not in index_text:
            errors.append(f"wiki/index.md: 沒有列出 [[{stem}]]")
        if stem not in SPECIAL and stem != "overview" and incoming[stem] == 0:
            warns.append(f"{files[stem].relative_to(ROOT).as_posix()}: 孤兒頁（沒有其他頁面連進來）")
    out = [f"頁面 {len(files) - len(SPECIAL & set(files))} 個｜ERROR {len(errors)}｜WARN {len(warns)}"]
    out += [f"ERROR {e}" for e in errors] + [f"WARN  {w}" for w in warns]
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(out))
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
