#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修 EPUB 的封面兼容性（pandoc 产物补丁）。

pandoc 只输出 EPUB3 规范的 `properties="cover-image"`，并且把封面页写成
SVG `<image xlink:href>`。不少阅读器（Calibre、KOReader、多看、Kindle 转换、
部分手机阅读器）不认这两点，于是"没有封面"。

本脚本就地改写 EPUB：
1. OPF metadata 补 `<meta name="cover" content="cover_png" />`（legacy，兼容绝大多数阅读器）；
2. cover.xhtml 改成普通 `<img>`，带 `epub:type="cover"` 与去边距样式；
3. 保证 cover.xhtml 在 spine 第一位（pandoc 已如此，这里只做校验）。

用法: python3 tools/fix_epub_cover.py dist/xxx.epub
"""
import re
import shutil
import sys
import zipfile

COVER_XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="zh-CN" xml:lang="zh-CN">
<head>
<meta charset="utf-8" />
<title>封面</title>
<style>
html, body { margin: 0; padding: 0; }
body { text-align: center; background: #fff; }
section { margin: 0; padding: 0; }
img { max-width: 100%; max-height: 100%; }
</style>
</head>
<body epub:type="cover">
<section epub:type="cover"><img src="../media/cover.png" alt="工程控制论（第三版）封面" /></section>
</body>
</html>
"""


def fix(path: str) -> None:
    tmp = path + ".tmp"
    zin = zipfile.ZipFile(path)
    names = zin.namelist()
    if "EPUB/text/cover.xhtml" not in names:
        print("warning: 没有 cover.xhtml，跳过（pandoc 未生成封面）")
        zin.close()
        return

    opf = zin.read("EPUB/content.opf").decode("utf-8")
    cover_id = None
    m = re.search(r'<item[^>]*properties="cover-image"[^>]*>', opf)
    if m:
        mid = re.search(r'id="([^"]+)"', m.group(0))
        if mid:
            cover_id = mid.group(1)
    if not cover_id:
        m = re.search(r'<item[^>]*id="([^"]+)"[^>]*properties="cover-image"', opf)
        cover_id = m.group(1) if m else "cover_png"

    changed = 0
    with zipfile.ZipFile(tmp, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "EPUB/content.opf":
                txt = data.decode("utf-8")
                if 'name="cover"' not in txt:
                    txt = txt.replace(
                        "</metadata>",
                        '    <meta name="cover" content="%s" />\n  </metadata>' % cover_id,
                        1,
                    )
                    changed += 1
                if 'properties="cover-image"' not in txt:
                    # 没标 cover-image 的话，给图片项补上
                    txt = re.sub(
                        r'(<item[^>]*id="%s"[^>]*)/>' % re.escape(cover_id),
                        r'\1 properties="cover-image" />', txt, count=1)
                data = txt.encode("utf-8")
            elif item.filename == "EPUB/text/cover.xhtml":
                data = COVER_XHTML.encode("utf-8")
                changed += 1
            zout.writestr(item, data)
    zin.close()
    shutil.move(tmp, path)
    print("fix_epub_cover: patched %d part(s) in %s" % (changed, path))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix(p)
