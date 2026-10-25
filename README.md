# Segullah

<https://hungshinlee.github.io/segullah/>

教會服事中可以公開分享的內容：主日學的教材與學習單，以及其他服事用得上的資料。

## 結構

```
index.html                              首頁
assets/site.css                         全站共用樣式
sunday-school/junior-high/index.html    板新青少主日學 · 國中部：每一課一列（日期、主題、經文、資料）
sunday-school/junior-high/YYYY-MM-DD/   國中部每一課一個資料夾（投影片、學習單）
sunday-school/senior-high/              高中部，結構同上
sunday-school/slides-guide.html         投影片使用說明（列表頁連過來）
enoch-fellowship/index.html             以諾團契小組問題：每一次一列（日期、主題、經文、資料）
enoch-fellowship/YYYY-MM-DD/            每一次一個資料夾（討論題頁面）
scripts/check.py                        發布前檢查
.github/workflows/                      push 到 main 後自動發布
```

純 HTML，不需要建置。資料夾與檔名只用英數字，中文路徑在網址裡會變成一長串 %E5…。

簡報含講者備註與講者視窗（按 P 另開一個視窗：投影中的這一頁、下一頁、講稿、計時），給要拿去教的老師備課用（2026-10-25 起）。

新增一課或一次團契：把檔案放進該次的資料夾，再到列表頁照 HTML 註解裡的範本加一列（新的放最上面）。
`check.py` 會檢查站內連結有沒有指到不存在的檔案。

## 發布

commit 之前，先在本機跑：

```bash
python3 scripts/check.py
```

push 到 `main` 之後，GitHub Actions 會再跑一次同樣的檢查，通過才發布。
這個 repo 是公開的，檔案一 push 就進了公開的歷史，事後刪檔也看得到；
CI 擋得住網站，擋不住 repo，所以本機那一次才是真正的關卡。

## 本站不放

- 學生的照片、姓名、班級、作品
- 還沒核對過的經文引文與史實（講者備註也一樣）
- 備課用的來源等級標記（全形方括號裡的「查證」「推估」之類）；出處改寫成括號裡的資料名稱
