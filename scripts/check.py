#!/usr/bin/env python3
"""發布前檢查：確認 site/ 裡沒有不該公開的東西。

用法（在 site/ 裡）：
    python3 scripts/check.py

有問題就列出檔案與原因，並以 1 結束；GitHub Actions 每次發布前也跑這一支。
注意：這個 repo 是公開的，push 上去就進了公開的歷史。
所以要在 commit 之前跑，CI 那一關只是第二道保險。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", "scripts", "_site"}
TEXT_EXT = {".html", ".htm", ".md", ".txt", ".css", ".js", ".json", ".svg", ".csv", ".xml"}
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".avif",
             ".mp4", ".mov", ".webm", ".mp3", ".m4a", ".wav", ".pdf"}

# 不能公開的內部檔名
BLOCK_NAMES = {"facts_and_decisions.md", "decision_log.md", "outline.md", "notes.md"}

# (正規表示式, 原因)：出現就擋
BLOCK_PATTERNS = [
    (r"【(推估|待核對|待查證|待補|自述|教會|查證)】", "備課用的來源標記"),
    (r"facts_and_decisions|decision_log|outline\.md", "內部檔名"),
    (r"/Users/|/home/[a-z]|~/[A-Za-z]", "本機路徑"),
    (r"claude\.ai/artifact", "私人 Artifact 連結"),
    (r"<form\b", "表單（本站不收集任何資料）"),
    (r"googletagmanager|google-analytics|gtag\(|fbq\(|clarity\.ms", "追蹤碼"),
]


def walk(root):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        yield p, rel


LINK_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"'#?]+)""")


def broken_links(path, text):
    """站內連結指到不存在的檔案。HTML 註解裡的範本不算。"""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
            continue  # http:、https:、mailto:、data: 等外部連結不檢查
        dest = (ROOT / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
        if target.endswith("/") or dest.is_dir():
            dest = dest / "index.html"
        if not dest.exists():
            line = text.count("\n", 0, m.start()) + 1
            yield line, target


def main():
    problems, media = [], []
    for path, rel in walk(ROOT):
        if path.name in BLOCK_NAMES:
            problems.append((rel, "內部檔案，不該放進 site/"))
            continue
        ext = path.suffix.lower()
        if ext in MEDIA_EXT:
            media.append(rel)
            continue
        if ext not in TEXT_EXT:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, reason in BLOCK_PATTERNS:
            for m in re.finditer(pattern, text):
                line = text.count("\n", 0, m.start()) + 1
                problems.append((rel, f"第 {line} 行：{reason}（{m.group(0)[:40]}）"))
        if ext in {".html", ".htm"}:
            for line, target in broken_links(path, text):
                problems.append((rel, f"約第 {line} 行：連結指到不存在的檔案（{target}）"))

    if media:
        print("請人眼確認以下檔案沒有學生的臉、名字、作品：")
        for rel in media:
            print(f"  {rel}")
        print()

    if problems:
        print("發現問題，請先處理再 commit：")
        for rel, reason in problems:
            print(f"  {rel}  {reason}")
        return 1

    print("OK：沒有發現不該公開的內容，站內連結也都正常。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
