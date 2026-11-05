#!/usr/bin/env python3
"""扫描 notes/<course>/ 下的定理类环境，每门课生成一份 index/<course>.md 与 .csv。
用法： python tools/make_index.py
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "notes"
OUT = ROOT / "index"
ENVS = ("theorem", "lemma", "proposition", "corollary", "definition", "example", "remark")
KIND = {"theorem": "定理", "lemma": "引理", "proposition": "命题", "corollary": "推论",
        "definition": "定义", "example": "例", "remark": "注"}

BEGIN = re.compile(r"\\begin\{(" + "|".join(ENVS) + r")\}(?:\[(?P<title>[^\]]*)\])?")
LABEL = re.compile(r"\\label\{(?P<label>[^}]+)\}")
SECTION = re.compile(r"\\(?:section|chapter)\*?\{(?P<sec>[^}]*)\}")


def strip_tex(s: str) -> str:
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\})?", " ", s)
    s = re.sub(r"[{}\\]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def scan(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pos, section = 0, ""
    rows = []
    # 按文档顺序同时推进 section 与定理的位置
    events = [(m.start(), "sec", m) for m in SECTION.finditer(text)]
    events += [(m.start(), "thm", m) for m in BEGIN.finditer(text)]
    for _, kind, m in sorted(events, key=lambda x: x[0]):
        if kind == "sec":
            section = m.group("sec")
            continue
        body_start = m.end()
        nxt = text.find("\\end{" + m.group(1) + "}", body_start)
        body = text[body_start:nxt] if nxt != -1 else ""
        lab = LABEL.search(body)
        if not lab:  # 无 label 时回退到该环境之后最近的 label
            lab = LABEL.search(text[body_start:body_start + 500])
        rows.append({
            "type": KIND[m.group(1)],
            "title": (m.group("title") or "").strip(),
            "label": lab.group("label") if lab else "",
            "section": section,
            "file": path.relative_to(ROOT).as_posix(),
            "text": strip_tex(body)[:120],
        })
        pos = nxt
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    # 一门课 = 一个带 main.tex 的子目录（跳过 common/ 等共用目录）
    courses = sorted(p for p in SRC.iterdir() if p.is_dir() and (p / "main.tex").exists())
    for course in courses:
        rows = []
        m = re.search(r"\\title\{([^}]*)\}", (course / "main.tex").read_text(encoding="utf-8"))
        title = m.group(1).strip() if m else course.name
        for p in sorted(course.rglob("*.tex")):
            if p.name == "preamble.tex":
                continue
            rows += scan(p)

        with (OUT / f"{course.name}.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["type", "title", "label", "section", "file", "text"])
            w.writeheader()
            w.writerows(rows)

        lines = [f"# 定理索引 · {title}", "",
                 f"共 {len(rows)} 条，由 `tools/make_index.py` 自动生成。", "",
                 "| # | 类型 | 标题 | 标签 | 章节 | 文件 |", "|---|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            lines.append(f"| {i} | {r['type']} | {r['title']} | `{r['label']}` | {r['section']} | {r['file']} |")
        (OUT / f"{course.name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"indexed {len(rows):4d} items -> index/{course.name}.md, index/{course.name}.csv")


if __name__ == "__main__":
    main()
