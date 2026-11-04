# 数学笔记

手写笔记的 LaTeX 化版本：源文件 + 编译好的 PDF + 自动生成的定理索引。

## 目录

| 路径 | 内容 |
|---|---|
| `notes/main.tex` | 唯一入口，`\include` 各章 |
| `notes/preamble.tex` | 导言区（宏包与环境定义） |
| `notes/chapters/` | 每章一个 `.tex` |
| `notes/figures/` | 图片 |
| `scan/` | 手写原稿扫描件（留档，不参与编译） |
| `inbox/` | 待处理文件暂存（不进版本库） |
| `tools/make_index.py` | 扫描定理环境，生成索引 |
| `index/theorems.md` | 定理索引（自动生成，可直接在网页看） |
| `index/theorems.csv` | 同上，给脚本/Anki 用 |
| `dist/math-notes.pdf` | 最新编译产物 |

## 编译

```bash
cd notes && latexmk -xelatex main.tex
```

引擎固定为 XeLaTeX（见 `notes/.latexmkrc`）。

## 生成索引

```bash
python tools/make_index.py
```

## 约定

- 定理类环境：`theorem` / `lemma` / `proposition` / `corollary` / `definition` / `example` / `remark`，共用一套编号。
- **每个定理必须带 `\label{thm:xxx}`**，否则索引里只剩位置、没有稳定锚点。
- 标签前缀：`thm:` 定理、`lem:` 引理、`def:` 定义、`eq:` 公式、`fig:` 图。

## 下载

最新 PDF：`dist/math-notes.pdf`
