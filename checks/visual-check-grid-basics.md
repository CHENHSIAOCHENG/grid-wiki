# 截圖檢查｜grid-basics（2026-11-21）

照 keynote-decks AGENTS.md 第 11 節，看 dist/contact/sheet-1～4.png，有疑慮的頁再看 dist/png/<頁>.png。

| 頁 | 問題 | 怎麼發現 | 處理 |
|---|---|---|---|
| 7 頁邊距與版心 | 「訂口（內側）」的虛線從右頁訂口穿過左頁，標籤在左頁外側，看起來在指左頁的切口 | 看截圖；數字檢查不會檢查圖的語意 | 改成兩個標籤都標在右頁：訂口標在中縫旁、從下方引出，切口標在右側 |
| 12 三種網格 | GridCell 的 title 只有一個「格」字，數字和標題斷開 | 看截圖 | value 改成「8 格」「20 格」「32 格」，title 改成「常見用途／示範／可能性」 |
| 其他 13 頁 | 無文字溢出、孤字、彩色文字；每頁都有 section 與講稿 | 看截圖 | 無 |

修完重跑 `npm run diagrams`、`npm run shots`，看過 7.png、12.png 確認已修好；check_outline 再跑一次 0 ERROR（slides-check-run2.txt）。
