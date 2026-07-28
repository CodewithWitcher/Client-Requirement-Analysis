#!/usr/bin/env python3
"""
Intelligent Combined Document Generator
Programmatically merges Web + App document pairs by:
  1. Splitting both files into sections (by ## heading)
  2. Matching sections with normalized fuzzy keys
  3. Merging matched sections side-by-side (showing both web + app data)
  4. Keeping platform-unique sections with a [🌐 Web] or [📱 App] label
  5. Removing all duplication

Run: py scripts/generate_combined.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMBINED_DIR = ROOT / "combined"
COMBINED_DIR.mkdir(exist_ok=True)


# ─── Section Parser ──────────────────────────────────────────────────────────

def parse_sections(text: str):
    """Split markdown into (heading_line, body) pairs. Index 0 = intro (before first ##)."""
    pattern = re.compile(r'^(## .+)$', re.MULTILINE)
    parts = pattern.split(text)
    # parts = [pre_content, heading1, body1, heading2, body2, ...]
    sections = []
    intro = parts[0].strip()
    i = 1
    while i < len(parts) - 1:
        heading = parts[i].strip()
        body = parts[i + 1].strip()
        sections.append((heading, body))
        i += 2
    return intro, sections


def normalize_key(heading: str) -> str:
    """Strip emojis, numbers, punctuation and lowercase for fuzzy matching."""
    # Remove emoji unicode ranges
    h = re.sub(r'[^\x20-\x7E]', '', heading)
    # Remove leading numbering like "1." "20." etc
    h = re.sub(r'^#+\s*', '', h)
    h = re.sub(r'^\d+[\.\)]\s*', '', h)
    # Remove special chars, lowercase
    h = re.sub(r'[&/\\|]', ' ', h)
    h = re.sub(r'[^a-z0-9\s]', '', h.lower())
    h = re.sub(r'\s+', ' ', h).strip()
    return h


def match_sections(web_sections, app_sections):
    """
    Match web sections to app sections by normalized heading key.
    Returns:
      matched: list of (web_heading, web_body, app_heading, app_body)
      web_only: list of (heading, body)  — sections only in web
      app_only: list of (heading, body)  — sections only in app
    """
    web_keys = [(normalize_key(h), h, b) for h, b in web_sections]
    app_keys = [(normalize_key(h), h, b) for h, b in app_sections]

    matched = []
    used_app = set()

    for wkey, wh, wb in web_keys:
        best_match = None
        best_score = 0
        for i, (akey, ah, ab) in enumerate(app_keys):
            if i in used_app:
                continue
            score = key_similarity(wkey, akey)
            if score > best_score:
                best_score = score
                best_match = i
        if best_score >= 0.55:
            akey, ah, ab = app_keys[best_match]
            matched.append((wh, wb, ah, ab))
            used_app.add(best_match)
        else:
            matched.append((wh, wb, None, None))

    app_only = [(ah, ab) for i, (akey, ah, ab) in enumerate(app_keys) if i not in used_app]

    return matched, app_only


def key_similarity(a: str, b: str) -> float:
    """Simple word-overlap similarity score between two normalized strings."""
    if a == b:
        return 1.0
    wa = set(a.split())
    wb = set(b.split())
    if not wa or not wb:
        return 0.0
    intersection = wa & wb
    return len(intersection) / max(len(wa), len(wb))

# ─── Content Merger ──────────────────────────────────────────────────────────

def merge_section_bodies(web_body: str, app_body: str, web_label="🌐 Website", app_label="📱 Application") -> str:
    """
    Intelligently merge two section bodies:
    - If bodies are nearly identical (>80%) → keep one (de-duplicated)
    - If moderate similarity (50-80%) → shared base + unique additions labeled
    - If low similarity (<50%) → both shown fully with platform sub-headings
    """
    web_body = web_body.strip()
    app_body = app_body.strip()

    if not web_body:
        return f"**{app_label}**\n\n{app_body}"
    if not app_body:
        return f"**{web_label}**\n\n{web_body}"

    sim = text_similarity(web_body, app_body)

    # Nearly identical → de-duplicate, keep longer version
    if sim >= 0.80:
        return web_body if len(web_body) >= len(app_body) else app_body

    # Moderately similar → shared base + platform-unique additions
    if sim >= 0.50:
        web_lines = web_body.splitlines()
        app_lines_set = set(app_body.splitlines())
        web_lines_set = set(web_lines)

        app_unique = [l for l in app_body.splitlines() if l not in web_lines_set]
        unique_text = "\n".join(app_unique).strip()

        result = web_body
        if unique_text:
            result += f"\n\n**{app_label} Additional:**\n\n{unique_text}"
        return result

    # Low similarity → show both fully, clearly labeled
    return (
        f"**{web_label}**\n\n"
        f"{web_body}\n\n"
        f"---\n\n"
        f"**{app_label}**\n\n"
        f"{app_body}"
    )



def text_similarity(a: str, b: str) -> float:
    """Word-level Jaccard similarity of two text bodies."""
    wa = set(re.findall(r'\w+', a.lower()))
    wb = set(re.findall(r'\w+', b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def platform_label_heading(heading: str, platform: str) -> str:
    """Add a platform badge to a heading."""
    badge = "🌐" if platform == "web" else "📱"
    clean_h = re.sub(r'^#+\s*', '', heading.strip())
    return f"## {badge} {clean_h}"


# ─── Full Document Builder ────────────────────────────────────────────────────

def build_combined_md(
    title: str,
    description: str,
    web_path: Path,
    app_path: Path,
    out_path: Path
):
    web_text = web_path.read_text(encoding="utf-8", errors="replace")
    app_text = app_path.read_text(encoding="utf-8", errors="replace")

    web_intro, web_sections = parse_sections(web_text)
    app_intro, app_sections = parse_sections(app_text)

    matched, app_only = match_sections(web_sections, app_sections)

    lines = []

    # ── Header ──
    lines.append(f"# {title}\n")
    lines.append(f"> {description}\n")
    lines.append("> **Covers:** 🌐 Website / Web App &nbsp;|&nbsp; 📱 Mobile Application\n")
    lines.append("---\n")

    # ── Merged sections ──
    for wh, wb, ah, ab in matched:
        if ah is None:
            # Web-only section — label it clearly
            clean_wh = re.sub(r'^#+\s*', '', wh.strip())
            lines.append(f"## 🌐 {clean_wh}")
            lines.append("")
            lines.append(wb.strip())
            lines.append("\n---\n")
        else:
            sim = text_similarity(wb, ab)

            # Build unified heading: merge both headings, removing platform-prefix words
            wh_clean = re.sub(r'^#+\s*', '', wh.strip())
            ah_clean = re.sub(r'^#+\s*', '', ah.strip())
            # Use whichever heading is more descriptive (longer)
            unified_h = wh_clean if len(wh_clean) >= len(ah_clean) else ah_clean

            if sim >= 0.80:
                # Nearly identical → single unified section, no labels needed
                lines.append(f"## {unified_h}")
                lines.append("")
                body = wb if len(wb) >= len(ab) else ab
                lines.append(body.strip())

            elif sim >= 0.45:
                # Moderately similar → unified heading + merged body with app additions
                lines.append(f"## {unified_h}")
                lines.append("")
                merged_body = merge_section_bodies(wb, ab)
                lines.append(merged_body.strip())

            else:
                # Very different content → show both with clear platform sub-headings
                lines.append(f"## {unified_h}")
                lines.append("")
                lines.append(f"### 🌐 Website")
                lines.append("")
                lines.append(wb.strip())
                lines.append("")
                lines.append(f"### 📱 Mobile Application")
                lines.append("")
                lines.append(ab.strip())

            lines.append("\n---\n")

    # ── App-only sections ──
    for ah, ab in app_only:
        clean_ah = re.sub(r'^#+\s*', '', ah.strip())
        lines.append(f"## 📱 {clean_ah}")
        lines.append("")
        lines.append(ab.strip())
        lines.append("\n---\n")

    combined = "\n".join(lines)
    out_path.write_text(combined, encoding="utf-8")
    total_lines = combined.count("\n")
    print(f"  [COMBINED-MD] {out_path.name}  ({total_lines} lines, {len(combined)//1024} KB)")


# ─── Excel Merger ────────────────────────────────────────────────────────────

def merge_excel(app_path: Path, web_path: Path, out_path: Path, title: str):
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment

    app_wb = openpyxl.load_workbook(app_path, data_only=True)
    web_wb = openpyxl.load_workbook(web_path, data_only=True)

    combined_wb = openpyxl.Workbook()
    combined_wb.remove(combined_wb.active)

    # Summary sheet
    s = combined_wb.create_sheet("Combined Summary", 0)
    hdr_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    web_fill = PatternFill(start_color="1E3A5F", end_color="1E3A5F", fill_type="solid")
    app_fill = PatternFill(start_color="1E3D2F", end_color="1E3D2F", fill_type="solid")
    white_bold = Font(name="Calibri", bold=True, color="FFFFFF", size=12)
    normal = Font(name="Calibri", size=11)

    s["A1"] = title
    s["A1"].fill = hdr_fill
    s["A1"].font = white_bold

    s["A2"] = "Unified pricing calculator covering Website and Mobile Application projects."
    s["A2"].font = normal

    s.append([])
    s.append(["Section", "Source", "Sheets"])
    for cell in s[4]:
        cell.fill = hdr_fill
        cell.font = white_bold

    s.append(["Website Pricing", "Website-Pricing-Calculator.xlsx", ", ".join(web_wb.sheetnames)])
    s.append(["Application Pricing", "Application-Pricing-Calculator.xlsx", ", ".join(app_wb.sheetnames)])
    s.column_dimensions["A"].width = 35
    s.column_dimensions["B"].width = 45
    s.column_dimensions["C"].width = 40

    def copy_wb_sheets(src_wb, prefix, fill):
        bold_white = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
        for name in src_wb.sheetnames:
            src = src_wb[name]
            dest_name = f"{prefix} - {name}"[:31]
            dst = combined_wb.create_sheet(dest_name)
            for col_l, col_d in src.column_dimensions.items():
                dst.column_dimensions[col_l].width = col_d.width
            for rn, rd in src.row_dimensions.items():
                dst.row_dimensions[rn].height = rd.height
            for row in src.iter_rows():
                for cell in row:
                    dc = dst.cell(row=cell.row, column=cell.column)
                    dc.value = cell.value
                    if cell.has_style:
                        try:
                            dc.font = cell.font.copy()
                            dc.border = cell.border.copy()
                            dc.fill = cell.fill.copy()
                            dc.number_format = cell.number_format
                            dc.alignment = cell.alignment.copy()
                        except Exception:
                            pass
            dst.insert_rows(1)
            h = dst.cell(row=1, column=1)
            h.value = f"{prefix}: {name}"
            h.fill = fill
            h.font = bold_white
            h.alignment = Alignment(horizontal="left", vertical="center")

    copy_wb_sheets(web_wb, "WEB", web_fill)
    copy_wb_sheets(app_wb, "APP", app_fill)
    combined_wb.save(out_path)
    print(f"  [COMBINED-XLSX] {out_path.name}")


# ─── DOCX Merger ─────────────────────────────────────────────────────────────

def merge_docx(app_path: Path, web_path: Path, out_path: Path, title: str, description: str):
    """
    Intelligently merge two DOCX files using python-docx.
    Extracts paragraphs from both, groups by heading sections,
    matches shared sections, merges unique sections with platform labels.
    """
    import docx
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    def extract_sections_from_docx(path):
        d = docx.Document(path)
        sections = []
        current_heading = None
        current_paras = []
        for para in d.paragraphs:
            if para.style.name.startswith("Heading 1") and not current_heading:
                # Skip document title
                continue
            elif para.style.name.startswith("Heading"):
                if current_heading is not None:
                    sections.append((current_heading, list(current_paras)))
                current_heading = para.text.strip()
                current_paras = []
            else:
                current_paras.append(para)
        if current_heading:
            sections.append((current_heading, list(current_paras)))
        return sections

    web_sections = extract_sections_from_docx(web_path)
    app_sections = extract_sections_from_docx(app_path)

    matched, app_only = match_sections(
        [(h, "\n".join(p.text for p in ps)) for h, ps in web_sections],
        [(h, "\n".join(p.text for p in ps)) for h, ps in app_sections]
    )

    combined = docx.Document()
    combined.styles["Normal"].font.name = "Calibri"
    combined.styles["Normal"].font.size = Pt(11)

    # Title
    t = combined.add_heading(title, level=1)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    combined.add_paragraph(description)
    combined.add_paragraph(
        "Covers: Website / Web Application Projects | Mobile Application Projects"
    )
    combined.add_page_break()

    # Build lookup: heading → paragraph list
    web_para_map = {h: ps for h, ps in web_sections}
    app_para_map = {h: ps for h, ps in app_sections}

    for wh, wb_text, ah, ab_text in matched:
        if ah is None:
            # Web-only
            combined.add_heading(f"[WEB] {wh}", level=2)
            for para in web_para_map.get(wh, []):
                if para.text.strip():
                    combined.add_paragraph(para.text, style="Normal")
        else:
            sim = text_similarity(wb_text, ab_text)
            # Unified heading
            clean_h = re.sub(r'[^\x20-\x7E]', '', wh).strip()
            combined.add_heading(clean_h, level=2)

            if sim >= 0.75:
                # Mostly same — use web version (longer/more complete)
                base = web_para_map.get(wh, []) if len(wb_text) >= len(ab_text) else app_para_map.get(ah, [])
                for para in base:
                    if para.text.strip():
                        combined.add_paragraph(para.text, style="Normal")
            else:
                # Show web content, then app-specific additions
                combined.add_heading("Website", level=3)
                for para in web_para_map.get(wh, []):
                    if para.text.strip():
                        combined.add_paragraph(para.text, style="Normal")
                combined.add_heading("Mobile Application", level=3)
                for para in app_para_map.get(ah, []):
                    if para.text.strip():
                        combined.add_paragraph(para.text, style="Normal")

    for ah, _ in app_only:
        combined.add_heading(f"[APP] {ah}", level=2)
        for para in app_para_map.get(ah, []):
            if para.text.strip():
                combined.add_paragraph(para.text, style="Normal")

    combined.save(out_path)
    print(f"  [COMBINED-DOCX] {out_path.name}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("[SMART COMBINED] Generating Intelligently Merged Documents")
    print("=" * 60)
    COMBINED_DIR.mkdir(exist_ok=True)

    tasks = [
        # (type, title, description, web_path, app_path, out_filename)
        ("md", "Pricing Module — Complete Overview",
         "Comprehensive overview of the pricing module system for both Website and Mobile Application projects. Covers architecture, methodology, all parameter categories, and reference costs.",
         ROOT / "overview/Website-Pricing-Module-Overview.md",
         ROOT / "overview/Application-Pricing-Module-Overview.md",
         "Combined-Pricing-Module-Overview.md"),

        ("md", "Pricing Quick Reference Guide",
         "Fast-reference pricing guide for full-stack client engagements covering pricing formulas, cost ranges, key drivers, technology recommendations, and common pitfalls for both Website and Mobile App projects.",
         ROOT / "overview/Website-Pricing-Quick-Guide.md",
         ROOT / "overview/Application-Pricing-Quick-Guide.md",
         "Combined-Pricing-Quick-Guide.md"),

        ("md", "Project Delivery Checklist",
         "Full-scope project delivery checklist covering all phases — from client discovery through post-launch — for both Website and Mobile Application engagements.",
         ROOT / "checklists/Website-Project-Checklist.md",
         ROOT / "checklists/Application-Project-Checklist.md",
         "Combined-Project-Checklist.md"),

        ("md", "Client Discovery Questionnaire",
         "All-in-one structured client questionnaire for scoping both Website and Mobile Application projects in a single intake session. Covers business overview, technical requirements, design, features, integrations, and commercial terms.",
         ROOT / "Questionnaire/website/Website-Client-Questionnaire.md",
         ROOT / "Questionnaire/application/Application-Client-Questionnaire.md",
         "Combined-Client-Questionnaire.md"),

        ("md", "Requirements Complete Guide",
         "Master reference guide documenting all technical requirement categories for both Website and Mobile Application projects — ideal for comprehensive scoping, proposal writing, and technical specification.",
         ROOT / "docs/website/Website-Requirements-Complete-Guide.md",
         ROOT / "docs/application/Application-Requirements-Complete-Guide.md",
         "Combined-Requirements-Complete-Guide.md"),

        ("md", "Pricing Parameters Reference",
         "Unified pricing parameters sheet covering all cost line items, complexity multipliers, and estimation formulas for both Website and Mobile Application engagements.",
         ROOT / "docs/website/Website-Pricing-Parameters.md",
         ROOT / "docs/application/Application-Pricing-Parameters.md",
         "Combined-Pricing-Parameters.md"),
    ]

    for task in tasks:
        kind = task[0]
        title, description, web_path, app_path, out_filename = task[1], task[2], task[3], task[4], task[5]
        out_path = COMBINED_DIR / out_filename
        print(f"\n  Processing: {out_filename}")
        try:
            build_combined_md(title, description, web_path, app_path, out_path)
        except Exception as e:
            print(f"  [ERROR] {out_filename}: {e}")
            import traceback; traceback.print_exc()

    # Excel — combined workbook (separate sheets per platform, no meaningful dedup possible)
    print("\n  Processing: Combined-Pricing-Calculator.xlsx")
    try:
        merge_excel(
            app_path=ROOT / "Template/excel template/Application-Pricing-Calculator.xlsx",
            web_path=ROOT / "Template/excel template/Website-Pricing-Calculator.xlsx",
            out_path=COMBINED_DIR / "Combined-Pricing-Calculator.xlsx",
            title="Combined Web + App Pricing Calculator"
        )
    except Exception as e:
        print(f"  [ERROR] Combined-Pricing-Calculator.xlsx: {e}")
        import traceback; traceback.print_exc()

    # DOCX Proposal — intelligent merge
    print("\n  Processing: Combined-Client-Proposal.docx")
    try:
        merge_docx(
            app_path=ROOT / "Template/word template/Application-Client-Proposal.docx",
            web_path=ROOT / "Template/word template/Website-Client-Proposal.docx",
            out_path=COMBINED_DIR / "Combined-Client-Proposal.docx",
            title="Combined Web + App Client Proposal",
            description="Full-stack client proposal covering Website and Mobile Application scope, pricing, deliverables, and terms in a single document."
        )
    except Exception as e:
        print(f"  [ERROR] Combined-Client-Proposal.docx: {e}")
        import traceback; traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Combined documents written to: {COMBINED_DIR}")
    print("=" * 60)
    for f in sorted(COMBINED_DIR.iterdir()):
        kb = f.stat().st_size / 1024
        print(f"  {f.name:<50} {kb:>7.1f} KB")


if __name__ == "__main__":
    main()
