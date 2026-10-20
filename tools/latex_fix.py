#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF 编译前的 LaTeX 修补（EPUB 不需要）：

OCR 输出的 `\\begin{array}{spec}` 常把列数数错，XeLaTeX 会报
"Extra alignment tab"，这里按实际 `&` 数重建列声明。

用法: python3 tools/latex_fix.py book.tex book.build.tex
"""
import re
import sys


def fix_arrays(tex: str):
    pat = re.compile(r"\\begin\{array\}\{([^{}]*)\}([\s\S]*?)\\end\{array\}")
    fixed = 0

    def repl(m):
        nonlocal fixed
        spec, body = m.group(1), m.group(2)
        rows = body.split(r"\\")
        cols = max(r.count("&") for r in rows) + 1
        letters = re.sub(r"[^lcr]", "", spec)
        if len(letters) == cols:
            return m.group(0)
        fixed += 1
        if not letters:
            letters = "c"
        new = (letters * cols)[:cols] if len(letters) < cols else letters[:cols]
        return r"\begin{array}{%s}%s\end{array}" % (new, body)

    return pat.sub(repl, tex), fixed


def main():
    src, dst = sys.argv[1], sys.argv[2]
    tex = open(src, encoding="utf-8").read()
    tex, n = fix_arrays(tex)
    open(dst, "w", encoding="utf-8").write(tex)
    print("latex_fix: array specs repaired =", n)


if __name__ == "__main__":
    main()
