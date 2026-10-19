# Segullah

<https://hungshinlee.github.io/segullah/>

教會服事中可以公開分享的內容：主日學的教材與學習單，以及其他服事用得上的資料。

## 結構

```
index.html                 首頁
sunday-school/YYYY-MM-DD/  每一課一個資料夾（網址只用英數字，中文路徑會變成一長串 %E5…）
scripts/check.py           發布前檢查
.github/workflows/         push 到 main 後自動發布
```

純 HTML，不需要建置。

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
- 還沒核對過的經文引文與史實
- 簡報的講者備註
