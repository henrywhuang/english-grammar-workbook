import importlib.util
import re
from pathlib import Path

import pdfplumber
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


SOURCE_PDF = "English_Grammar_Knowledge_Outline_CN.pdf"
TARGETS = [
    Path("English_Grammar_Knowledge_Outline_CN.pdf"),
    Path("English_Grammar_Knowledge_Outline_CN (1).pdf"),
]

FONT = "Songti"
pdfmetrics.registerFont(TTFont(FONT, "/System/Library/Fonts/Supplemental/Songti.ttc", subfontIndex=0))

PAGE_W, PAGE_H = letter
MARGIN_X = 54
TOP = PAGE_H - 48
BOTTOM = 42


def load_workbook_module():
    spec = importlib.util.spec_from_file_location("grammar_workbook", "scripts/generate_complete_grammar_workbook.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outline_lines():
    skip = {
        "语法知识点大纲",
        "英语语法知识体系 · 结构化目录版",
        "STRUCTURED OUTLINE · 结构化大纲",
        "第一部分",
    }
    rows = []
    item_no = 1
    with pdfplumber.open(SOURCE_PDF) as pdf:
        raw_lines = []
        for page in pdf.pages:
            raw_lines.extend((page.extract_text() or "").splitlines())
    for raw in raw_lines:
        line = raw.strip()
        if not line or line in skip or line.isdigit():
            continue
        if line.startswith("·"):
            topic = re.sub(r"^\d{3}\s+", "", line[1:].strip())
            rows.append(("bullet", f"· {item_no:03d} {topic}"))
            item_no += 1
        elif line.startswith(("一、", "二、", "三、")):
            rows.append(("part", line))
        elif re.match(r"^\d+(\.\d+)?\s+", line):
            rows.append(("section", line))
        else:
            rows.append(("sub", line))
    if item_no - 1 != 286:
        raise RuntimeError(f"Expected 286 numbered grammar points, found {item_no - 1}")
    return rows


def wrap_text(text, size, max_width):
    lines = []
    line = ""
    for ch in text:
        candidate = line + ch
        if pdfmetrics.stringWidth(candidate, FONT, size) <= max_width or not line:
            line = candidate
        else:
            lines.append(line.rstrip())
            line = ch.lstrip()
    if line:
        lines.append(line.rstrip())
    return lines


def draw_wrapped(c, text, x, y, size, leading, max_width, fill):
    c.setFont(FONT, size)
    c.setFillColor(fill)
    for line in wrap_text(text, size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_page_header(c, page_no):
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(FONT, 10)
    c.drawString(MARGIN_X, PAGE_H - 28, "英语语法知识体系 · 编号索引版")
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(MARGIN_X, PAGE_H - 36, PAGE_W - MARGIN_X, PAGE_H - 36)
    c.setFont(FONT, 8.2)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PAGE_W - MARGIN_X, 24, f"Grammar Outline Index | Page {page_no}")


def render_outline(path, rows):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("英语语法知识体系 编号索引版")

    page_no = 1
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont(FONT, 21)
    c.drawString(MARGIN_X, TOP, "语法知识点大纲")
    c.setFont(FONT, 12)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(MARGIN_X, TOP - 24, "英语语法知识体系 · 编号索引版")
    c.drawString(MARGIN_X, TOP - 42, "STRUCTURED OUTLINE · NUMBERED INDEX")
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(MARGIN_X, TOP - 56, PAGE_W - MARGIN_X, TOP - 56)
    y = TOP - 86
    c.setFont(FONT, 10.5)
    c.setFillColor(colors.HexColor("#374151"))
    c.drawString(MARGIN_X, y, "说明：每个圆点语法点前的 001-286 编号，与完整 worksheet 题册中的语法点编号一一对应。")
    y -= 34

    for kind, text in rows:
        if kind == "part":
            size, leading, gap, color, indent = 14, 19, 10, colors.HexColor("#111827"), 0
        elif kind == "section":
            size, leading, gap, color, indent = 11.3, 15.5, 5, colors.HexColor("#1F2937"), 10
        elif kind == "sub":
            size, leading, gap, color, indent = 10.2, 14, 3, colors.HexColor("#475569"), 20
        else:
            size, leading, gap, color, indent = 9.2, 12.5, 1, colors.HexColor("#111827"), 30
        needed = len(wrap_text(text, size, PAGE_W - 2 * MARGIN_X - indent)) * leading + gap
        if y - needed < BOTTOM:
            c.showPage()
            page_no += 1
            draw_page_header(c, page_no)
            y = TOP
        y = draw_wrapped(c, text, MARGIN_X + indent, y, size, leading, PAGE_W - 2 * MARGIN_X - indent, color)
        y -= gap
    c.save()


def main():
    workbook = load_workbook_module()
    topics = workbook.extract_topics()
    if len(topics) != 286:
        raise RuntimeError(f"Workbook extractor expected 286 topics, found {len(topics)}")
    rows = outline_lines()
    for target in TARGETS:
        render_outline(target, rows)
        print(target)


if __name__ == "__main__":
    main()
