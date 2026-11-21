# 網格系統 LLM Wiki

以 Josef Müller-Brockmann《網格系統在平面設計中的應用》為資料來源，由 LLM 維護的知識庫（LLM Wiki）。
這輪 ingest 了 6 份來源（書頁 7–103），共 29 頁 wiki，每一句事實都標書頁。

- 從這裡開始讀：[wiki/overview.md](wiki/overview.md)
- 全部頁面：[wiki/index.md](wiki/index.md)
- 時間序紀錄：[wiki/log.md](wiki/log.md)
- 規則（schema）：[CLAUDE.md](CLAUDE.md)
- ingest 前的討論：[discussions/](discussions/)
- 每次檢查的輸出：[checks/](checks/)
- 作業說明（loop / graph、執行紀錄、反思）：[繳交內容.md](繳交內容.md)
- 用這份 wiki 做的教學簡報：https://chenhsiaocheng.github.io/keynote-decks/grid-basics/

## 重新產生 raw/

`raw/` 是原書的中文文字層，受著作權保護，所以沒有放進 repo。有 PDF 的話可以重新產生：

```
python scripts/extract_sources.py <PDF 路徑>
python scripts/lint_wiki.py
```

`lint_wiki.py` 要比對 raw/ 的原文，所以要先產生 raw/。
