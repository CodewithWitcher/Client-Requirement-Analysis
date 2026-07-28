#!/usr/bin/env python3
"""
Document Hub & Interactive Static Site Generator
Scans repository for .md, .xlsx, .xls, .doc, and .docx files, converts all 18 documents into HTML pages,
builds a categorized, bucket-structured landing page (`docs/index.html`) with Smart Assistant Wizard, AI Document Analyzer,
and Client-Provided API Key Manager.

Run:
  python scripts/build_site.py
  or:
  py scripts/build_site.py
"""

import os
import sys
import re
import shutil
import datetime
import html
from pathlib import Path

# Python document parsing dependencies
import markdown
import openpyxl
import docx
import mammoth


# ─── Configuration & Directories ──────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "docs"
PAGES_DIR = OUTPUT_DIR / "pages"
FILES_DIR = OUTPUT_DIR / "files"
ASSETS_DIR = OUTPUT_DIR / "assets"

SUPPORTED_EXTENSIONS = {".md", ".docx", ".doc", ".xlsx", ".xls"}

IGNORE_DIRS = {
    ".git", ".github", ".gemini", "node_modules", "venv", "env",
    "__pycache__", "build", "dist", "site", ".pytest_cache"
}

# Secondary/Reference markdown filenames to exclude from the main landing page (but include in File Explorer)
LANDING_EXCLUDE_FILENAMES = {
    "Application-Pricing-Parameters.md",
    "Website-Pricing-Parameters.md",
    "Application-Pricing-Module-Overview.md",
    "Application-Pricing-Quick-Guide.md",
    "Website-Pricing-Module-Overview.md",
    "Website-Pricing-Quick-Guide.md",
    "Readme1.md"
}


# ─── Utility Functions ───────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert string into clean URL-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'document'


def format_bytes(size_bytes: int) -> str:
    """Format byte count into human readable KB / MB."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def get_file_type_info(ext: str):
    """Return badge info and category for file extension."""
    ext = ext.lower()
    if ext == ".md":
        return {"category": "md", "badge_class": "badge-md", "label": "MD"}
    elif ext in {".docx", ".doc"}:
        return {"category": "docx", "badge_class": "badge-docx", "label": "DOCX"}
    elif ext in {".xlsx", ".xls"}:
        return {"category": "xlsx", "badge_class": "badge-xlsx", "label": "XLSX"}
    return {"category": "other", "badge_class": "badge-md", "label": ext.upper().strip('.')}


def get_document_topics(file_path: Path):
    """Classify document by domain topic (web, mobile, pricing, combined)."""
    rel_str = str(file_path).lower()
    topics = []

    # Combined documents (merged web + app into one file)
    if "combined" in rel_str or str(file_path.parent).lower().endswith("combined"):
        topics.append("combined")
        topics.append("web")
        topics.append("mobile")
        if "pricing" in rel_str or "calculator" in rel_str or "proposal" in rel_str or "cost" in rel_str:
            topics.append("pricing")
        return topics

    if "website" in rel_str or "web" in rel_str:
        topics.append("web")
    if "application" in rel_str or "mobile" in rel_str or "app" in rel_str:
        topics.append("mobile")
    if "pricing" in rel_str or "calculator" in rel_str or "proposal" in rel_str or "cost" in rel_str:
        topics.append("pricing")

    if not topics:
        topics.append("general")

    return topics


# ─── Document Converters ──────────────────────────────────────────────────

def parse_markdown_file(file_path: Path):
    """Convert Markdown file to HTML with 2-column TOC sidebar and interactive scope selectors."""
    content = file_path.read_text(encoding="utf-8", errors="replace")
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem.replace('-', ' ').replace('_', ' ').title()

    cb_count = 0
    def replace_task_cb(match):
        nonlocal cb_count
        matched_str = match.group(0)
        checked = 'checked' if (matched_str in {'☑', '☒'} or (len(matched_str) >= 3 and matched_str[1].lower() == 'x')) else ''
        cb_html = f'<input type="checkbox" class="interactive-checklist-item" data-cb-id="cb-{cb_count}" {checked}>'
        cb_count += 1
        return cb_html

    # Replace both [ ] / [x] and literal Unicode ballot boxes ☐ / ☑ / ☒
    processed_content = re.sub(r'(?:\[[ xX]\]|[☐☑☒])', replace_task_cb, content)

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'attr_list', 'nl2br'])
    rendered_html = md.convert(processed_content)

    headings = re.findall(r'<h([23])\s+id="([^"]+)">([^<]+)</h[23]>', rendered_html)
    toc_items_html = []
    sec_count = 0

    for level, head_id, head_text in headings:
        indent = 'style="padding-left: 0.75rem;"' if level == '3' else ''
        clean_head_text = re.sub(r'^[0-9\.]+\s*', '', head_text).strip()
        toc_items_html.append(f'<li {indent}><a href="#{head_id}">📌 {html.escape(clean_head_text)}</a></li>')

        sec_id = f"sec_{sec_count}"
        scope_btn = f'<div class="section-scope-header"><h{level} id="{head_id}">{head_text}</h{level}><button class="section-scope-btn" data-sec-id="{sec_id}">+ Add to Scope</button></div>'
        rendered_html = rendered_html.replace(f'<h{level} id="{head_id}">{head_text}</h{level}>', scope_btn)
        sec_count += 1

    sidebar_toc_html = ""
    if toc_items_html:
        sidebar_toc_html = f'''
        <aside class="doc-sidebar-toc">
          <div class="toc-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"></line>
              <line x1="8" y1="12" x2="21" y2="12"></line>
              <line x1="8" y1="18" x2="21" y2="18"></line>
              <line x1="3" y1="6" x2="3.01" y2="6"></line>
              <line x1="3" y1="12" x2="3.01" y2="12"></line>
              <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
            <span>Table of Contents</span>
          </div>
          <ul class="toc-list">
            {"".join(toc_items_html)}
          </ul>
        </aside>
        '''

    progress_bar_html = ""
    if cb_count > 0:
        progress_bar_html = f'''
        <div class="summary-card" style="margin-bottom: 2rem; background: rgba(59, 130, 246, 0.05);">
          <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 0.5rem;">
            <span>Task Checklist Progress</span>
            <span id="checklist-progress-text">0 of {cb_count} completed (0%)</span>
          </div>
          <div style="height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden;">
            <div id="checklist-progress-bar" style="height: 100%; width: 0%; background: var(--accent-primary); transition: width 0.3s ease;"></div>
          </div>
        </div>
        '''

    clean_text = re.sub(r'<[^>]+>', ' ', rendered_html)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    words = clean_text.split()
    word_count = len(words)
    excerpt = clean_text[:220] + ("..." if len(clean_text) > 220 else "")

    return {
        "title": title,
        "html": f'{rendered_html}',
        "sidebar_toc": sidebar_toc_html,
        "progress_bar": progress_bar_html,
        "excerpt": excerpt,
        "word_count": word_count,
        "meta_label": f"{word_count:,} words",
        "read_time": f"{max(1, word_count // 200)} min read"
    }


def parse_docx_file(file_path: Path):
    """Convert Word (.docx) file to HTML using Mammoth and python-docx fallback."""
    title = file_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    try:
        with open(file_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            raw_html = result.value
            
            processed_html = raw_html.replace('<table>', '<div class="table-responsive"><table class="doc-table">')
            processed_html = processed_html.replace('</table>', '</table></div>')
    except Exception as e:
        print(f"  [Warning] Mammoth conversion failed for {file_path.name}: {e}. Using fallback.")
        try:
            doc = docx.Document(file_path)
            paragraphs_html = []
            for p in doc.paragraphs:
                if p.text.strip():
                    paragraphs_html.append(f'<p>{html.escape(p.text)}</p>')
            processed_html = "\n".join(paragraphs_html)
        except Exception as e2:
            processed_html = f'<p class="error-msg">Error rendering Word document: {html.escape(str(e2))}</p>'

    clean_text = re.sub(r'<[^>]+>', ' ', processed_html)
    words = clean_text.split()
    word_count = len(words)
    excerpt = clean_text[:220] + ("..." if len(clean_text) > 220 else "")

    return {
        "title": title,
        "html": f'<div class="rendered-docx">{processed_html}</div>',
        "sidebar_toc": "",
        "progress_bar": "",
        "excerpt": excerpt,
        "word_count": word_count,
        "meta_label": f"{word_count:,} words",
        "read_time": f"{max(1, word_count // 200)} min read"
    }


def parse_excel_file(file_path: Path):
    """Convert Excel (.xlsx) sheets into live interactive pricing tables."""
    title = file_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet_names = wb.sheetnames
        
        tab_buttons = []
        tab_panes = []
        total_rows = 0

        for i, sheet_name in enumerate(sheet_names):
            ws = wb[sheet_name]
            is_active = "active" if i == 0 else ""
            sheet_id = f"sheet-{i}"

            tab_buttons.append(
                f'<button class="sheet-tab-btn {is_active}" data-sheet-target="{sheet_id}">'
                f'📊 {html.escape(sheet_name)}</button>'
            )

            table_rows = []
            max_r = ws.max_row or 0
            max_c = ws.max_column or 0
            if max_r > 0: total_rows += max_r

            is_calculator_sheet = ("calculator" in sheet_name.lower()) or ("pricing" in sheet_name.lower())

            for r_idx in range(1, min(max_r + 1, 300)):
                row_cells = []
                is_header = (r_idx == 1 or r_idx == 6)
                cell_tag = "th" if is_header else "td"

                first_cell_val = ws.cell(row=r_idx, column=1).value
                item_id = f"item_{r_idx}" if (is_calculator_sheet and isinstance(first_cell_val, (int, str)) and str(first_cell_val).isdigit()) else None

                for c_idx in range(1, min(max_c + 1, 10)):
                    val = ws.cell(row=r_idx, column=c_idx).value
                    val_str = "" if val is None else str(val)

                    if is_calculator_sheet and item_id and not is_header:
                        if c_idx == 7:
                            checked = "checked" if val_str.lower() in {"yes", "true", "1"} else ""
                            row_cells.append(f'<{cell_tag} style="text-align: center;"><input type="checkbox" class="item-check" {checked}></{cell_tag}>')
                            continue
                        elif c_idx == 4 and val_str.isdigit():
                            row_cells.append(f'<{cell_tag}><input type="number" class="item-cost form-control" value="{val_str}"></{cell_tag}>')
                            continue
                        elif c_idx == 5 and val_str.isdigit():
                            row_cells.append(f'<{cell_tag}><input type="number" class="item-qty form-control" value="{val_str}"></{cell_tag}>')
                            continue
                        elif c_idx == 6:
                            row_cells.append(f'<{cell_tag}><span class="item-row-total">₹{val_str}</span></{cell_tag}>')
                            continue

                    row_cells.append(f'<{cell_tag}>{html.escape(val_str)}</{cell_tag}>')

                tr_attr = f'data-item-id="{item_id}"' if item_id else ''
                table_rows.append(f'<tr {tr_attr}>{"".join(row_cells)}</tr>')

            calc_class = "interactive-calc-table" if is_calculator_sheet else ""

            pane_html = f'''
            <div id="{sheet_id}" class="sheet-pane {is_active}">
              <div class="table-responsive">
                <table class="doc-table {calc_class}">
                  <tbody>
                    {"".join(table_rows)}
                  </tbody>
                </table>
              </div>
            </div>
            '''
            tab_panes.append(pane_html)

        summary_widget_html = '''
        <div class="proposal-summary-grid" style="margin-top: 2rem;">
          <div class="summary-card">
            <h3>📊 Live Investment Calculation</h3>
            <div class="summary-row"><span>Base Items Subtotal:</span><strong id="summary-subtotal">₹0</strong></div>
            <div class="summary-row"><span>Adjusted (Platform + Complexity):</span><strong id="summary-adjusted">₹0</strong></div>
            <div class="summary-row"><span>Discount Amount:</span><strong id="summary-discount">-₹0</strong></div>
            <div class="summary-row"><span>Tax (GST 18%):</span><strong id="summary-gst">₹0</strong></div>
            <div class="summary-row grand-total"><span>Grand Total Investment:</span><strong id="summary-grandtotal">₹0</strong></div>
          </div>

          <div class="summary-card">
            <h3>💼 Payment Milestone Split</h3>
            <div class="milestone-item"><span>Phase 1: Advance / Kickoff (35%)</span><strong id="milestone-advance">₹0</strong></div>
            <div class="milestone-item"><span>Phase 2: Wireframes & Design (20%)</span><strong id="milestone-design">₹0</strong></div>
            <div class="milestone-item"><span>Phase 3: Core Feature Build (30%)</span><strong id="milestone-dev">₹0</strong></div>
            <div class="milestone-item"><span>Phase 4: Testing & Handover (15%)</span><strong id="milestone-handover">₹0</strong></div>
          </div>
        </div>
        '''

        full_html = f'''
        <div id="project-banner-container"></div>

        <div class="excel-viewer">
          <div class="sheet-tabs">
            {"".join(tab_buttons)}
          </div>
          <div class="sheet-panes">
            {"".join(tab_panes)}
          </div>
        </div>

        {summary_widget_html}
        '''

        excerpt = f"Interactive Pricing Calculator with {len(sheet_names)} sheet(s) and {total_rows:,} configurable line-items."

        return {
            "title": title,
            "html": full_html,
            "sidebar_toc": "",
            "progress_bar": "",
            "excerpt": excerpt,
            "word_count": total_rows,
            "meta_label": f"{len(sheet_names)} Sheet(s) • {total_rows:,} Rows",
            "read_time": "Interactive Tool"
        }

    except Exception as e:
        print(f"  [Warning] Excel parsing error for {file_path.name}: {e}")
        return {
            "title": title,
            "html": f'<div class="no-results">Unable to preview spreadsheet: {html.escape(str(e))}</div>',
            "sidebar_toc": "",
            "progress_bar": "",
            "excerpt": "Excel file data preview unavailable.",
            "word_count": 0,
            "meta_label": "Excel Sheet",
            "read_time": "N/A"
        }


# ─── Multi-Format Pre-Exporter Generators ────────────────────────────────

def generate_export_files(doc_data: dict, file_path: Path, slug: str):
    """Ensure DOCX, XLSX, and Original export files are generated/copied in docs/files."""
    file_rel_path = file_path.relative_to(ROOT_DIR)
    target_orig = FILES_DIR / file_rel_path
    target_orig.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, target_orig)

    ext = file_path.suffix.lower()
    
    docx_export_path = FILES_DIR / "exports" / f"{slug}.docx"
    docx_export_path.parent.mkdir(parents=True, exist_ok=True)
    
    if ext in {".docx", ".doc"}:
        shutil.copy2(file_path, docx_export_path)
    else:
        try:
            doc = docx.Document()
            doc.add_heading(doc_data["title"], level=1)
            doc.add_paragraph(f"Source: {file_rel_path}")
            doc.add_paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            doc.add_heading("Content Overview", level=2)
            doc.add_paragraph(doc_data["excerpt"])
            doc.save(docx_export_path)
        except Exception as e:
            print(f"  [Warning] Failed creating DOCX export for {slug}: {e}")

    xlsx_export_path = FILES_DIR / "exports" / f"{slug}.xlsx"
    xlsx_export_path.parent.mkdir(parents=True, exist_ok=True)
    
    if ext in {".xlsx", ".xls"}:
        shutil.copy2(file_path, xlsx_export_path)
    else:
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Document Summary"
            ws.append(["Title", "Source Path", "Word Count / Rows", "Excerpt"])
            ws.append([doc_data["title"], str(file_rel_path), doc_data["meta_label"], doc_data["excerpt"]])
            wb.save(xlsx_export_path)
        except Exception as e:
            print(f"  [Warning] Failed creating XLSX export for {slug}: {e}")

    return {
        "original_url": f"../files/{file_rel_path.as_posix()}",
        "docx_url": f"../files/exports/{slug}.docx",
        "xlsx_url": f"../files/exports/{slug}.xlsx"
    }


# ─── HTML Page Generator Templates ───────────────────────────────────────

def render_doc_card_html(doc: dict, is_page_dir: bool = False) -> str:
    """Render single glass document card HTML."""
    prefix = "" if is_page_dir else "pages/"
    topic_attr = " ".join(doc['topics'])
    return f'''
    <a href="{prefix}{doc['slug']}.html" class="doc-card" data-type="{doc['category']}" data-topics="{topic_attr}" data-title="{html.escape(doc['title'])}">
      <div class="card-header">
        <div class="card-title">{html.escape(doc['title'])}</div>
        <span class="badge {doc['badge_class']}">{doc['label']}</span>
      </div>
      <p class="card-excerpt">{html.escape(doc['excerpt'])}</p>
      <div class="card-footer">
        <div class="card-meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <span>{doc['meta_label']}</span>
        </div>
        <div class="view-link">
          Open Tool &rarr;
        </div>
      </div>
    </a>
    '''


def generate_index_html(documents: list) -> str:
    """Build home index dashboard page (docs/index.html) with Smart Assistant Wizard, AI Analyzer, and API Key Config."""

    # Combined full-stack documents get their own bucket
    combined_docs = [d for d in documents if 'combined' in d['topics']]
    non_combined = [d for d in documents if 'combined' not in d['topics']]

    calc_docs = [d for d in non_combined if d['category'] == 'xlsx']
    proposal_docs = [d for d in non_combined if d['category'] == 'docx' or 'pricing-parameters' in d['slug']]
    questionnaire_docs = [d for d in non_combined if 'questionnaire' in d['slug']]
    checklist_docs = [d for d in non_combined if 'checklist' in d['slug']]
    guide_docs = [d for d in non_combined if d not in calc_docs and d not in proposal_docs and d not in questionnaire_docs and d not in checklist_docs]

    combined_cards_html = "".join([render_doc_card_html(d) for d in combined_docs])
    calc_cards_html = "".join([render_doc_card_html(d) for d in calc_docs])
    proposal_cards_html = "".join([render_doc_card_html(d) for d in proposal_docs])
    quest_cards_html = "".join([render_doc_card_html(d) for d in questionnaire_docs])
    check_cards_html = "".join([render_doc_card_html(d) for d in checklist_docs])
    guide_cards_html = "".join([render_doc_card_html(d) for d in guide_docs])
    combined_count = len(combined_docs)

    md_count = sum(1 for d in documents if d['category'] == 'md')
    docx_count = sum(1 for d in documents if d['category'] == 'docx')
    xlsx_count = sum(1 for d in documents if d['category'] == 'xlsx')

    web_count = sum(1 for d in non_combined if 'web' in d['topics'])
    mobile_count = sum(1 for d in non_combined if 'mobile' in d['topics'])
    pricing_count = sum(1 for d in non_combined if 'pricing' in d['topics'])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Client Requirement Analysis — Scoping System</title>
  <meta name="description" content="Centralized Client Requirement Scoping, Pricing Calculators, and Proposal Management System.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/soria">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="glass-header">
      <a href="index.html" class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span class="brand-name">Client Requirement Hub</span>
          <span class="version-badge">PRO v2.4</span>
        </div>
      </a>
      <nav class="nav-links">
        <button id="header-api-key-btn" class="export-btn api-key-btn" onclick="window.SmartAssistant.openApiKeyModal()">🔑 DeepSeek Key</button>
        <a href="index.html" class="nav-pill active">🏠 Workspace</a>
        <a href="pages/file-explorer.html" class="nav-pill">📁 File Explorer</a>
        <a href="pages/interactive-proposal-builder.html" class="nav-pill">Proposal Builder</a>
        <a href="pages/ai-intelligence-engine.html" class="nav-pill ai-pill">🧠 AI Studio</a>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <h1>Client Requirement Scoping & Proposal Management System</h1>
      <p class="hero-subtitle">
        Scope software projects, evaluate pricing parameters, conduct discovery questionnaires, and generate client proposals.
      </p>
    </section>

    <!-- Structured Filter & Search Controls -->
    <div class="filter-bar">
      <div class="search-box">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" id="search-input" class="search-input" placeholder="Search primary tools by title or keyword..." aria-label="Search tools">
      </div>

      <div class="filter-controls-row">
        <div class="filter-group">
          <span class="filter-label">Category:</span>
          <div class="filter-tags">
            <button class="filter-btn topic-filter active" data-topic="all">All Topics</button>
            <button class="filter-btn topic-filter" data-topic="web">🌐 Web Projects ({web_count})</button>
            <button class="filter-btn topic-filter" data-topic="mobile">📱 Mobile Apps ({mobile_count})</button>
            <button class="filter-btn topic-filter" data-topic="pricing">💰 Pricing & Calculators ({pricing_count})</button>
            <button class="filter-btn topic-filter" data-topic="combined" style="background: linear-gradient(135deg, rgba(30,58,95,0.15), rgba(30,61,47,0.15)); border-color: #38bdf8; color: #38bdf8;">⚡ Full-Stack Combined ({combined_count})</button>
          </div>
        </div>

        <div class="filter-group">
          <span class="filter-label">Format:</span>
          <div class="filter-tags">
            <button class="filter-btn type-filter active" data-filter="all">All Formats (<span id="visible-count">{len(documents)}</span>)</button>
            <button class="filter-btn type-filter" data-filter="md">Markdown ({md_count})</button>
            <button class="filter-btn type-filter" data-filter="docx">Word ({docx_count})</button>
            <button class="filter-btn type-filter" data-filter="xlsx">Excel ({xlsx_count})</button>
          </div>
        </div>
      </div>
    </div>

    <!-- BUCKET: Full-Stack Combined Documents -->
    <section class="bucket-section combined-bucket">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: linear-gradient(135deg, rgba(30,58,95,0.15), rgba(30,61,47,0.15)); color: #38bdf8;">⚡</div>
        <div>
          <h2 class="bucket-title">Full-Stack Combined Documents <span style="font-size: 0.7rem; font-weight: 600; background: linear-gradient(135deg, #1e3a5f, #1e3d2f); color: #fff; padding: 2px 10px; border-radius: 99px; margin-left: 0.5rem; vertical-align: middle; letter-spacing: 0.08em;">WEB + APP</span></h2>
          <p class="bucket-desc">Unified documents combining both Website and Mobile Application content — ideal for full-stack client engagements requiring a single comprehensive resource.</p>
        </div>
      </div>
      <div class="card-grid">
        {combined_cards_html}
      </div>
    </section>

    <!-- BUCKET 1: Pricing Calculators Container Box -->
    <section class="bucket-section">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: rgba(16, 185, 129, 0.1); color: var(--accent-emerald);">📊</div>
        <div>
          <h2 class="bucket-title">Pricing Calculators</h2>
          <p class="bucket-desc">Spreadsheets with real-time tax computation, complexity multipliers, and payment milestone splits.</p>
        </div>
      </div>
      <div class="card-grid">
        {calc_cards_html}
      </div>
    </section>

    <!-- BUCKET 2: Proposal Parameters Container Box -->
    <section class="bucket-section">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: rgba(99, 102, 241, 0.1); color: var(--accent-indigo);">📄</div>
        <div>
          <h2 class="bucket-title">Proposal Parameters & Templates</h2>
          <p class="bucket-desc">Formal Word proposal templates and pricing parameter reference specifications.</p>
        </div>
      </div>
      <div class="card-grid">
        {proposal_cards_html}
      </div>
    </section>

    <!-- BUCKET 2: Client Questionnaires Container Box -->
    <section class="bucket-section">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: rgba(59, 130, 246, 0.1); color: var(--accent-primary);">📋</div>
        <div>
          <h2 class="bucket-title">Client Discovery Questionnaires</h2>
          <p class="bucket-desc">Interactive requirement gathering questionnaires to conduct structured discovery calls with clients.</p>
        </div>
      </div>
      <div class="card-grid">
        {quest_cards_html}
      </div>
    </section>

    <!-- BUCKET 3: Project Checklists Container Box -->
    <section class="bucket-section">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: rgba(99, 102, 241, 0.1); color: var(--accent-indigo);">✅</div>
        <div>
          <h2 class="bucket-title">Project Lifecycle Checklists</h2>
          <p class="bucket-desc">300+ interactive task checklists tracking pre-project kickoff, design, build, and handover tasks.</p>
        </div>
      </div>
      <div class="card-grid">
        {check_cards_html}
      </div>
    </section>

    <!-- BUCKET 4: Master Requirement Reference Guides Container Box -->
    <section class="bucket-section">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--accent-amber);">📖</div>
        <div>
          <h2 class="bucket-title">Master Requirement Reference Guides</h2>
          <p class="bucket-desc">Comprehensive reference guides with sticky table-of-contents and parameter scope selection tools.</p>
        </div>
      </div>
      <div class="card-grid">
        {guide_cards_html}
      </div>
    </section>

    <div id="no-results" class="no-results" style="display: none; text-align: center; padding: 3rem 1.5rem;">
      <h3>No matching tools found</h3>
      <p>Try refining your search terms or selecting a different file category filter.</p>
    </div>

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • Interactive Web App for GitHub Pages</p>
    </footer>
  </div>

  <script src="./assets/js/storage.js"></script>
  <script src="./assets/js/calculator.js"></script>
  <script src="./assets/js/proposal.js"></script>
  <script src="./assets/js/assistant.js"></script>
  <script src="./assets/js/main.js"></script>
  <script src="./assets/js/export.js"></script>
  <script>
    function handleWizardRecommend() {{
      const plat = document.getElementById('wizard-platform').value;
      const intent = document.getElementById('wizard-intent').value;
      const clientName = document.getElementById('wizard-client-name').value.trim();

      const rec = window.SmartAssistant.getRecommendation(plat, intent);
      const out = document.getElementById('wizard-recommend-output');

      if (clientName && window.ProjectStorage) {{
        const proj = window.ProjectStorage.getProject();
        proj.clientName = clientName;
        window.ProjectStorage.saveProject(proj);
      }}

      out.style.display = 'block';
      out.innerHTML = '<div style="background: rgba(16, 185, 129, 0.08); padding: 1rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3);">' +
        '<div style="font-weight: 700; color: var(--accent-emerald);">Recommended Tool: ' + rec.title + '</div>' +
        '<p style="font-size: 0.85rem; color: var(--text-muted); margin: 0.25rem 0 0.75rem 0;">' + rec.desc + '</p>' +
        '<a href="pages/' + rec.slug + '.html" class="export-btn primary" style="font-size: 0.82rem;">🚀 Open ' + rec.title + ' Now</a>' +
        '</div>';
    }}

    async function handleAiDocumentAnalyze() {{
      const fileInput = document.getElementById('ai-file-input');
      const clientTitle = document.getElementById('ai-client-title').value.trim();

      if (!fileInput.files || !fileInput.files[0]) {{
        alert("Please select a client requirement document file first.");
        return;
      }}

      await window.SmartAssistant.analyzeDocumentFile(fileInput.files[0], clientTitle, clientTitle);
    }}
  </script>
</body>
</html>
'''


def generate_file_explorer_page_html(all_documents: list) -> str:
    """Build dedicated File Explorer Catalog Page (docs/pages/file-explorer.html) with Soria Display Serif typography."""
    cards_html = "".join([render_doc_card_html(d, is_page_dir=True) for d in all_documents])
    
    md_count = sum(1 for d in all_documents if d['category'] == 'md')
    docx_count = sum(1 for d in all_documents if d['category'] == 'docx')
    xlsx_count = sum(1 for d in all_documents if d['category'] == 'xlsx')

    web_count = sum(1 for d in all_documents if 'web' in d['topics'])
    mobile_count = sum(1 for d in all_documents if 'mobile' in d['topics'])
    pricing_count = sum(1 for d in all_documents if 'pricing' in d['topics'])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Repository File Explorer — All 18 Documents</title>
  <meta name="description" content="Complete repository catalog containing all Markdown reference guides, Excel calculators, Word proposals, and checklists.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/soria">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="glass-header">
      <a href="../index.html" class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span class="brand-name">Client Requirement Hub</span>
          <span class="version-badge">FILE CATALOG</span>
        </div>
      </a>
      <nav class="nav-links">
        <button id="header-api-key-btn" class="export-btn api-key-btn" onclick="window.SmartAssistant.openApiKeyModal()">🔑 DeepSeek Key</button>
        <a href="../index.html" class="nav-pill">🏠 Workspace</a>
        <a href="file-explorer.html" class="nav-pill active">📁 File Explorer</a>
        <a href="interactive-proposal-builder.html" class="nav-pill">✨ Proposal Builder</a>
        <a href="ai-intelligence-engine.html" class="nav-pill ai-pill">🧠 AI Studio</a>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <h1>📁 Repository File Explorer & Reference Catalog</h1>
      <p class="hero-subtitle">
        Browse, search, and read all 18 repository files — including pricing parameter markdowns, quick guides, overview documents, questionnaires, spreadsheets, and proposal templates.
      </p>
    </section>

    <!-- Structured Filter & Search Controls -->
    <div class="filter-bar">
      <div class="search-box">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" id="search-input" class="search-input" placeholder="Search all 18 repository files..." aria-label="Search all files">
      </div>

      <div class="filter-controls-row">
        <div class="filter-group">
          <span class="filter-label">Category:</span>
          <div class="filter-tags">
            <button class="filter-btn topic-filter active" data-topic="all">All Topics ({len(all_documents)})</button>
            <button class="filter-btn topic-filter" data-topic="web">🌐 Web Projects ({web_count})</button>
            <button class="filter-btn topic-filter" data-topic="mobile">📱 Mobile Apps ({mobile_count})</button>
            <button class="filter-btn topic-filter" data-topic="pricing">💰 Pricing & References ({pricing_count})</button>
          </div>
        </div>

        <div class="filter-group">
          <span class="filter-label">Format:</span>
          <div class="filter-tags">
            <button class="filter-btn type-filter active" data-filter="all">All Formats (<span id="visible-count">{len(all_documents)}</span>)</button>
            <button class="filter-btn type-filter" data-filter="md">Markdown ({md_count})</button>
            <button class="filter-btn type-filter" data-filter="docx">Word ({docx_count})</button>
            <button class="filter-btn type-filter" data-filter="xlsx">Excel ({xlsx_count})</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Complete Repository Files Bucket Container Box -->
    <section class="bucket-section">
      <div class="bucket-header">
        <div class="bucket-icon" style="background: rgba(59, 130, 246, 0.1); color: var(--accent-primary);">📁</div>
        <div>
          <h2 class="bucket-title">All Repository Documents & Reference Files</h2>
          <p class="bucket-desc">Complete catalog of all 18 markdown documents, questionnaires, spreadsheets, and proposals in the repository.</p>
        </div>
      </div>
      <div class="card-grid" id="card-grid">
        {cards_html}
      </div>
    </section>

    <div id="no-results" class="no-results" style="display: none; text-align: center; padding: 3rem 1.5rem;">
      <h3>No matching files found</h3>
      <p>Try refining your search terms or selecting a different file category filter.</p>
    </div>

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • Repository File Catalog</p>
    </footer>
  </div>

  <script src="../assets/js/storage.js"></script>
  <script src="../assets/js/calculator.js"></script>
  <script src="../assets/js/proposal.js"></script>
  <script src="../assets/js/assistant.js"></script>
  <script src="../assets/js/main.js"></script>
  <script src="../assets/js/export.js"></script>
</body>
</html>
'''


def render_export_toolbar_html(doc: dict) -> str:
    category = doc['category'] # 'md', 'xlsx', 'docx'
    filename = doc['filename']
    slug = doc['slug']
    original_url = doc['original_url']

    buttons = []

    if category == 'xlsx':
        # Excel Calculator Page - Only show relevant Excel/PDF downloads
        buttons.append(f'''
        <button class="export-btn primary" onclick="ExportManager.downloadFile('{original_url}', '{filename}')">
          <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
          Download Excel Spreadsheet ({filename})
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.exportXLSX('{original_url}', '{slug}.csv')">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
          Export Table Data (.csv)
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.exportPDF()">
          <svg viewBox="0 0 24 24"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>
          Print / Save PDF Summary
        </button>
        ''')

    elif category == 'docx':
        # Word Proposal Page - Only show relevant Word/PDF downloads
        buttons.append(f'''
        <button class="export-btn primary" onclick="ExportManager.downloadFile('{original_url}', '{filename}')">
          <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
          Download Word Document ({filename})
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.exportDOCX('{original_url}', '{slug}.doc')">
          <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
          Export Customized Word (.doc)
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.exportPDF()">
          <svg viewBox="0 0 24 24"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>
          Export as PDF
        </button>
        ''')

    else:
        # Markdown Document Page - PDF, Word, Copy, and Download Original
        buttons.append(f'''
        <button class="export-btn primary" onclick="ExportManager.exportPDF()">
          <svg viewBox="0 0 24 24"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>
          Export as PDF
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.exportDOCX(null, '{slug}.doc')">
          <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
          Export as Word (.doc)
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.copyContentToClipboard()">
          <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
          Copy Content
        </button>
        ''')
        buttons.append(f'''
        <button class="export-btn" onclick="ExportManager.downloadFile('{original_url}', '{filename}')">
          <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
          Download Original ({filename})
        </button>
        ''')

    return '<div class="export-toolbar">' + ''.join(buttons) + '</div>'


def generate_doc_page_html(doc: dict) -> str:
    """Build individual document view page (docs/pages/<slug>.html)."""
    layout_wrapper_start = '<div class="doc-layout-grid">' if doc.get('sidebar_toc') else '<div>'
    layout_wrapper_end = '</div>'
    export_toolbar_html = render_export_toolbar_html(doc)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(doc['title'])} — Requirement Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/soria">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header & Breadcrumb Navigation -->
    <header class="glass-header">
      <a href="../index.html" class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span class="brand-name">Client Requirement Hub</span>
          <span class="version-badge">DOC VIEW</span>
        </div>
      </a>
      <nav class="nav-links">
        <button id="header-api-key-btn" class="export-btn api-key-btn" onclick="window.SmartAssistant.openApiKeyModal()">🔑 DeepSeek Key</button>
        <a href="../index.html" class="nav-pill">🏠 Workspace</a>
        <a href="file-explorer.html" class="nav-pill">📁 File Explorer</a>
        <a href="interactive-proposal-builder.html" class="nav-pill">Proposal Builder</a>
        <a href="ai-intelligence-engine.html" class="nav-pill ai-pill">🧠 AI Studio</a>
      </nav>
    </header>

    <!-- Document Header Info Card -->
    <section class="doc-header-card">
      <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
        <span class="badge {doc['badge_class']}">{doc['label']}</span>
        <span style="font-size: 0.85rem; color: var(--text-subtle);">{doc['relative_path']}</span>
      </div>
      <h1>{html.escape(doc['title'])}</h1>

      <div class="doc-meta-row">
        <span>File Size: {doc['formatted_size']}</span>
        <span>Metrics: {doc['meta_label']}</span>
        <span>Reading Time: {doc['read_time']}</span>
        <span>Last Modified: {doc['last_modified']}</span>
      </div>

      <!-- Dynamic Format-Specific Export & Download Action Bar -->
      {export_toolbar_html}
    </section>

    <!-- 2-Column Content Layout (TOC Sidebar + Main Content) -->
    {layout_wrapper_start}
      {doc.get('sidebar_toc', '')}

      <main class="doc-main-content">
        <div class="doc-content-card">
          {doc.get('progress_bar', '')}
          <div class="rendered-markdown">
            {doc['rendered_html']}
          </div>
        </div>
      </main>
    {layout_wrapper_end}

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • Interactive Web App</p>
    </footer>
  </div>

  <script src="../assets/js/storage.js"></script>
  <script src="../assets/js/calculator.js"></script>
  <script src="../assets/js/proposal.js"></script>
  <script src="../assets/js/assistant.js"></script>
  <script src="../assets/js/ai-engine.js"></script>
  <script src="../assets/js/main.js"></script>
  <script src="../assets/js/export.js"></script>
</body>
</html>
'''


def generate_proposal_builder_tool_html() -> str:
    """Generate dedicated interactive proposal builder tool page (docs/pages/interactive-proposal-builder.html)."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Custom Client Proposal Builder — Requirement Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/soria">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="glass-header">
      <a href="../index.html" class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span class="brand-name">Client Requirement Hub</span>
          <span class="version-badge">PROPOSAL SCOPER</span>
        </div>
      </a>
      <nav class="nav-links">
        <button id="header-api-key-btn" class="export-btn api-key-btn" onclick="window.SmartAssistant.openApiKeyModal()">🔑 DeepSeek Key</button>
        <a href="../index.html" class="nav-pill">🏠 Workspace</a>
        <a href="file-explorer.html" class="nav-pill">📁 File Explorer</a>
        <a href="interactive-proposal-builder.html" class="nav-pill active">✨ Proposal Builder</a>
        <a href="ai-intelligence-engine.html" class="nav-pill ai-pill">🧠 AI Studio</a>
      </nav>
    </header>

    <!-- Interactive Client Banner -->
    <div id="project-banner-container"></div>

    <!-- Proposal Actions Bar -->
    <div class="glass-header" style="margin-bottom: 1.5rem;">
      <div style="font-weight: 800; font-size: 1.1rem; color: #ffffff; display: flex; align-items: center; gap: 0.5rem;">
        <span>⚡ Proposal Actions</span>
      </div>
      <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
        <button class="nav-pill ai-pill" onclick="ProposalGenerator.openHowItWorksModal()">❓ How It Works & Data Sources</button>
        <button class="nav-pill active" style="background: linear-gradient(135deg, #10b981, #059669); border-color: #10b981; color: #ffffff; font-weight: 700;" onclick="ExportManager.exportPDF()">📄 Download PDF Proposal</button>
        <button class="nav-pill" style="color: #ffffff;" onclick="ProjectStorage.exportJSON()">💾 Export Project JSON</button>
        <label class="nav-pill" style="color: #ffffff; cursor: pointer;">
          📂 Import Project JSON
          <input type="file" accept=".json" style="display: none;" onchange="handleImportFile(event)">
        </label>
      </div>
    </div>

    <!-- Rendered Proposal Document Output -->
    <main class="doc-content-card" id="proposal-output-container">
      <!-- Generated via proposal.js -->
    </main>

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • Powered by Interactive Static Web App</p>
    </footer>
  </div>

  <script src="../assets/js/storage.js"></script>
  <script src="../assets/js/calculator.js"></script>
  <script src="../assets/js/proposal.js"></script>
  <script src="../assets/js/assistant.js"></script>
  <script src="../assets/js/ai-engine.js"></script>
  <script src="../assets/js/main.js"></script>
  <script src="../assets/js/export.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      ProposalGenerator.renderProposal('proposal-output-container');
    }});

    function handleImportFile(evt) {{
      const file = evt.target.files[0];
      if (file) {{
        const reader = new FileReader();
        reader.onload = function(e) {{
          ProjectStorage.importJSON(e.target.result);
        }};
        reader.readAsText(file);
      }}
    }}
  </script>
</body>
</html>
'''


def generate_ai_intelligence_engine_html() -> str:
    """Generate dedicated AI Requirement Intelligence Engine page (docs/pages/ai-intelligence-engine.html)."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Requirement Intelligence Engine — DeepSeek Technical Document Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/soria">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="glass-header">
      <a href="../index.html" class="brand-title">
        <div class="brand-icon" style="background: linear-gradient(135deg, var(--accent-indigo), #ec4899); color: #fff;">🧠</div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span class="brand-name">AI Technical Intelligence Studio</span>
          <span class="version-badge">DEEP AI</span>
        </div>
      </a>
      <nav class="nav-links">
        <button id="header-api-key-btn" class="export-btn api-key-btn" onclick="window.SmartAssistant.openApiKeyModal()">🔑 DeepSeek Key</button>
        <a href="../index.html" class="nav-pill">🏠 Workspace</a>
        <a href="file-explorer.html" class="nav-pill">📁 File Explorer</a>
        <a href="interactive-proposal-builder.html" class="nav-pill">✨ Proposal Builder</a>
        <a href="ai-intelligence-engine.html" class="nav-pill ai-pill active">🧠 AI Studio</a>
      </nav>
    </header>

    <!-- Interactive Client Banner -->
    <div id="project-banner-container"></div>

    <!-- AI Studio Hero Header -->
    <section class="doc-header-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(59, 130, 246, 0.04)); border: 1px solid rgba(99, 102, 241, 0.3);">
      <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
        <span class="badge badge-md" style="background: var(--accent-indigo); color: #fff;">DEEPSEEK AI STUDIO</span>
        <span style="font-size: 0.85rem; color: var(--text-subtle);">Automated Technical Architecture & Document Generator</span>
      </div>
      <h1 style="font-family: var(--font-serif); font-size: 2.2rem; color: var(--text-main);">AI Requirement Intelligence Studio</h1>
      <p style="color: var(--text-muted); font-size: 1rem; max-width: 800px; margin-top: 0.5rem; line-height: 1.6;">
        Upload a client requirement document (PDF, DOCX, TXT), answer clarifying technical intake questions, and let DeepSeek AI generate complete technical architecture specifications, deployment guides, SEO reports, tech stack analyses, and REST API contracts automatically!
      </p>
    </section>

    <!-- Step 1 & 2: Interactive Intake Wizard Form -->
    <main class="doc-content-card" style="margin-bottom: 2rem;">
      <h2 style="font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
        <span>📋 Step 1: Technical Requirement Intake Wizard</span>
      </h2>

      <div class="form-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
        <div class="form-group">
          <label>Target Project Platform:</label>
          <select id="ai-wizard-platform" class="form-control" onchange="toggleWizardFields(this.value)">
            <option value="Website">🌐 Website / Web Application</option>
            <option value="Mobile">📱 Mobile Application (iOS/Android)</option>
            <option value="Both">⚡ Full-Stack Web & Mobile Solution</option>
          </select>
        </div>

        <div class="form-group">
          <label>Target Industry / Business Domain:</label>
          <input type="text" id="ai-wizard-industry" class="form-control" placeholder="e.g. E-Commerce, SaaS, Healthcare, Fintech">
        </div>

        <div class="form-group" id="group-seo">
          <label>SEO & Marketing Growth Priority:</label>
          <select id="ai-wizard-seo" class="form-control">
            <option value="High (Local & National SEO + Schema.org + OpenGraph)">🚀 High (Local/National SEO + Schema.org)</option>
            <option value="Medium (Standard On-Page Meta & Sitemap)">Standard Meta Tags & Sitemap</option>
            <option value="Internal Tool (No SEO Needed)">Internal Platform (No Public SEO)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Cloud Infrastructure & Hosting Preference:</label>
          <select id="ai-wizard-hosting" class="form-control">
            <option value="AWS Cloud Container Stack">AWS (ECS / RDS / S3)</option>
            <option value="Vercel + Managed Postgres">Vercel / Netlify + Supabase</option>
            <option value="DigitalOcean App Platform">DigitalOcean App Platform</option>
            <option value="Google Cloud Platform (GCP)">Google Cloud Platform (GCP)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Expected Traffic / Active User Scale:</label>
          <select id="ai-wizard-traffic" class="form-control">
            <option value="10,000+ monthly active users">10,000+ monthly active users</option>
            <option value="100,000+ monthly active users">100,000+ high concurrency users</option>
            <option value="Startup Initial Launch (<5k users)">Startup Launch (<5,000 users)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Delivery Timeline Urgency:</label>
          <select id="ai-wizard-timeline" class="form-control">
            <option value="Standard Sprint Delivery (4–8 Weeks)">Standard Sprint Delivery (4–8 Weeks)</option>
            <option value="Fast-Track MVP (2–4 Weeks)">Fast-Track MVP (2–4 Weeks)</option>
            <option value="Enterprise Multi-Phase Roadmap">Enterprise Multi-Phase Roadmap</option>
          </select>
        </div>
      </div>
    </main>

    <!-- Step 3: Document Upload Area -->
    <main class="doc-content-card" style="margin-bottom: 2rem;">
      <h2 style="font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 1.25rem;">
        📄 Step 2: Upload Client Requirement File
      </h2>

      <div style="border: 2px dashed var(--accent-indigo); padding: 2rem; border-radius: 12px; text-align: center; background: rgba(99, 102, 241, 0.03);">
        <input type="file" id="ai-doc-file" accept=".pdf,.docx,.txt,.md" style="display: none;" onchange="updateFileLabel(this)">
        <button class="export-btn primary" onclick="document.getElementById('ai-doc-file').click()" style="padding: 0.75rem 1.5rem; font-size: 1rem; margin-bottom: 0.75rem;">
          📁 Choose File (PDF, DOCX, TXT, MD)
        </button>
        <div id="ai-file-name-label" style="font-weight: 600; color: var(--text-subtle);">No file chosen yet. (Optional — AI can build documents using intake parameters alone!)</div>
      </div>
    </main>

    <!-- Step 4: Deliverables Generator Selector -->
    <main class="doc-content-card" style="margin-bottom: 2rem;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 0.75rem;">
        <h2 style="font-family: var(--font-serif); font-size: 1.5rem; margin: 0;">
          🛠️ Step 3: Select Technical Documents for AI to Generate
        </h2>
        <div style="display: flex; gap: 0.5rem;">
          <button class="export-btn" onclick="selectAllDocTypes(true)">Check All (10 Docs)</button>
          <button class="export-btn" onclick="selectAllDocTypes(false)">Clear Selection</button>
        </div>
      </div>

      <div class="card-grid" style="grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem;" id="ai-doc-type-grid">
        <!-- Rendered via JS script below -->
      </div>

      <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end;">
        <button class="export-btn primary" style="padding: 0.85rem 2rem; font-size: 1.1rem; background: linear-gradient(135deg, var(--accent-indigo), var(--accent-primary)); border: none; box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);" onclick="startAiGenerationPipeline()">
          🚀 Generate Selected AI Documents & Auto-Fill Workspace
        </button>
      </div>
    </main>

    <!-- Step 5: Live Generation Dashboard Overlay / Container -->
    <div id="ai-progress-container" class="doc-content-card" style="display: none; margin-bottom: 2rem; background: rgba(99, 102, 241, 0.05); border: 1px solid var(--accent-indigo);">
      <h3 style="font-size: 1.2rem; color: var(--accent-indigo); margin-bottom: 0.75rem;">⚡ AI Document Generation Pipeline Running...</h3>
      <div id="ai-progress-status" style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.75rem;">Preparing pipeline...</div>
      <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-bottom: 1rem;">
        <div id="ai-progress-bar-inner" style="height: 100%; width: 0%; background: var(--accent-indigo); transition: width 0.4s ease;"></div>
      </div>
    </div>

    <!-- Output Deliverables Cards Container -->
    <div id="ai-results-container"></div>

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • AI Technical Intelligence Studio</p>
    </footer>
  </div>

  <script src="../assets/js/storage.js"></script>
  <script src="../assets/js/calculator.js"></script>
  <script src="../assets/js/proposal.js"></script>
  <script src="../assets/js/assistant.js"></script>
  <script src="../assets/js/ai-engine.js"></script>
  <script src="../assets/js/main.js"></script>
  <script src="../assets/js/export.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      renderDocTypeSelectionGrid();
    }});

    function toggleWizardFields(val) {{
      const seoGroup = document.getElementById('group-seo');
      if (seoGroup) {{
        seoGroup.style.display = (val === 'Mobile') ? 'none' : 'block';
      }}
    }}

    function updateFileLabel(input) {{
      const lbl = document.getElementById('ai-file-name-label');
      if (input.files && input.files[0]) {{
        lbl.textContent = `📄 Selected File: ${{input.files[0].name}} (${{(input.files[0].size / 1024).toFixed(1)}} KB)`;
        lbl.style.color = 'var(--accent-emerald)';
      }}
    }}

    function renderDocTypeSelectionGrid() {{
      const grid = document.getElementById('ai-doc-type-grid');
      if (!grid || !window.AIEngine) return;

      let html = '';
      Object.keys(window.AIEngine.docTypes).forEach(id => {{
        const d = window.AIEngine.docTypes[id];
        html += `
          <div style="background: #ffffff; padding: 1.25rem; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">${{d.icon}}</span>
                <input type="checkbox" class="ai-doc-checkbox" data-doc-id="${{d.id}}" checked style="width: 18px; height: 18px; cursor: pointer;">
              </div>
              <div style="font-weight: 700; font-size: 1rem; color: var(--text-main); margin-bottom: 0.25rem;">${{d.title}}</div>
              <span class="badge badge-md" style="margin-bottom: 0.5rem; font-size: 0.7rem;">${{d.category}}</span>
              <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5;">${{d.desc}}</p>
            </div>
          </div>
        `;
      }});
      grid.innerHTML = html;
    }}

    function selectAllDocTypes(check) {{
      document.querySelectorAll('.ai-doc-checkbox').forEach(cb => cb.checked = check);
    }}

    async function startAiGenerationPipeline() {{
      const selected = [];
      document.querySelectorAll('.ai-doc-checkbox:checked').forEach(cb => {{
        selected.push(cb.getAttribute('data-doc-id'));
      }});

      if (!selected.length) {{
        alert("Please select at least one technical document to generate.");
        return;
      }}

      const fileInput = document.getElementById('ai-doc-file');
      let docText = "";

      if (fileInput.files && fileInput.files[0]) {{
        if (window.showToast) window.showToast("Extracting document text...", "info");
        docText = await window.AIEngine.extractTextFromPDF(fileInput.files[0]);
      }}

      const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : {{}};

      const context = {{
        clientName: proj.clientName || 'Client',
        projectName: proj.projectName || 'Project',
        projectType: document.getElementById('ai-wizard-platform').value,
        docText: docText,
        answers: {{
          industry: document.getElementById('ai-wizard-industry').value,
          seoPriority: document.getElementById('ai-wizard-seo')?.value || 'Standard',
          hostingPreference: document.getElementById('ai-wizard-hosting').value,
          trafficScale: document.getElementById('ai-wizard-traffic').value,
          timeline: document.getElementById('ai-wizard-timeline').value
        }}
      }};

      const progressContainer = document.getElementById('ai-progress-container');
      const progressStatus = document.getElementById('ai-progress-status');
      const progressBar = document.getElementById('ai-progress-bar-inner');
      const resultsContainer = document.getElementById('ai-results-container');

      progressContainer.style.display = 'block';

      const results = await window.AIEngine.generateAllSelected(selected, context, (current, total, title) => {{
        const pct = Math.round((current / total) * 100);
        progressBar.style.width = `${{pct}}%`;
        progressStatus.textContent = `Generating (${{current}} of ${{total}}): ${{title}}...`;
      }});

      progressContainer.style.display = 'none';

      // Render Deliverables Summary Cards
      let resultsHtml = `<main class="doc-content-card"><h2 style="font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 1.25rem;">✨ Generated Technical Deliverables</h2><div style="display: flex; gap: 0.75rem; margin-bottom: 1.5rem;"><button class="export-btn primary" onclick="downloadAllAiDeliverables()">📦 Download All AI Deliverables</button></div><div style="display: grid; gap: 1.5rem;">`;

      results.forEach(doc => {{
        resultsHtml += `
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
              <h3 style="font-size: 1.2rem; color: var(--text-main); margin: 0;">${{doc.icon}} ${{doc.title}}</h3>
              <a href="${{doc.targetSlug}}.html" class="export-btn" style="font-size: 0.8rem;">🚀 Open Auto-Filled Page</a>
            </div>
            <pre style="background: #ffffff; padding: 1rem; border-radius: 8px; border: 1px solid #cbd5e1; max-height: 250px; overflow-y: auto; font-size: 0.85rem; line-height: 1.5;">${{escapeHtml(doc.markdown)}}</pre>
          </div>
        `;
      }});

      resultsHtml += `</div></main>`;
      resultsContainer.innerHTML = resultsHtml;

      if (window.showToast) window.showToast(`Generated ${{results.length}} technical documents and auto-filled workspace pages!`, "success");
    }}

    function downloadAllAiDeliverables() {{
      const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
      if (!proj || !proj.aiGeneratedDocs) {{
        alert("No AI deliverables generated yet.");
        return;
      }}

      let fullContent = `# AI Technical Deliverables Package\nClient: ${{proj.clientName}}\n\n`;
      Object.keys(proj.aiGeneratedDocs).forEach(id => {{
        const doc = proj.aiGeneratedDocs[id];
        fullContent += `\n\n================================================\n# ${{doc.title}}\n================================================\n\n${{doc.markdown}}\n`;
      }});

      const blob = new Blob([fullContent], {{ type: 'text/markdown' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `AI_Deliverables_${{proj.clientName.replace(/[^a-z0-9]+/gi, '_')}}.md`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }}

    function escapeHtml(str) {{
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }}
  </script>
</body>
</html>
'''


# ─── Main Build Execution ────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("[BUILD] Building Interactive Site with Client-Provided API Key Manager")
    print("=" * 60)

    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    discovered_files = []

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        rel_root = Path(root).relative_to(ROOT_DIR)
        if rel_root.parts and rel_root.parts[0] == "docs":
            if len(rel_root.parts) > 1 and rel_root.parts[1] in {"pages", "files", "assets"}:
                continue

        for filename in files:
            file_path = Path(root) / filename
            ext = file_path.suffix.lower()

            if ext in SUPPORTED_EXTENSIONS and not filename.startswith("."):
                if "docs" in file_path.parts and ("pages" in file_path.parts or "files" in file_path.parts):
                    continue
                discovered_files.append(file_path)

    # Also discover combined/ folder explicitly (in case not picked up above)
    combined_dir = ROOT_DIR / "combined"
    if combined_dir.exists():
        for file_path in combined_dir.iterdir():
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS and not file_path.name.startswith("."):
                if file_path not in discovered_files:
                    discovered_files.append(file_path)

    discovered_files.sort(key=lambda p: str(p).lower())
    print(f"\n[DISCOVERY] Found {len(discovered_files)} total document(s) in repository:\n")

    all_processed_docs = []
    landing_docs = []

    for file_path in discovered_files:
        rel_path = file_path.relative_to(ROOT_DIR)
        ext = file_path.suffix.lower()
        type_info = get_file_type_info(ext)
        topics = get_document_topics(file_path)
        slug = slugify(str(rel_path.with_suffix('')))
        
        stat = file_path.stat()
        file_size = stat.st_size
        last_mod = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%b %d, %Y')

        print(f"  [CONVERT] Processing [{type_info['label']}] ({','.join(topics)}) {rel_path} ...")

        if ext == ".md":
            parsed = parse_markdown_file(file_path)
        elif ext in {".docx", ".doc"}:
            parsed = parse_docx_file(file_path)
        elif ext in {".xlsx", ".xls"}:
            parsed = parse_excel_file(file_path)
        else:
            parsed = {
                "title": file_path.stem,
                "html": f"<p>Preview not available for {ext}</p>",
                "sidebar_toc": "",
                "progress_bar": "",
                "excerpt": f"Document file ({ext})",
                "word_count": 0,
                "meta_label": ext.upper(),
                "read_time": "N/A"
            }

        doc_data = {
            "slug": slug,
            "filename": file_path.name,
            "title": parsed["title"],
            "category": type_info["category"],
            "topics": topics,
            "label": type_info["label"],
            "badge_class": type_info["badge_class"],
            "excerpt": parsed["excerpt"],
            "rendered_html": parsed["html"],
            "sidebar_toc": parsed.get("sidebar_toc", ""),
            "progress_bar": parsed.get("progress_bar", ""),
            "meta_label": parsed["meta_label"],
            "read_time": parsed["read_time"],
            "file_size": file_size,
            "formatted_size": format_bytes(file_size),
            "last_modified": last_mod,
            "relative_path": str(rel_path)
        }

        export_urls = generate_export_files(doc_data, file_path, slug)
        doc_data.update(export_urls)

        doc_page_html = generate_doc_page_html(doc_data)
        doc_page_path = PAGES_DIR / f"{slug}.html"
        doc_page_path.write_text(doc_page_html, encoding="utf-8")

        all_processed_docs.append(doc_data)

        if file_path.name not in LANDING_EXCLUDE_FILENAMES:
            landing_docs.append(doc_data)

    file_explorer_html = generate_file_explorer_page_html(all_processed_docs)
    (PAGES_DIR / "file-explorer.html").write_text(file_explorer_html, encoding="utf-8")

    proposal_tool_html = generate_proposal_builder_tool_html()
    (PAGES_DIR / "interactive-proposal-builder.html").write_text(proposal_tool_html, encoding="utf-8")

    ai_studio_html = generate_ai_intelligence_engine_html()
    (PAGES_DIR / "ai-intelligence-engine.html").write_text(ai_studio_html, encoding="utf-8")

    index_html = generate_index_html(landing_docs)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Client-Provided API Key Manager Site Successfully Built!")
    print(f"[OUTPUT] Directory: {OUTPUT_DIR}")
    print(f"[INDEX] Main Index: {OUTPUT_DIR / 'index.html'}")
    print(f"[EXPLORER] File Explorer Page: {PAGES_DIR / 'file-explorer.html'} ({len(all_processed_docs)} total files)")
    print(f"[TOOL] Proposal Builder: {PAGES_DIR / 'interactive-proposal-builder.html'}")
    print(f"[STUDIO] AI Intelligence Studio: {PAGES_DIR / 'ai-intelligence-engine.html'}")
    print(f"[PAGES] Generated {len(all_processed_docs)} total document pages in {PAGES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
