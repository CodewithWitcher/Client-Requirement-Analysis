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
    import os, hashlib
    # Use a content-based hash so the build stamp is stable across builds
    # unless the actual file content changes.  This prevents the stamp from
    # churning on every `build_site.py` run (which copies files and can
    # change mtimes).
    with open(file_path, 'rb') as f:
        build_stamp = hashlib.md5(f.read()).hexdigest()[:12]
    
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
                            # Store default as data attr — JS always sets the actual checked state from localStorage
                            is_checked_default = "true" if val_str.lower() in {"yes", "true", "1"} else "false"
                            row_cells.append(f'<{cell_tag} style="text-align: center;"><input type="checkbox" class="item-check" data-default-checked="{is_checked_default}"></{cell_tag}>')
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

                if item_id:
                    item_name = ws.cell(row=r_idx, column=2).value or ""
                    tr_attr = f'data-item-id="{item_id}" data-item-name="{html.escape(str(item_name))}"'
                else:
                    tr_attr = ''
                table_rows.append(f'<tr {tr_attr}>{"".join(row_cells)}</tr>')

            # Determine table CSS classes
            sheet_lower = sheet_name.lower()
            file_lower = str(file_path).lower()
            is_calculator_sheet = ("calculator" in sheet_lower) or ("pricing" in sheet_lower)
            is_maintenance_sheet = "maintenance" in sheet_lower
            is_hourly_rates_sheet = ("hourly" in sheet_lower) and ("rate" in sheet_lower)

            # Detect type (web/app) from sheet name first, then fall back to filename
            if "web" in sheet_lower:
                detected_type = "web"
            elif "app" in sheet_lower:
                detected_type = "app"
            elif "website" in file_lower:
                detected_type = "web"
            elif "application" in file_lower or " app " in file_lower or file_lower.endswith("app"):
                detected_type = "app"
            else:
                detected_type = "web"  # default

            if is_calculator_sheet:
                extra_class = "interactive-calc-table"
                extra_attrs = ""
            elif is_maintenance_sheet:
                extra_class = "maintenance-table"
                extra_attrs = f' data-maint-type="{detected_type}"'
            elif is_hourly_rates_sheet:
                extra_class = "hourly-rates-table"
                extra_attrs = f' data-rates-type="{detected_type}"'
            else:
                extra_class = ""
                extra_attrs = ""

            # Build toolbar row for interactive calculator sheets
            toolbar_row_html = ""
            if is_calculator_sheet:
                # Count columns from the header row
                col_count = 8  # default
                all_rows = table_rows
                if all_rows:
                    # Find the header row with #
                    for tr_html in all_rows:
                        if '<td>#</td>' in tr_html or '<td>#</td>' in tr_html:
                            col_count = tr_html.count('<td') + tr_html.count('<th')
                            break
                toolbar_row_html = f'''
<tr class="calc-toolbar-row" data-toolbar="true" style="background:rgba(99,102,241,0.04);border-top:2px dashed rgba(99,102,241,0.3);">
  <td colspan="{col_count}" style="padding:10px 14px;text-align:center;">
    <button class="calc-action-btn add-category-btn" data-action="add-category" title="Add a new category section">➕ Add Category</button>
    <button class="calc-action-btn add-item-btn" data-action="add-item" title="Add a new line item to a category" style="margin-left:8px;">➕ Add Line Item</button>
  </td>
</tr>'''

            pane_html = f'''
            <div id="{sheet_id}" class="sheet-pane {is_active}">
              <div class="table-responsive">
                <table class="doc-table {extra_class}"{extra_attrs}>
                  <tbody>
                    {"".join(table_rows)}
                    {toolbar_row_html}
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

          <div class="summary-card" id="maint-summary-card">
            <h3>🛠️ Maintenance Plans (Monthly)</h3>
            <div class="summary-row"><span>🌐 Website Maintenance:</span><strong id="summary-web-maint-monthly">—</strong></div>
            <div class="summary-row" style="font-size:0.8rem;color:var(--text-muted);"><span>Yearly Cost:</span><strong id="summary-web-maint-yearly">—</strong></div>
            <div class="summary-row" style="margin-top:0.5rem;"><span>📱 App Maintenance:</span><strong id="summary-app-maint-monthly">—</strong></div>
            <div class="summary-row" style="font-size:0.8rem;color:var(--text-muted);"><span>Yearly Cost:</span><strong id="summary-app-maint-yearly">—</strong></div>
          </div>

          <div class="summary-card" id="rates-summary-card">
            <h3>⏱️ Key Hourly Rates (WEB)</h3>
            <div class="summary-row"><span>Junior Dev:</span><strong id="summary-rate-junior">₹500/hr</strong></div>
            <div class="summary-row"><span>Senior Dev:</span><strong id="summary-rate-senior">₹1,800/hr</strong></div>
            <div class="summary-row"><span>Full-Stack (Sr):</span><strong id="summary-rate-fs-senior">₹2,200/hr</strong></div>
            <div class="summary-row"><span>Tech Architect:</span><strong id="summary-rate-architect">₹3,000/hr</strong></div>
          </div>
        </div>
        '''

        full_html = f'''
        <div id="project-banner-container"></div>

        <div class="excel-viewer" data-build-stamp="{build_stamp}">
          <div class="sheet-tabs">
            {"".join(tab_buttons)}
          </div>
          <div class="sheet-panes">
            {"".join(tab_panes)}
          </div>
        </div>

        {summary_widget_html}
        
        <script>
        // Bulletproof sheet tab switching (runs immediately, not dependent on other scripts)
        (function() {{
          var tabs = document.querySelectorAll('.sheet-tab-btn');
          tabs.forEach(function(btn) {{
            btn.addEventListener('click', function() {{
              var targetId = this.getAttribute('data-sheet-target');
              var container = this.closest('.excel-viewer') || document;
              container.querySelectorAll('.sheet-tab-btn').forEach(function(b) {{ b.classList.remove('active'); }});
              container.querySelectorAll('.sheet-pane').forEach(function(p) {{ p.classList.remove('active'); }});
              this.classList.add('active');
              var target = document.getElementById(targetId);
              if (target) target.classList.add('active');
            }});
          }});
        }})();
        </script>
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

    # Route all docs into their natural buckets (combined docs slot in alongside individual ones)
    calc_docs = [d for d in documents if d['category'] == 'xlsx']
    proposal_docs = [d for d in documents if d['category'] == 'docx' or 'pricing-parameters' in d['slug']]
    questionnaire_docs = [d for d in documents if 'questionnaire' in d['slug']]
    checklist_docs = [d for d in documents if 'checklist' in d['slug']]
    guide_docs = [d for d in documents if d not in calc_docs and d not in proposal_docs and d not in questionnaire_docs and d not in checklist_docs]

    calc_cards_html = "".join([render_doc_card_html(d) for d in calc_docs])
    proposal_cards_html = "".join([render_doc_card_html(d) for d in proposal_docs])
    quest_cards_html = "".join([render_doc_card_html(d) for d in questionnaire_docs])
    check_cards_html = "".join([render_doc_card_html(d) for d in checklist_docs])
    guide_cards_html = "".join([render_doc_card_html(d) for d in guide_docs])

    md_count = sum(1 for d in documents if d['category'] == 'md')
    docx_count = sum(1 for d in documents if d['category'] == 'docx')
    xlsx_count = sum(1 for d in documents if d['category'] == 'xlsx')

    web_count = sum(1 for d in documents if 'web' in d['topics'] and 'combined' not in d['topics'])
    mobile_count = sum(1 for d in documents if 'mobile' in d['topics'] and 'combined' not in d['topics'])
    pricing_count = sum(1 for d in documents if 'pricing' in d['topics'] and 'combined' not in d['topics'])

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
        <a href="pages/client-onboarding-flow.html" class="nav-pill" style="background: linear-gradient(135deg, #10b981, #059669); color: #ffffff; border-color: #10b981; font-weight: 700;">🚀 Onboarding Flow</a>
        <a href="pages/interactive-proposal-builder.html" class="nav-pill">Proposal Builder</a>
        <a href="pages/ai-intelligence-engine.html" class="nav-pill ai-pill">🧠 AI Studio</a>
      </nav>
    </header>



    <!-- Hero: Onboarding Flow CTA Banner -->
    <section class="hero-section" style="margin-top: 1rem; padding: 2rem 2rem 2rem 2.5rem; text-align: left; display: flex; align-items: center; gap: 2rem; flex-wrap: wrap; background: linear-gradient(135deg, rgba(16,185,129,0.05), rgba(59,130,246,0.05)); border: 1px solid rgba(16,185,129,0.15);">
      <div style="flex: 1; min-width: 280px;">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0.75rem; background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.25); border-radius: 20px; font-size: 0.75rem; font-weight: 700; color: #059669; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;">
          🆕 NEW — Professional Onboarding System
        </div>
        <h2 style="margin-bottom: 0.5rem; font-size: 1.8rem;">🚀 Client Onboarding Flow</h2>
        <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.7; max-width: 600px;">
          A complete step-by-step system to onboard clients like a pro — from discovery call to project kickoff. Follow the proven 8-stage workflow with linked questionnaires, proposals, pricing calculators, and checklists tailored to Website, Application, or Combined projects.
        </p>
        <a href="pages/client-onboarding-flow.html" style="display: inline-flex; align-items: center; gap: 0.5rem; margin-top: 1rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #059669); color: #ffffff; border-radius: 10px; font-weight: 700; font-size: 0.95rem; text-decoration: none; transition: all 0.2s ease; box-shadow: 0 4px 15px rgba(16,185,129,0.3);">
          Start Onboarding Flow →
        </a>
      </div>
      <div style="flex-shrink: 0; display: flex; gap: 0.5rem; flex-wrap: wrap;">
        <div style="text-align: center; padding: 1rem 1.5rem; background: rgba(255,255,255,0.7); border-radius: 12px; border: 1px solid rgba(59,130,246,0.15);">
          <div style="font-size: 2rem;">🔍</div>
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Discovery</div>
          <div style="font-size: 0.7rem; color: var(--text-subtle);">Call → Questionnaire</div>
        </div>
        <div style="text-align: center; padding: 1rem 1.5rem; background: rgba(255,255,255,0.7); border-radius: 12px; border: 1px solid rgba(245,158,11,0.2);">
          <div style="font-size: 2rem;">📄</div>
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Proposal</div>
          <div style="font-size: 0.7rem; color: var(--text-subtle);">Build → Send → Approve</div>
        </div>
        <div style="text-align: center; padding: 1rem 1.5rem; background: rgba(255,255,255,0.7); border-radius: 12px; border: 1px solid rgba(16,185,129,0.2);">
          <div style="font-size: 2rem;">💰</div>
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Pricing</div>
          <div style="font-size: 0.7rem; color: var(--text-subtle);">Calculator → Milestones</div>
        </div>
        <div style="text-align: center; padding: 1rem 1.5rem; background: rgba(255,255,255,0.7); border-radius: 12px; border: 1px solid rgba(132,204,22,0.2);">
          <div style="font-size: 2rem;">🚀</div>
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Kickoff</div>
          <div style="font-size: 0.7rem; color: var(--text-subtle);">Contract → Development</div>
        </div>
      </div>
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
        # Excel Calculator Page - Save button first, then Excel/PDF downloads
        buttons.append(f'''
        <button id="save-pricing-btn" class="export-btn" style="background: linear-gradient(135deg, #10b981, #059669); border-color: #10b981; color: #ffffff; font-weight: 700; font-size: 0.9rem; padding: 0.6rem 1.4rem; gap: 0.5rem;" onclick="savePricingState()">
          <svg viewBox="0 0 24 24"><path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/></svg>
          💾 Save Pricing Changes
        </button>
        ''')
        buttons.append(f'''
        <a href="interactive-proposal-builder.html" id="go-to-proposal-btn" class="export-btn" style="color: #6366f1; border-color: #6366f1; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem;">
          <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
          View Proposal Builder
        </a>
        ''')
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
<body class="{'full-width-layout' if doc.get('category') == 'xlsx' else ''}">

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

    <!-- Interactive Client Banner -->
    <div id="project-banner-container"></div>

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

  <!-- Global Floating Save Bar (shows on any page when unsaved changes exist) -->
  <div id="global-save-bar" style="
    position: fixed; bottom: -80px; left: 50%; transform: translateX(-50%);
    background: #0f172a; color: #ffffff;
    padding: 0.75rem 1.5rem; border-radius: 50px;
    display: flex; align-items: center; gap: 0.9rem;
    box-shadow: 0 8px 32px rgba(15,23,42,0.35);
    z-index: 99999; transition: bottom 0.4s cubic-bezier(0.16,1,0.3,1);
    border: 1px solid rgba(255,255,255,0.08); min-width: 340px; justify-content: center;
  ">
    <span id="global-save-msg" style="font-size: 0.88rem; font-weight: 600; opacity: 0.85;">⚠️ You have unsaved changes</span>
    <button id="global-save-btn" onclick="globalSaveAllData()" style="
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff; border: none; border-radius: 25px;
      padding: 0.45rem 1.1rem; font-size: 0.85rem; font-weight: 700;
      cursor: pointer; transition: all 0.2s ease; white-space: nowrap;
    ">💾 Save Now</button>
    <button onclick="document.getElementById('global-save-bar').style.bottom='-80px'" style="
      background: transparent; border: none; color: rgba(255,255,255,0.4);
      font-size: 1.1rem; cursor: pointer; padding: 0 0.2rem; line-height: 1;
    " title="Dismiss">✕</button>
  </div>

  <script src="../assets/js/storage.js"></script>
  <script src="../assets/js/calculator.js"></script>
  <script src="../assets/js/proposal.js"></script>
  <script src="../assets/js/assistant.js"></script>
  <script src="../assets/js/ai-engine.js"></script>
  <script src="../assets/js/main.js"></script>
  <script src="../assets/js/export.js"></script>
  <script>
    // Global Save Bar Controller
    let _globalSavePending = false;
    function showGlobalSaveBar(msg) {{
      const bar = document.getElementById('global-save-bar');
      const msgEl = document.getElementById('global-save-msg');
      if (msgEl) msgEl.textContent = msg || '⚠️ You have unsaved changes';
      if (bar) bar.style.bottom = '24px';
      _globalSavePending = true;
    }}
    function hideGlobalSaveBar() {{
      const bar = document.getElementById('global-save-bar');
      if (bar) bar.style.bottom = '-80px';
      _globalSavePending = false;
    }}
    function globalSaveAllData() {{
      // Save pricing calculator data if on a calculator page
      if (typeof savePricingState === 'function') savePricingState();
      // Save checklist data via storage
      if (window.ProjectStorage) {{
        const proj = window.ProjectStorage.getProject();
        window.ProjectStorage.saveProject(proj);
      }}
      // Visual feedback on bar
      const btn = document.getElementById('global-save-btn');
      const msg = document.getElementById('global-save-msg');
      if (btn) {{ btn.textContent = '✅ Saved!'; btn.style.background = 'linear-gradient(135deg, #6366f1, #4f46e5)'; }}
      if (msg) msg.textContent = '✅ All changes saved to your workspace';
      if (typeof window.showToast === 'function') window.showToast('✅ All changes saved successfully!', 'success');
      setTimeout(() => {{
        hideGlobalSaveBar();
        if (btn) {{ btn.textContent = '💾 Save Now'; btn.style.background = 'linear-gradient(135deg, #10b981, #059669)'; }}
      }}, 2000);
    }}
    // Intercept all changes globally to show the save bar
    document.addEventListener('DOMContentLoaded', () => {{
      // Watch for checkbox changes
      document.addEventListener('change', (e) => {{
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {{
          showGlobalSaveBar();
        }}
      }});
      // Watch for number/text input changes
      document.addEventListener('input', (e) => {{
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {{
          showGlobalSaveBar();
        }}
      }});
    }});
  </script>
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
        <button class="nav-pill" style="background: linear-gradient(135deg, #3b82f6, #2563eb); border-color: #3b82f6; color: #ffffff; font-weight: 700;" onclick="ExportManager.exportDOCX(null, 'Client_Proposal.doc')">📝 Download Word Proposal</button>
        <a id="proposal-actions-edit-btn" href="template-excel-template-website-pricing-calculator.html" class="nav-pill" style="color: #ffffff; text-decoration: none; font-weight: 700; background: rgba(255,255,255,0.15); border-color: rgba(255,255,255,0.25);">✏️ Edit Web Pricing</a>
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

  <!-- Global Floating Save Bar -->
  <div id="global-save-bar" style="
    position: fixed; bottom: -80px; left: 50%; transform: translateX(-50%);
    background: #0f172a; color: #ffffff;
    padding: 0.75rem 1.5rem; border-radius: 50px;
    display: flex; align-items: center; gap: 0.9rem;
    box-shadow: 0 8px 32px rgba(15,23,42,0.35);
    z-index: 99999; transition: bottom 0.4s cubic-bezier(0.16,1,0.3,1);
    border: 1px solid rgba(255,255,255,0.08); min-width: 340px; justify-content: center;
  ">
    <span id="global-save-msg" style="font-size: 0.88rem; font-weight: 600; opacity: 0.85;">⚠️ You have unsaved changes</span>
    <button id="global-save-btn" onclick="globalSaveAllData()" style="
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff; border: none; border-radius: 25px;
      padding: 0.45rem 1.1rem; font-size: 0.85rem; font-weight: 700;
      cursor: pointer; transition: all 0.2s ease; white-space: nowrap;
    ">💾 Save Now</button>
    <button onclick="document.getElementById('global-save-bar').style.bottom='-80px'" style="
      background: transparent; border: none; color: rgba(255,255,255,0.4);
      font-size: 1.1rem; cursor: pointer; padding: 0 0.2rem; line-height: 1;
    " title="Dismiss">✕</button>
  </div>
  <script>
    let _globalSavePending = false;
    function showGlobalSaveBar(msg) {{
      const bar = document.getElementById('global-save-bar');
      const msgEl = document.getElementById('global-save-msg');
      if (msgEl) msgEl.textContent = msg || '⚠️ You have unsaved changes';
      if (bar) bar.style.bottom = '24px';
      _globalSavePending = true;
    }}
    function hideGlobalSaveBar() {{
      const bar = document.getElementById('global-save-bar');
      if (bar) bar.style.bottom = '-80px';
      _globalSavePending = false;
    }}
    function globalSaveAllData() {{
      if (window.ProjectStorage) {{
        const proj = window.ProjectStorage.getProject();
        window.ProjectStorage.saveProject(proj);
      }}
      const btn = document.getElementById('global-save-btn');
      const msg = document.getElementById('global-save-msg');
      if (btn) {{ btn.textContent = '✅ Saved!'; btn.style.background = 'linear-gradient(135deg, #6366f1, #4f46e5)'; }}
      if (msg) msg.textContent = '✅ All changes saved to your workspace';
      if (typeof window.showToast === 'function') window.showToast('✅ All changes saved successfully!', 'success');
      setTimeout(() => {{
        hideGlobalSaveBar();
        if (btn) {{ btn.textContent = '💾 Save Now'; btn.style.background = 'linear-gradient(135deg, #10b981, #059669)'; }}
      }}, 2000);
    }}
    document.addEventListener('DOMContentLoaded', () => {{
      document.addEventListener('change', (e) => {{
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') showGlobalSaveBar();
      }});
      document.addEventListener('input', (e) => {{
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') showGlobalSaveBar();
      }});
    }});
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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
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

    <!-- Consolidated Intake & Document Selector Dashboard Grid -->
    <div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 1.5rem; margin-bottom: 2rem; align-items: start;">
      
      <!-- Left Column: Intake Wizard & File Uploader -->
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        
        <!-- Intake Wizard Card -->
        <main class="doc-content-card" style="padding: 1.25rem; margin: 0; min-height: auto;">
          <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
            <span>📋</span> Technical Intake Wizard
          </h3>
          
          <div style="display: flex; flex-direction: column; gap: 0.85rem;">
            <div class="form-group" style="margin: 0;">
              <label style="font-size: 0.82rem; margin-bottom: 0.25rem; font-weight: 700;">Target Project Platform:</label>
              <select id="ai-wizard-platform" class="form-control" onchange="toggleWizardFields(this.value)" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
                <option value="Website">🌐 Website / Web App Only</option>
                <option value="Android">🤖 Android App Only</option>
                <option value="iOS">🍎 iOS App Only</option>
                <option value="Mobile">📱 Both Android & iOS Mobile Apps</option>
                <option value="Both">⚡ Both Website & Mobile Apps (All Platforms)</option>
                <option value="Custom">⚙️ Custom Platform...</option>
              </select>
              <div id="ai-wizard-custom-platform-container" style="margin-top: 0.5rem; display: none;">
                <input type="text" id="ai-wizard-custom-platform-input" class="form-control" placeholder="Enter Custom Platform Name (e.g. Smart TV App)" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
              </div>
            </div>

            <div class="form-group" style="margin: 0;">
              <label style="font-size: 0.82rem; margin-bottom: 0.25rem; font-weight: 700;">Target Industry / Domain:</label>
              <input type="text" id="ai-wizard-industry" class="form-control" placeholder="e.g. E-Commerce, SaaS, Fintech" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
            </div>

            <div class="form-group" id="group-seo" style="margin: 0;">
              <label style="font-size: 0.82rem; margin-bottom: 0.25rem; font-weight: 700;">SEO & Growth Priority:</label>
              <select id="ai-wizard-seo" class="form-control" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
                <option value="High (Local & National SEO + Schema.org + OpenGraph)">🚀 High (SEO + Schema.org)</option>
                <option value="Medium (Standard On-Page Meta & Sitemap)">Standard Meta Tags & Sitemap</option>
                <option value="Internal Tool (No SEO Needed)">Internal Platform (No Public SEO)</option>
              </select>
            </div>

            <div class="form-group" style="margin: 0;">
              <label style="font-size: 0.82rem; margin-bottom: 0.25rem; font-weight: 700;">Cloud Hosting Preference:</label>
              <select id="ai-wizard-hosting" class="form-control" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
                <option value="AWS Cloud Container Stack">AWS (ECS / RDS / S3)</option>
                <option value="Vercel + Managed Postgres">Vercel / Netlify + Supabase</option>
                <option value="DigitalOcean App Platform">DigitalOcean App Platform</option>
                <option value="Google Cloud Platform (GCP)">Google Cloud Platform (GCP)</option>
              </select>
            </div>

            <div class="form-group" style="margin: 0;">
              <label style="font-size: 0.82rem; margin-bottom: 0.25rem; font-weight: 700;">Expected Traffic / Active User Scale:</label>
              <select id="ai-wizard-traffic" class="form-control" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
                <option value="10,000+ monthly active users">10,000+ monthly active users</option>
                <option value="100,000+ monthly active users">100,000+ high concurrency users</option>
                <option value="Startup Initial Launch (<5k users)">Startup Launch (<5,000 users)</option>
              </select>
            </div>

            <div class="form-group" style="margin: 0;">
              <label style="font-size: 0.82rem; margin-bottom: 0.25rem; font-weight: 700;">Delivery Timeline Urgency:</label>
              <select id="ai-wizard-timeline" class="form-control" style="font-size: 0.85rem; padding: 0.45rem 0.75rem;">
                <option value="Standard Sprint Delivery (4–8 Weeks)">Standard Sprint Delivery (4–8 Weeks)</option>
                <option value="Fast-Track MVP (2–4 Weeks)">Fast-Track MVP (2–4 Weeks)</option>
                <option value="Enterprise Multi-Phase Roadmap">Enterprise Multi-Phase Roadmap</option>
              </select>
            </div>
          </div>
        </main>

        <!-- Document Upload Card -->
        <main class="doc-content-card" style="padding: 1.25rem; margin: 0; min-height: auto;">
          <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
            <span>📄</span> Upload Requirement File
          </h3>
          <div style="border: 2px dashed var(--accent-indigo); padding: 1.25rem; border-radius: 8px; text-align: center; background: rgba(99, 102, 241, 0.02);">
            <input type="file" id="ai-doc-file" accept=".pdf,.docx,.txt,.md" style="display: none;" onchange="updateFileLabel(this)">
            <button class="export-btn primary" onclick="document.getElementById('ai-doc-file').click()" style="padding: 0.5rem 1rem; font-size: 0.85rem; margin-bottom: 0.5rem; justify-content: center; width: 100%;">
              📁 Choose File (PDF/DOCX/TXT/MD)
            </button>
            <div id="ai-file-name-label" style="font-size: 0.75rem; color: var(--text-subtle); line-height: 1.4;">No file chosen yet. (Optional)</div>
          </div>
        </main>
      </div>

      <!-- Right Column: Deliverables Selector & Pipeline Run -->
      <main class="doc-content-card" style="padding: 1.25rem; margin: 0; display: flex; flex-direction: column; align-self: stretch; min-height: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
          <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin: 0;">
            <span>🛠️</span> AI Deliverables
          </h3>
          <div style="display: flex; gap: 0.35rem;">
            <button class="export-btn" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="selectAllDocTypes(true)">Check All</button>
            <button class="export-btn" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="selectAllDocTypes(false)">Clear</button>
          </div>
        </div>

        <div class="card-grid" style="grid-template-columns: 1fr; gap: 0.65rem; max-height: 480px; overflow-y: auto; padding-right: 0.25rem;" id="ai-doc-type-grid">
          <!-- Rendered via JS script below -->
        </div>

        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end;">
          <button class="export-btn primary" style="padding: 0.75rem 1.5rem; font-size: 0.95rem; background: linear-gradient(135deg, var(--accent-indigo), var(--accent-primary)); border: none; box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3); width: 100%; justify-content: center;" onclick="startAiGenerationPipeline()">
            🚀 Generate Selected AI Documents
          </button>
        </div>
      </main>
    </div>

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

    <!-- Full-Screen Document Reader Modal -->
    <div id="ai-doc-reader-modal" class="modal-overlay" style="display: none; z-index: 12000; align-items: center; justify-content: center; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);">
      <div class="modal-card" style="max-width: 90vw; width: 1000px; height: 85vh; display: flex; flex-direction: column; padding: 0; overflow: hidden; background: #ffffff; border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); border: 1px solid rgba(255, 255, 255, 0.2);">
        <!-- Modal Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; background: #f8fafc;">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span id="reader-modal-icon" style="font-size: 1.5rem;">📄</span>
            <h3 id="reader-modal-title" style="font-family: var(--font-serif); font-size: 1.3rem; margin: 0; color: var(--text-main);">Technical Document Reader</h3>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <button class="export-btn primary" id="reader-modal-open-btn" style="font-size: 0.8rem; padding: 0.35rem 0.85rem;">🚀 Open Page</button>
            <button class="export-btn" id="reader-modal-copy-btn" style="font-size: 0.8rem; padding: 0.35rem 0.85rem;">📋 Copy Content</button>
            <button class="export-btn" onclick="closeDocReaderModal()" style="font-size: 0.8rem; padding: 0.35rem 0.85rem; background: #ef4444; color: #fff; border-color: #ef4444;">✕ Close</button>
          </div>
        </div>
        <!-- Modal Body (Parsed Rich Markdown) -->
        <div id="reader-modal-body" class="rendered-markdown" style="flex: 1; overflow-y: auto; padding: 2.5rem; background: #ffffff; color: var(--text-main); font-size: 1rem; line-height: 1.7; text-align: left;">
          <!-- Parsed markdown will be injected here -->
        </div>
      </div>
    </div>

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
      renderExistingGeneratedDocs();
    }});

    function toggleWizardFields(val) {{
      const seoGroup = document.getElementById('group-seo');
      if (seoGroup) {{
        seoGroup.style.display = (val === 'Mobile' || val === 'Android' || val === 'iOS') ? 'none' : 'block';
      }}
      const customContainer = document.getElementById('ai-wizard-custom-platform-container');
      if (customContainer) {{
        customContainer.style.display = (val === 'Custom') ? 'block' : 'none';
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
      const platformSelectVal = document.getElementById('ai-wizard-platform').value;
      const finalPlatform = (platformSelectVal === 'Custom')
        ? (document.getElementById('ai-wizard-custom-platform-input')?.value.trim() || 'Custom')
        : platformSelectVal;

      const context = {{
        clientName: proj.clientName || 'Client',
        projectName: proj.projectName || 'Project',
        projectType: finalPlatform,
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

      renderExistingGeneratedDocs();

      if (window.showToast) window.showToast(`Generated ${{results.length}} technical documents and auto-filled workspace pages!`, "success");
    }}

    async function downloadAllAiDeliverables() {{
      const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
      if (!proj || !proj.aiGeneratedDocs || !Object.keys(proj.aiGeneratedDocs).length) {{
        alert("No AI deliverables generated yet.");
        return;
      }}

      if (typeof JSZip === 'undefined') {{
        alert("JSZip library is still loading. Please try again in a moment.");
        return;
      }}

      if (window.showToast) window.showToast("Preparing ZIP archive...", "info");

      const zip = new JSZip();
      Object.keys(proj.aiGeneratedDocs).forEach(id => {{
        const doc = proj.aiGeneratedDocs[id];
        const safeTitle = doc.title.replace(/[^a-z0-9\\s-_]+/gi, '').replace(/\\s+/g, '_');
        zip.file(`${{safeTitle}}.md`, doc.markdown);
      }});

      try {{
        const content = await zip.generateAsync({{ type: 'blob' }});
        const url = URL.createObjectURL(content);
        const link = document.createElement('a');
        link.href = url;
        const safeClientName = proj.clientName.replace(/[^a-z0-9]+/gi, '_');
        link.download = `AI_Deliverables_${{safeClientName}}.zip`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        if (window.showToast) window.showToast("Downloaded all files as ZIP!", "success");
      }} catch (err) {{
        console.error("ZIP creation failed:", err);
        alert("Failed to build ZIP archive.");
      }}
    }}

    function escapeHtml(str) {{
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }}

    let currentSelectedAiDocId = null;

    function renderExistingGeneratedDocs() {{
      const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
      const resultsContainer = document.getElementById('ai-results-container');
      if (!resultsContainer) return;

      if (!proj || !proj.aiGeneratedDocs || !Object.keys(proj.aiGeneratedDocs).length) {{
        resultsContainer.innerHTML = '';
        return;
      }}

      const docs = Object.values(proj.aiGeneratedDocs);
      if (!currentSelectedAiDocId || !proj.aiGeneratedDocs[currentSelectedAiDocId]) {{
        currentSelectedAiDocId = docs[0].id;
      }}

      let tabsHtml = '';
      for (let loop = 0; loop < 3; loop++) {{
        docs.forEach(doc => {{
          const isActive = doc.id === currentSelectedAiDocId;
          const activeStyles = isActive 
            ? 'background: rgba(99, 102, 241, 0.08); border-color: var(--accent-indigo); color: var(--accent-indigo); font-weight: 700;'
            : 'background: #ffffff; border-color: #e2e8f0; color: var(--text-muted);';
          tabsHtml += `
            <button class="export-btn" style="padding: 0.5rem 0.75rem; border-radius: 6px; text-align: left; font-size: 0.82rem; cursor: pointer; transition: all 0.2s; display: block; width: 100%; border: 1px solid; margin-bottom: 0.35rem; ${{activeStyles}}" onclick="switchAiDocTab('${{doc.id}}')">
              ${{doc.icon || '📄'}} ${{doc.title}}
            </button>
          `;
        }});
      }}

      const activeDoc = proj.aiGeneratedDocs[currentSelectedAiDocId];
      const isAgentPrompt = activeDoc.id === 'agent_prompt';
      
      let refinementHistoryHtml = '';
      if (isAgentPrompt && proj.aiPromptRefinements && proj.aiPromptRefinements.length) {{
        refinementHistoryHtml = `
          <div style="background: rgba(99, 102, 241, 0.03); border: 1px solid rgba(99, 102, 241, 0.15); border-radius: 8px; padding: 0.75rem; margin-top: 1rem;">
            <div style="font-weight: 700; font-size: 0.8rem; color: var(--accent-indigo); margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.35rem;">
              ⏳ Refinement History Memory Context
            </div>
            <ul style="margin: 0; padding-left: 1.1rem; font-size: 0.75rem; color: var(--text-muted); line-height: 1.4; text-align: left;">
        `;
        proj.aiPromptRefinements.forEach(r => {{
          refinementHistoryHtml += `<li><b>\${{new Date(r.timestamp).toLocaleTimeString()}}:</b> \${{escapeHtml(r.text)}}</li>`;
        }});
        refinementHistoryHtml += `</ul></div>`;
      }}

      let refinementPanelHtml = '';
      if (isAgentPrompt) {{
        refinementPanelHtml = `
          <div style="margin-top: 1rem; border-top: 1px dashed #cbd5e1; padding-top: 1rem; text-align: left;">
            <div style="font-weight: 700; font-size: 0.88rem; color: var(--text-main); margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.35rem;">
              🤖 Add Features / Refine Coding Prompt
            </div>
            <p style="font-size: 0.75rem; color: var(--text-subtle); margin: 0 0 0.5rem 0; line-height: 1.4;">
              Type new feature specifications or bug fixes. The system will build upon your existing prompt history utilizing session context memory.
            </p>
            <div style="display: flex; gap: 0.5rem; align-items: stretch;">
              <textarea id="ai-refinement-input" class="form-control" placeholder="e.g. Add Google/Apple social sign-in support and write Jest integration tests." style="font-size: 0.8rem; padding: 0.45rem 0.75rem; flex: 1; min-height: 50px; resize: vertical;"></textarea>
              <button id="ai-refine-btn" class="export-btn primary" style="font-size: 0.82rem; padding: 0 1rem;" onclick="refineActivePrompt()">
                ⚡ Refine Prompt
              </button>
            </div>
            ${{refinementHistoryHtml}}
          </div>
        `;
      }}

      let resultsHtml = `
        <main class="doc-content-card" style="min-height: auto; margin-bottom: 2rem; padding: 1.25rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.75rem; flex-wrap: wrap; gap: 0.75rem;">
            <h2 style="font-family: var(--font-serif); font-size: 1.3rem; margin: 0;">✨ Generated Technical Deliverables</h2>
            <div style="display: flex; gap: 0.5rem;">
              <button class="export-btn primary" style="padding: 0.4rem 0.85rem; font-size: 0.8rem;" onclick="downloadAllAiDeliverables()">📦 Download All</button>
              <button class="export-btn" style="color: #ef4444; border-color: #ef4444; padding: 0.4rem 0.85rem; font-size: 0.8rem;" onclick="clearAllAiDeliverables()">🗑️ Clear All</button>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 240px 1fr; gap: 1.25rem; align-items: stretch; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); min-height: 560px;">
            <div id="ai-tabs-container" style="display: flex; flex-direction: column; gap: 0.15rem; max-height: 560px; overflow-y: auto; border-right: 1px solid #e2e8f0; padding-right: 1rem;">
              ${{tabsHtml}}
            </div>

            <!-- Right: Selected Document Detail -->
            <div style="display: flex; flex-direction: column; justify-content: space-between;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.5rem; margin-bottom: 0.5rem;">
                <div style="font-weight: 700; font-size: 1.05rem; color: var(--text-main); display: flex; align-items: center; gap: 0.35rem;">
                  ${{activeDoc.icon || '📄'}} ${{activeDoc.title}}
                </div>
                <div style="display: flex; gap: 0.4rem;">
                  <button class="export-btn primary" style="font-size: 0.78rem; padding: 0.3rem 0.65rem; background: var(--accent-indigo); border-color: var(--accent-indigo);" onclick="openDocReaderModal('${{activeDoc.id}}')">📖 Read Full Document</button>
                  <a href="${{activeDoc.targetSlug}}.html" class="export-btn" style="font-size: 0.78rem; padding: 0.3rem 0.65rem;">🚀 Open Page</a>
                  <button class="export-btn" style="font-size: 0.78rem; padding: 0.3rem 0.65rem;" onclick="copyDocTextToClipboard('${{activeDoc.id}}')">📋 Copy Content</button>
                </div>
              </div>

              <pre style="background: #f8fafc; padding: 0.85rem; border-radius: 8px; border: 1px solid #e2e8f0; height: 500px; overflow-y: auto; font-size: 0.82rem; line-height: 1.45; margin: 0; white-space: pre-wrap; word-break: break-word;">${{escapeHtml(activeDoc.markdown)}}</pre>
              ${{refinementPanelHtml}}
            </div>
          </div>
        </main>
      `;

      resultsContainer.innerHTML = resultsHtml;

      // Hook up infinite scroll loop on the tabs list
      const tabContainer = document.getElementById('ai-tabs-container');
      if (tabContainer) {{
        const singleSetHeight = tabContainer.scrollHeight / 3;
        
        // Scroll to the middle set initially
        if (tabContainer.scrollTop === 0) {{
          tabContainer.scrollTop = singleSetHeight;
        }}

        tabContainer.onscroll = () => {{
          if (tabContainer.scrollTop < 10) {{
            tabContainer.scrollTop += singleSetHeight;
          }} else if (tabContainer.scrollTop > (singleSetHeight * 2) - 10) {{
            tabContainer.scrollTop -= singleSetHeight;
          }}
        }};
      }}
    }}

    function switchAiDocTab(id) {{
      currentSelectedAiDocId = id;
      renderExistingGeneratedDocs();
    }}

    function openDocReaderModal(id) {{
      const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
      if (!proj || !proj.aiGeneratedDocs || !proj.aiGeneratedDocs[id]) return;

      const doc = proj.aiGeneratedDocs[id];
      
      document.getElementById('reader-modal-icon').textContent = doc.icon || '📄';
      document.getElementById('reader-modal-title').textContent = doc.title;
      
      const openBtn = document.getElementById('reader-modal-open-btn');
      openBtn.onclick = () => {{ window.location.href = `${{doc.targetSlug}}.html`; }};
      
      const copyBtn = document.getElementById('reader-modal-copy-btn');
      copyBtn.onclick = () => {{ copyDocTextToClipboard(doc.id); }};
      
      const bodyEl = document.getElementById('reader-modal-body');
      if (typeof marked !== 'undefined') {{
        bodyEl.innerHTML = marked.parse(doc.markdown);
      }} else {{
        bodyEl.innerHTML = `<pre style="white-space: pre-wrap;">\${{escapeHtml(doc.markdown)}}</pre>`;
      }}
      bodyEl.scrollTop = 0;
      setTimeout(() => {{
        bodyEl.scrollTop = 0;
      }}, 50);

      document.getElementById('ai-doc-reader-modal').style.display = 'flex';
    }}

    function closeDocReaderModal() {{
      document.getElementById('ai-doc-reader-modal').style.display = 'none';
    }}

    async function refineActivePrompt() {{
      const inputEl = document.getElementById('ai-refinement-input');
      const text = inputEl ? inputEl.value.trim() : '';
      if (!text) {{
        alert("Please enter a feature description or fix request.");
        return;
      }}

      const apiKey = window.SmartAssistant ? window.SmartAssistant.getApiKey() : '';
      if (!apiKey) {{
        alert("DeepSeek API Key is required to refine the prompt. Please add it in the key manager at the top.");
        return;
      }}

      const btn = document.getElementById('ai-refine-btn');
      if (btn) {{
        btn.disabled = true;
        btn.textContent = "⚡ Refining Prompt...";
      }}

      try {{
        if (window.showToast) window.showToast("Refining coding prompt using memory context...", "info");
        await window.AIEngine.generateRefinedPrompt(text, apiKey);
        if (inputEl) inputEl.value = '';
        renderExistingGeneratedDocs();
        if (window.showToast) window.showToast("Successfully updated coding prompt!", "success");
      }} catch (err) {{
        alert("Prompt refinement failed: " + err.message);
      }} finally {{
        if (btn) {{
          btn.disabled = false;
          btn.textContent = "⚡ Refine Prompt";
        }}
      }}
    }}

    function clearAllAiDeliverables() {{
      if (confirm("Are you sure you want to clear all generated AI documents for this client workspace? This cannot be undone.")) {{
        const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
        if (proj) {{
          proj.aiGeneratedDocs = {{}};
          proj.aiPromptRefinements = [];
          window.ProjectStorage.saveProject(proj);
          renderExistingGeneratedDocs();
          if (window.showToast) window.showToast("Cleared generated documents.", "info");
        }}
      }}
    }}

    function copyDocTextToClipboard(id) {{
      const proj = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
      if (proj && proj.aiGeneratedDocs && proj.aiGeneratedDocs[id]) {{
        navigator.clipboard.writeText(proj.aiGeneratedDocs[id].markdown);
        if (window.showToast) window.showToast("Copied content to clipboard!", "success");
      }}
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
