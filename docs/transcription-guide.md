# 转写规范

新章节照这份文件做即可。**只改内容，不要动 `notes/common/preamble.tex`。**

## 1. 目录

```
notes/common/preamble.tex     全课共用导言区，禁止擅自增删宏包
notes/<course>/main.tex       课程主文件，\input 共用导言区
notes/<course>/chapters/chNN.tex
notes/<course>/.latexmkrc
scan/<course>/                扫描件原件
dist/<course>.pdf             发布用 PDF
index/<course>.md|csv        每门课一份，自动生成，勿手改
tools/make_index.py
```

新开一门课：复制 `notes/reptheory/` 整个目录，改 `main.tex` 里的 `\title` 和 `\markboth{课程名}{}`。

## 2. 编译

**必须两步**，`xelatex` 在沙箱里无法直接写 PDF：

```bash
cd notes/<course>
xelatex -no-pdf -interaction=nonstopmode main.tex
xelatex -no-pdf -interaction=nonstopmode main.tex   # 第二遍填目录
xdvipdfmx main.xdv
```

不要用 `latexmk -outdir=...`：会让 `\include` 的子目录找 aux 失败。

## 3. 环境

| 用途 | 环境 | 显示名 |
|---|---|---|
| 定义 | `definition` | Definition |
| 定理 | `theorem` | Theorem |
| 命题 | `proposition` | Proposition |
| 引理 | `lemma` | Lemma |
| 推论 | `corollary` | Corollary |
| 例子 | `example` | Example |
| 注 | `remark` | Remark |
| 习题 | `exercise` | Exercise |
| 证明 | `proof` | Proof |

- **一律英文名**，正文引用写 `Definition \ref{def:xxx}`。
- 编号按节自动：`Definition 1.16`。
- **每个环境都要 `\label`**，前缀：`def:` `thm:` `prop:` `lem:` `cor:` `rem:` `thm:frobenius` 这种「前缀:含义」。
- 无标题环境直接写正文；有简短名字用 `\begin{example}[子群代数]`。
- `example` 里带 `enumerate` 时，正文首行加 `\mbox{}\par\vspace{-0.2em}`，让列表另起一行。

## 4. 语言

- **只用西文标点**：`, . ; : ?`，标点后留一个空格。不出现 `，。；：？`。
- 禁用这些手稿口吻，改写成陈述句：
  - `Q:` / `答:` → `remark` 环境
  - `一个事实是` → 直接陈述
  - `不难发现` / `不难证明` → 删掉，或补一句理由
  - `不妨设 $\exists x\in I$` → `若 $I\neq\{0\}$, 取 $0\neq x\in I$`
  - `自然, 我们考虑` → `设`
  - `下面我们` → 直接开始做
  - `显然` 每页最多留一个
- **括注要改成句子**：`(幂等)` → `这说明 $a$ 是幂等的.`
- 列表：一级 `(1) (2) (3)`，二级 `(i) (ii) (iii)`，不用 `a. b. c.`。

## 5. 数学排版

- 矩阵 `pmatrix`，行列向量 `\begin{pmatrix}...\end{pmatrix}`。
- 直和 `\oplus`，张量积 `\otimes`，理想 `\trianglelefteq` / `\trianglelefteq_l` / `\trianglelefteq_r`。
- 域：一般域一律写 `\mathbb{F}`（不用 `K`、`F`）；具体数系用 `\mathbb{R}` `\mathbb{C}` `\mathbb{Z}` `\mathbb{Q}` `\mathbb{H}`（黑体字母自动走 STIX Two 的 bb 字形）。环用 `R`，代数用 `A`，群用 `G`。
- 假设句式统一「设 $X$ 为 ……」，不写「设 $X$ 是一个 ……」。
- 交换图一律用 `tikz-cd`：`\begin{tikzcd}[row sep=1.4cm, column sep=2.4cm, arrows={->,>=stealth}]`，标签写在引号里，如 `\arrow[r,"\pi"]`、`\arrow[dr,"f"']`。不要用 `array` 手拼箭头。
- 算子用 `\operatorname{span}` `\operatorname{End}` `\operatorname{Ker}` `\operatorname{Im}`。
- display 公式前后各留一个空行，别贴着段落；短公式留在行内。
- **行内不要放大矩阵**，会把行距撑开，改 display 或 `smallmatrix`。
- 零列/零行这种「某些位置为 0」的记法：把 0 和任意元交替写出，不要用竖线分块。

## 6. 转录流程

1. 扫描件放 `scan/<course>/`，`pdfinfo` 看页数。
2. `pdftoppm -f A -l B -r 115 -png x.pdf out/p` 逐页渲染。
3. 逐页读图转写，看不清的地方用 `-r 300` 局部裁剪放大核对，**不要猜**。
4. 写入 `chapters/chNN.tex`，先编译，再抽查 3 页（开头、中间、结尾）。
5. `python tools/make_index.py` 更新索引。
6. `cp notes/<course>/main.pdf dist/<course>.pdf`。
7. commit + push（push 需要完整访问权限）。

## 7. 提交信息

```
feat(ch01): 第一章 代数 全 10 页转录
fix(ch01): 修正 Im(f) 论证方向
style: 标题页与目录分页
```

## 8. 收尾自查

- [ ] 编译零报错，无 overfull 超过 3pt
- [ ] 目录页码正确（编译两遍）
- [ ] 每个定理/定义都有 `\label`，`index/<course>.md` 条目数对得上
- [ ] 没有中文标点、没有 `Q:`、没有孤行（单字或单句独占一行）
- [ ] 数学验算：每个「显然」「不难」都问一遍是否真的成立
