# 工程控制论（第三版）· LaTeX 源 + EPUB/PDF 构建

钱学森、宋健《工程控制论》第三版（科学出版社，2011）的 **LaTeX 重建版**：由原书 PDF 经 OCR 整理而来，一份 `book.tex` 同时产出

- **EPUB3**（公式为原生 **MathML**，可选中、可检索、可缩放）
- **PDF**（XeLaTeX + ctex + fandol 字体，由同一份源排印）

> **⚠️ 版权说明（请先读）**
>
> 本书文字、插图、公式的著作权归 **钱学森、宋健** 及 **科学出版社** 所有。
> 本仓库是**个人学习/无障碍阅读用途的数字化重建**，不是授权出版物，**不授予任何再分发许可**。
> 建议**保持仓库为 private**；若公开，请自行确认符合当地著作权法（合理使用范围），
> 并保留本文件与 [`NOTICE.md`](NOTICE.md) 的署名。权利人如有异议，请开 issue，仓库将立即删除。

---

## 致谢 · Credits

| 角色 | 署名 |
|---|---|
| **作者** | 钱学森、宋健 |
| **原出版者** | **科学出版社**（Science Press，北京，2011，ISBN 978-7-03-030094-2） |
| **第三版编辑团队** | 科学出版社《工程控制论》第三版编辑组与责任编辑 —— 本书的章节结构、公式编号、图注编号、版式皆沿用他们的成果 |
| 原英文版 | *Engineering Cybernetics*, McGraw-Hill, 1954（钱学森 著） |
| 修订工作 | 于景元（第十二章）、林金、郭孝宽（第十三章）、唐志强（第十四、十五章）等，见原书前言 |
| 排版/OCR 工具 | [Pandoc](https://pandoc.org/)（LaTeX → EPUB3/MathML）、XeLaTeX + [ctex](https://ctan.org/pkg/ctex)、[PyMuPDF](https://pymupdf.readthedocs.io/)、[qwen-vl-ocr](https://help.aliyun.com/zh/model-studio/qwenvl-ocr) |

原书内容的一切功劳归于作者与科学出版社的编辑们；本仓库只做了「PDF → 结构化文本」这一步搬运工作，其中的 OCR 错漏与原书无关。

---

## 数据规模

| 项 | 值 |
|---|---|
| 篇幅 | 上册 543 页 + 下册 524 页 = 1067 页 |
| 结构 | 2 册 / 21 章 / 约 250 节，三级目录 |
| 正文 | 约 8,900 段、46 万字（汉字） |
| 公式 | 4,700+ 个显示公式、25,000+ 个 MathML 元素，2,458 条保留原书编号 |
| 插图 | 420 张（按原版位置嵌入，365 张带图注） |
| 产物体积 | EPUB ≈ 5.4 MB；PDF 视字体而定 |

## 构建

### 本地

```bash
# 只需要 pandoc 就能出 EPUB
brew install pandoc            # 或 apt install pandoc / 下载 3.5+ 二进制
make epub                      # → dist/工程控制论（第三版）.epub

# 出 PDF 需要 TeX Live（含 ctex 与中文字体）
make pdf                       # → dist/工程控制论（第三版）.pdf
make all                       # 两个都出
```

### CI（GitHub Actions）

[`.github/workflows/build.yml`](.github/workflows/build.yml) 在 push / PR / tag 时：

1. `epub` job：装 pandoc 3.5 → `make epub` → 上传 artifact；
2. `pdf` job：装 TeX Live（`texlive-xetex` `texlive-lang-chinese`）+ `fonts-noto-cjk` → `make pdf` → 上传 artifact（允许失败，不阻塞发布）；
3. `release` job：**打 `v*` tag 时**把 EPUB + PDF 附到 GitHub Release。

发版方式：

```bash
git tag v1.0.0 && git push origin v1.0.0
```

## 目录结构

```
book.tex              # 唯一的源文件（约 3 MB，29k 行）
figs/                 # 420 张插图（从原 PDF 按图区裁切渲染）
cover.png             # 封面
epub.css              # EPUB 样式（中文衬线体、段首缩进、公式居中）
Makefile              # make epub / pdf / all
.github/workflows/    # CI：构建 + 发版
NOTICE.md             # 版权与署名（务必保留）
```

## 这份 LaTeX 是怎么来的

```
原书 PDF（带文字层，但字体 ToUnicode 损坏、公式是二维排版）
   ├─ 逐页 OCR（qwen-vl-ocr）→ 带 LaTeX 公式的纯文本
   ├─ 用 PDF 书签恢复 21 章 / 250 节结构；文字层回填公式编号与图注
   ├─ 字形错位修复（唱→-、倡→*、矪→∂、枙枛→⟨⟩ 等 24 条，逐条对照页面图核过）
   ├─ 每段公式过 KaTeX 校验，失败则修补 / 降级，最终 0 残留 TeX 源码
   └─ book.tex ──pandoc──▶ EPUB3(MathML) ──XeLaTeX──▶ PDF
```

校对记录（1067 页逐页与 PDF 文字层比对）显示：汉字层面相似度均值 **0.997**，52% 的页逐字一致。

## 已知问题

- **MathML 兼容性**：Apple Books / Calibre / Thorium 支持良好；部分老旧阅读器（Kobo、部分安卓）对 MathML 支持弱，公式可能退化为线性文本。
- 少量 OCR 漏字/误读（如「那么」→「么」、「令」→「∴」、术语「轨线/轨迹」），未做逐字人工校对。
- 约 19 页与 PDF 文字层的相似度 < 0.97，多为版权页、整页插图页（分母小）。
- 标点以中文全角为主，个别参考文献条目保留半角。
