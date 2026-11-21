# CLAUDE.md — 網格系統 LLM Wiki

這是一份由 LLM 維護的知識庫（LLM Wiki），主題是 Josef Müller-Brockmann《網格系統在平面設計中的應用》。
人負責選資料、討論方向、做決定；LLM 負責讀資料、寫頁面、維護連結和檢查。

## 三層結構

```
grid-wiki/
├── raw/            原始資料（不可修改）。PDF 依章節抽出的中文文字層，每段開頭有 [p.書頁｜PDF 頁]
├── discussions/    ingest 前的討論紀錄（先討論、後生成）
├── checks/         每次 lint、抽查、簡報檢查的輸出
├── wiki/           LLM 寫的頁面
│   ├── index.md    目錄：每頁一行，依類別分組
│   ├── log.md      時間序紀錄：ingest、query、lint 的結果
│   ├── overview.md 主題總覽，給第一次來的讀者
│   ├── sources/    每份 raw 一頁摘要
│   ├── concepts/   概念頁
│   └── entities/   人物、標準等實體
└── scripts/
    ├── extract_sources.py  PDF → raw/
    ├── lint_wiki.py        檢查（連結、孤兒頁、出處、數字、簡體字）
    └── check_outline.py    檢查簡報 outline／slides 的數字能追回 wiki
```

## 頁面格式

```markdown
---
title: 單元網格
type: concept            # concept | entity | source | overview
sources: [01-grid-philosophy, 04-type-area-grid-construction]
updated: 2026-11-21
---

# 單元網格

一段定義（2–3 句）。

## 重點
- 每一條事實句結尾都要有書頁出處，格式 [p.11] 或 [p.61–62]。
- 推算出來、書中沒有直接寫的數字，句尾標〔推算〕並寫出算式。

## 相關
- [[type-area]]、[[baseline-alignment]]
```

- 檔名用英文 kebab-case；連結用 `[[檔名]]`（不含路徑與 .md），檔名在整個 wiki/ 內唯一。
- 全部用繁體中文（台灣用語）改寫，不貼大段原文；專有名詞第一次出現附原文。
- 「每行 7–10 個單字」這類英文排版經驗值，要註明是英文單字。
- 原文疑誤（錯字、矛盾）在頁面裡寫正確版本，並在 log.md 記下。

## 操作流程

### Ingest（一次一份來源）
1. **讀**：讀 raw/<來源>.md 全文。
2. **討論**：在 discussions/ 寫下重點、預計建立或更新的頁面、疑點，等使用者回覆。不可跳過。
3. **生成**：寫 sources/<來源>.md 摘要頁；建立或更新相關的 concepts/、entities/ 頁面。一份來源通常會動到 5–10 頁。
4. **更新** index.md 與 log.md。
5. **Lint**：執行 `python scripts/lint_wiki.py`，有 ERROR 就回到步驟 3 修正，直到 0 ERROR。
6. **對照原文抽查**（2026-11-21 執行後新增）：lint 只檢查格式和數字。這一步逐條把新寫的句子和 raw 原文比對，看方向、位置、因果有沒有寫錯，有沒有把別頁的內容混進來，或把自己的推論寫成書中說法。結果記在 checks/review-*.md；有錯就回到步驟 3。

### Query（用 wiki 回答問題或做簡報）
1. 先讀 index.md 找相關頁面，再讀頁面；不直接讀 raw/。
2. 答案或大綱的每個事實都標「wiki 頁面＋書頁」。
3. wiki 找不到的內容，回報「wiki 沒有」，不用一般知識補。需要時回到 Ingest 補頁面。
4. 有價值的答案可以存回 wiki 成新頁面，並記在 log.md。
5. **做簡報時**（2026-11-21 執行後新增）：先寫 outline.md（來源寫「wiki 頁面（書頁）」），執行
   `python scripts/check_outline.py <outline.md>`，0 ERROR 才寫 slides.md；寫完再帶 slides.md 跑一次。
   示意圖不在數字檢查範圍內，要看截圖確認。

### Lint（定期或每次 ingest 後）
`python scripts/lint_wiki.py` 檢查：
- ERROR：斷掉的 [[連結]]（討論稿已規劃、還沒建立的頁面只算 WARN）、事實句沒有書頁出處、句中數字在所引書頁的 raw 找不到（原文的中文數字會先轉成阿拉伯數字；〔推算〕與「原文疑誤」段落除外）、frontmatter 缺欄位、index.md 漏列頁面。
- WARN：孤兒頁（沒有其他頁連進來）、出現簡體字。

## log.md 格式

每筆用 `## [YYYY-MM-DD] 動作 | 標題` 開頭，方便用 grep 找：

```
## [2026-11-21] ingest | 01 網格的理念與目的
- 新增：grid-system、grid-field ...
- 疑誤：p.10「網絡系統」→ 網格系統
- lint：0 ERROR / 1 WARN
```
