# 构建入口：make epub / make pdf / make all / make clean
#
# 依赖：
#   EPUB: pandoc >= 3.1（需要 --mathml 与 epub3 支持）
#   PDF : XeLaTeX + ctex（TeX Live 的 texlive-lang-chinese）+ 中文字体

PANDOC  ?= pandoc
LATEXMK ?= latexmk

NAME    := 工程控制论（第三版）
DIST    := dist
EPUB    := $(DIST)/$(NAME).epub
PDF     := $(DIST)/$(NAME).pdf

PANDOC_FLAGS := -f latex -t epub3 \
  --mathml \
  --toc --toc-depth=3 \
  --split-level=2 \
  --resource-path=. \
  --css=epub.css \
  --metadata title="工程控制论（第三版）" \
  --metadata author="钱学森、宋健" \
  --metadata lang=zh-CN \
  --metadata publisher="科学出版社" \
  --metadata date="2011" \
  --epub-cover-image=cover.png

.PHONY: all clean epub pdf check

all: epub pdf

$(DIST):
	mkdir -p $(DIST)

epub: $(EPUB)

$(EPUB): book.tex epub.css cover.png $(wildcard figs/*.png) | $(DIST)
	$(PANDOC) $(PANDOC_FLAGS) -o "$@" book.tex

pdf: $(PDF)

$(PDF): book.tex $(wildcard figs/*.png) | $(DIST)
	$(LATEXMK) -xelatex -interaction=nonstopmode -f -outdir=$(DIST) book.tex

check:
	@command -v $(PANDOC) >/dev/null || (echo "缺少 pandoc" && exit 1)
	@command -v $(LATEXMK) >/dev/null || echo "提示：没有 latexmk 时只能构建 EPUB"

clean:
	rm -rf $(DIST) book.aux book.log book.toc book.out book.fls book.fdb_latexmk
