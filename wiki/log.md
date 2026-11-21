# Log

## [2026-11-21] setup | 建立 wiki
- 用 scripts/extract_sources.py 把 PDF 依章節抽成 9 份 raw（只取中文文字層）。
- 寫 CLAUDE.md（schema）與 scripts/lint_wiki.py。

## [2026-11-21] discuss | ingest 計畫
- discussions/2026-11-21-ingest-plan.md：AI 提出 6 份來源的重點、預計頁面、疑點。
- 使用者決定：觀念＋關鍵數字；本輪 ingest 來源 1–6；全部改寫成繁體中文。

## [2026-11-21] ingest | 01 網格的理念與目的
- 新增：src-01-grid-philosophy、grid-system、grid-field、design-philosophy、why-grid、josef-muller-brockmann、overview、index
- 疑誤：p.10「網絡系統」→ 網格系統
- lint run1：14 ERROR（2 個年代改寫成西元年後比對不到、1 句「瑞士平面設計師」是 raw 沒有的一般知識、4 行來源頁的說明句、7 個連到還沒建立的頁面）；11 WARN（「系」被誤判成簡體字）
- 修正 wiki 後，lint 也改了兩條規則：「系」移出簡體字清單；討論稿已規劃的頁面，連結先算 WARN
- lint run2：0 ERROR

## [2026-11-21] ingest | 02 紙張、度量系統與字體
- 新增：src-02-paper-measure-type、paper-sizes、measuring-system、typefaces
- 疑誤：p.18「1 厘米等於 10 厘米」→ 1 公分 = 10 公釐；Berthold 譯名不一致
- lint：0 ERROR。對照原文抽查發現 1 句把 p.72 的「雷射照排」混進 p.17（checks/review-02-ingest02.md），已改

## [2026-11-21] ingest | 03 欄寬、行距、頁邊距、頁碼與字體搭配
- 新增：src-03-column-leading-margin、column-width、leading、margins、page-numbers、body-and-display-type
- 註明「每行 7–10 個單字」是英文單字
- lint：0 ERROR。抽查發現 margins 把左頁的訂口寫成外側（checks/review-03-ingest03.md），已改

## [2026-11-21] ingest | 04 版心與網格的建構
- 新增：src-04-type-area-grid-construction、type-area、grid-construction、baseline-alignment、sketching、compound-grid
- 加入〔推算〕驗算：656 點 ≈ 24.7 cm、n × k + (n − 1) 通則、53 行與 59 行的分法
- lint run1：7 ERROR，其中 6 個是誤判（原文用中文數字「四栏」）。lint 改成先把中文數字轉成阿拉伯數字
- 抽查發現 3 處：自己推論的「一欄適合純文字」、違反文字規則的對比句、出處頁錯（checks/review-04-ingest04.md），已改

## [2026-11-21] ingest | 05 8／20／32 格、06 照片插圖色塊
- 新增：src-05-8-20-32-fields、grid-8-20-32、white-space、src-06-photo-illustration-tint、images-in-grid、color-tint；overview 改寫成完整的學習順序
- lint run1：1 ERROR（原文疑誤沒有出處）；run2：3 ERROR（overview 的來源清單被當成事實句）；run3：0 ERROR、0 WARN
- 抽查發現 2 處：對原文歧義做了詮釋、出處不完整（checks/review-05-ingest05-06.md），已改

## [2026-11-21] query | 教學簡報「網格系統入門」
- 只讀 index → wiki 頁面，寫成 keynote-decks/decks/grid-basics/outline.md（15 頁），每頁來源寫 wiki 頁面＋書頁
- 新增 scripts/check_outline.py：outline 的數字要在引用的 wiki 頁面找得到，書頁要在該頁出處裡；slides 的數字要在 outline 找得到
- check run1：70 個數字 0 ERROR。故意改錯 3 處做測試，只抓到 2 處：「5 mm」改成「3 mm」沒抓到，因為同頁 wiki 有「1 到 3 mm」（checks/outline-check-mutation-test.txt）
- slides check：102 個數字 0 ERROR
- 截圖檢查發現 2 個問題：頁邊距示意圖把「訂口」指到左頁外側（其實是切口）、三種網格卡片只有一個「格」字。已修，重出截圖確認
- 依這次執行結果，修改 CLAUDE.md：ingest 加「對照原文抽查」，query 加「做簡報時」的檢查順序

## 狀態
- 29 頁：overview 1、概念 21、實體 1、來源 6
- 尚未 ingest：raw/07、08、09
