#!/usr/bin/env python3
"""
Document Hub & Interactive Static Site Generator
Scans repository for .md, .xlsx, .xls, .doc, and .docx files, converts them into web pages,
embeds interactive client workspace engines, and builds a static web hub in `docs/` for GitHub Pages.

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
    """Classify document by domain topic (web, mobile, pricing)."""
    rel_str = str(file_path).lower()
    topics = []
    
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
    """Convert Markdown file to HTML with interactive checkboxes for checklists."""
    content = file_path.read_text(encoding="utf-8", errors="replace")
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem.replace('-', ' ').replace('_', ' ').title()

    cb_count = 0
    def replace_task_cb(match):
        nonlocal cb_count
        checked = 'checked' if match.group(1).lower() == 'x' else ''
        cb_html = f'<input type="checkbox" class="interactive-checklist-item" data-cb-id="cb-{cb_count}" {checked}>'
        cb_count += 1
        return cb_html

    processed_content = re.sub(r'\[([ xX])\]', replace_task_cb, content)

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'attr_list', 'nl2br'])
    rendered_html = md.convert(processed_content)

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
        "html": f'<div class="rendered-markdown">{progress_bar_html}{rendered_html}</div>',
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

def generate_index_html(documents: list) -> str:
    """Build home index dashboard page (docs/index.html) with Web, Mobile, Pricing & File-type filters."""
    cards_html = []
    
    md_count = sum(1 for d in documents if d['category'] == 'md')
    docx_count = sum(1 for d in documents if d['category'] == 'docx')
    xlsx_count = sum(1 for d in documents if d['category'] == 'xlsx')

    web_count = sum(1 for d in documents if 'web' in d['topics'])
    mobile_count = sum(1 for d in documents if 'mobile' in d['topics'])
    pricing_count = sum(1 for d in documents if 'pricing' in d['topics'])

    for doc in documents:
        topic_attr = " ".join(doc['topics'])
        cards_html.append(f'''
        <a href="pages/{doc['slug']}.html" class="doc-card" data-type="{doc['category']}" data-topics="{topic_attr}" data-title="{html.escape(doc['title'])}">
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
              Open Document &rarr;
            </div>
          </div>
        </a>
        ''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Client Requirement Analysis — Interactive Workspace</title>
  <meta name="description" content="Centralized Interactive Workspace for Client Requirements, Pricing Calculators, and Proposals.">
  <link rel="stylesheet" href="./assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="glass-header">
      <div class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <span>Client Requirement Hub</span>
      </div>
      <nav class="nav-links">
        <a href="pages/interactive-proposal-builder.html" class="export-btn primary">✨ Proposal Builder</a>
        <span class="breadcrumb">
          <span style="font-weight: 600; color: var(--text-main);">{len(documents)} Total Documents</span>
        </span>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <h1>Interactive Requirement Workspace & Proposal Generator</h1>
      <p class="hero-subtitle">
        Scope projects, edit live pricing calculators, fill client questionnaires, auto-save state in browser, and export professional proposals.
      </p>
    </section>

    <!-- Filter & Search Controls -->
    <div class="filter-bar">
      <div class="search-box">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" id="search-input" class="search-input" placeholder="Search documents by title or keyword..." aria-label="Search documents">
      </div>

      <!-- Domain / Topic Filters -->
      <div class="filter-tags" style="width: 100%; margin-top: 0.5rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-subtle); display: flex; align-items: center; margin-right: 0.5rem;">CATEGORY:</span>
        <button class="filter-btn topic-filter active" data-topic="all">All Topics</button>
        <button class="filter-btn topic-filter" data-topic="web">🌐 Web Projects ({web_count})</button>
        <button class="filter-btn topic-filter" data-topic="mobile">📱 Mobile Apps ({mobile_count})</button>
        <button class="filter-btn topic-filter" data-topic="pricing">💰 Pricing & Calculators ({pricing_count})</button>
      </div>

      <!-- File Extension Filters -->
      <div class="filter-tags" style="width: 100%; margin-top: 0.25rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-subtle); display: flex; align-items: center; margin-right: 0.5rem;">FORMAT:</span>
        <button class="filter-btn type-filter active" data-filter="all">All Formats (<span id="visible-count">{len(documents)}</span>)</button>
        <button class="filter-btn type-filter" data-filter="md">Markdown ({md_count})</button>
        <button class="filter-btn type-filter" data-filter="docx">Word ({docx_count})</button>
        <button class="filter-btn type-filter" data-filter="xlsx">Excel ({xlsx_count})</button>
      </div>
    </div>

    <!-- Document Card Grid -->
    <main class="card-grid" id="card-grid">
      {"".join(cards_html)}
      <div id="no-results" class="no-results" style="display: none;">
        <h3>No matching documents found</h3>
        <p>Try refining your search terms or selecting a different file category filter.</p>
      </div>
    </main>

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • Interactive Web App for GitHub Pages</p>
    </footer>
  </div>

  <script src="./assets/js/storage.js"></script>
  <script src="./assets/js/calculator.js"></script>
  <script src="./assets/js/proposal.js"></script>
  <script src="./assets/js/main.js"></script>
  <script src="./assets/js/export.js"></script>
</body>
</html>
'''


def generate_doc_page_html(doc: dict) -> str:
    """Build individual document view page (docs/pages/<slug>.html)."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(doc['title'])} — Requirement Hub</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header & Breadcrumb Navigation -->
    <header class="glass-header">
      <div class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <span>Requirement Hub</span>
      </div>
      <nav class="nav-links">
        <a href="interactive-proposal-builder.html" class="export-btn primary">✨ Proposal Builder</a>
        <div class="breadcrumb">
          <a href="../index.html">Home</a>
          <span class="breadcrumb-sep">&rsaquo;</span>
          <span style="font-weight: 600; color: var(--text-main);">{html.escape(doc['title'])}</span>
        </div>
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

      <!-- Export & Download Action Bar -->
      <div class="export-toolbar">
        <button class="export-btn primary" onclick="ExportManager.exportPDF()">
          <svg viewBox="0 0 24 24"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>
          Export as PDF
        </button>

        <button class="export-btn" onclick="ExportManager.exportDOCX('{doc['docx_url']}', '{doc['slug']}.docx')">
          <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
          Export as Word (.docx)
        </button>

        <button class="export-btn" onclick="ExportManager.exportXLSX('{doc['xlsx_url']}', '{doc['slug']}.xlsx')">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
          Export as Excel (.xlsx)
        </button>

        <button class="export-btn" onclick="ExportManager.downloadFile('{doc['original_url']}', '{doc['filename']}')">
          <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
          Download Original ({doc['label']})
        </button>
      </div>
    </section>

    <!-- Document Preview Content -->
    <main class="doc-content-card">
      {doc['rendered_html']}
    </main>

    <!-- Site Footer -->
    <footer class="site-footer">
      <p>&copy; {datetime.datetime.now().year} Client Requirement Analysis • Interactive Web App</p>
    </footer>
  </div>

  <script src="../assets/js/storage.js"></script>
  <script src="../assets/js/calculator.js"></script>
  <script src="../assets/js/proposal.js"></script>
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
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="glass-header">
      <div class="brand-title">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <span>Interactive Proposal Builder</span>
      </div>
      <nav class="nav-links">
        <div class="breadcrumb">
          <a href="../index.html">Home</a>
          <span class="breadcrumb-sep">&rsaquo;</span>
          <span style="font-weight: 600; color: var(--text-main);">Proposal Generator</span>
        </div>
      </nav>
    </header>

    <!-- Interactive Client Banner -->
    <div id="project-banner-container"></div>

    <!-- Proposal Actions Bar -->
    <div class="glass-header" style="margin-bottom: 1.5rem;">
      <div style="font-weight: 700;">Proposal Actions</div>
      <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
        <button class="export-btn primary" onclick="ExportManager.exportPDF()">📄 Download PDF Proposal</button>
        <button class="export-btn" onclick="ProjectStorage.exportJSON()">💾 Export Project JSON</button>
        <label class="export-btn" style="cursor: pointer;">
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


# ─── Main Build Execution ────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("[BUILD] Building Interactive Static Site & Document Hub")
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

    discovered_files.sort(key=lambda p: str(p).lower())
    print(f"[DISCOVERY] Found {len(discovered_files)} document(s) in repository:\n")

    processed_docs = []

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

        processed_docs.append(doc_data)

    proposal_tool_html = generate_proposal_builder_tool_html()
    (PAGES_DIR / "interactive-proposal-builder.html").write_text(proposal_tool_html, encoding="utf-8")

    index_html = generate_index_html(processed_docs)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Interactive Static Site Successfully Built!")
    print(f"[OUTPUT] Directory: {OUTPUT_DIR}")
    print(f"[INDEX] Main Index: {OUTPUT_DIR / 'index.html'}")
    print(f"[TOOL] Proposal Builder: {PAGES_DIR / 'interactive-proposal-builder.html'}")
    print(f"[PAGES] Generated {len(processed_docs)} document pages in {PAGES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
