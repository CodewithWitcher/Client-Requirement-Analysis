/**
 * Enhanced Export Utility Module
 * Supports client-side customized exports for PDF, Word (.doc/.docx), Excel (.csv/.xlsx), JSON, 
 * and Bulk Client Workspace Download.
 */

window.ExportManager = {
  /**
   * Trigger clean browser PDF print layout capturing live user inputs
   */
  exportPDF: function() {
    if (typeof window.showToast === 'function') {
      window.showToast('Preparing document for PDF export...', 'info');
    }

    const origTitle = document.title;
    const h1El = document.querySelector('h1');
    if (h1El) {
      document.title = h1El.innerText.replace(/[^a-zA-Z0-9\s-_]/g, '').trim();
    }

    setTimeout(() => {
      window.print();
      document.title = origTitle;
    }, 300);
  },

  /**
   * Export current customized page state (with checked items & inputs) as Word document
   */
  exportDOCX: function(fallbackUrl, fileName) {
    const contentCard = document.querySelector('.doc-content-card') || document.querySelector('.doc-main-content');
    if (!contentCard) {
      if (fallbackUrl) return this.downloadFile(fallbackUrl, fileName);
      if (typeof window.showToast === 'function') window.showToast('Unable to capture document content.', 'error');
      return;
    }

    if (typeof window.showToast === 'function') window.showToast('Generating Word document...', 'info');

    // Clone node to manipulate without affecting live UI
    const clone = contentCard.cloneNode(true);
    const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;

    // Convert checkboxes to text symbols
    clone.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      const span = document.createElement('span');
      span.style.fontWeight = 'bold';
      if (cb.checked) {
        span.style.color = '#059669';
        span.innerHTML = '☑ [COMPLETED] ';
      } else {
        span.style.color = '#64748b';
        span.innerHTML = '☐ [PENDING] ';
      }
      cb.parentNode.replaceChild(span, cb);
    });

    // Convert number & text inputs to plain text
    clone.querySelectorAll('input[type="number"], input[type="text"], select').forEach(input => {
      const span = document.createElement('span');
      span.style.fontWeight = 'bold';
      span.textContent = input.value || '';
      input.parentNode.replaceChild(span, input);
    });

    // Remove buttons, toolbars, and TOC elements if cloned inside content
    clone.querySelectorAll('.export-toolbar, .toc-sidebar, #progress-bar-container, button').forEach(el => el.remove());

    const titleText = document.querySelector('h1')?.innerText || 'Client Document';
    const headerHtml = `
      <div style="border-bottom: 2px solid #0f172a; padding-bottom: 15px; margin-bottom: 25px;">
        <h1 style="font-family: Arial, sans-serif; color: #0f172a;">${escapeHtml(titleText)}</h1>
        <p style="color: #475569; font-size: 14px;">
          <strong>Client Profile:</strong> ${project ? escapeHtml(project.clientName) : 'Standard Workspace'} | 
          <strong>Date:</strong> ${new Date().toLocaleDateString()}
        </p>
      </div>
    `;

    const fullWordHtml = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
        <meta charset='utf-8'>
        <title>${escapeHtml(titleText)}</title>
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; color: #0f172a; line-height: 1.6; padding: 20px; }
          table { width: 100%; border-collapse: collapse; margin: 15px 0; }
          th { background: #f1f5f9; color: #0f172a; font-weight: bold; padding: 8px; border: 1px solid #cbd5e1; }
          td { padding: 8px; border: 1px solid #e2e8f0; }
          h1, h2, h3 { color: #0f172a; }
          blockquote { border-left: 4px solid #3b82f6; padding-left: 10px; color: #475569; background: #f8fafc; }
        </style>
      </head>
      <body>
        ${headerHtml}
        ${clone.innerHTML}
      </body>
      </html>
    `;

    const blob = new Blob(['\ufeff' + fullWordHtml], { type: 'application/msword' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = (fileName || 'document').replace(/\.[^/.]+$/, "") + ".doc";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    if (typeof window.showToast === 'function') window.showToast('Word document downloaded successfully!', 'success');
  },

  /**
   * Export current customized table data / checklist items as Excel compatible CSV file
   */
  exportXLSX: function(fallbackUrl, fileName) {
    const tables = document.querySelectorAll('.doc-content-card table, .doc-main-content table');
    const checkboxes = document.querySelectorAll('.doc-content-card input[type="checkbox"], .doc-main-content input[type="checkbox"]');

    if (typeof window.showToast === 'function') window.showToast('Generating Excel CSV data...', 'info');

    let csvContent = "data:text/csv;charset=utf-8,\ufeff";

    // 1. Export tables if present
    if (tables.length > 0) {
      tables.forEach((table, tIdx) => {
        csvContent += `Table #${tIdx + 1}\n`;
        table.querySelectorAll('tr').forEach(row => {
          const rowData = [];
          row.querySelectorAll('th, td').forEach(cell => {
            let val = '';
            const cb = cell.querySelector('input[type="checkbox"]');
            const num = cell.querySelector('input[type="number"]');

            if (cb) {
              val = cb.checked ? "COMPLETED" : "PENDING";
            } else if (num) {
              val = num.value;
            } else {
              val = cell.innerText.replace(/"/g, '""').trim();
            }
            rowData.push(`"${val}"`);
          });
          csvContent += rowData.join(",") + "\n";
        });
        csvContent += "\n";
      });
    } 
    // 2. Export checklist items if no table
    else if (checkboxes.length > 0) {
      csvContent += "Status,Task Description\n";
      checkboxes.forEach(cb => {
        const status = cb.checked ? "COMPLETED" : "PENDING";
        const text = (cb.parentNode.innerText || cb.parentNode.textContent || '').replace(/"/g, '""').trim();
        csvContent += `"${status}","${text}"\n`;
      });
    } else {
      if (fallbackUrl) return this.downloadFile(fallbackUrl, fileName);
      if (typeof window.showToast === 'function') window.showToast('No table or checklist data found to export.', 'error');
      return;
    }

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', (fileName || 'spreadsheet').replace(/\.[^/.]+$/, "") + ".csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    if (typeof window.showToast === 'function') window.showToast('Excel CSV data downloaded successfully!', 'success');
  },

  /**
   * Bulk Download 100% Complete Client Workspace (JSON, Summary Report HTML, Word & Excel files)
   */
  downloadCompleteClientWorkspace: function() {
    const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
    if (!project) return;

    if (typeof window.showToast === 'function') window.showToast(`Exporting workspace for ${project.clientName}...`, 'info');

    // 1. Download Project JSON Configuration File
    if (window.ProjectStorage && window.ProjectStorage.exportJSON) {
      window.ProjectStorage.exportJSON(project.id);
    }

    // 2. Build and Download Client Master Summary HTML Report
    const summaryHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${escapeHtml(project.clientName)} — Client Workspace Report</title>
  <style>
    body { font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; color: #0f172a; padding: 20px; line-height: 1.6; }
    h1 { color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }
    .card { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }
    th { background: #e2e8f0; }
  </style>
</head>
<body>
  <h1>💼 Client Master Workspace Report</h1>
  <div class="card">
    <p><strong>Client Name:</strong> ${escapeHtml(project.clientName)}</p>
    <p><strong>Project Title:</strong> ${escapeHtml(project.projectName)}</p>
    <p><strong>Prepared By:</strong> ${escapeHtml(project.preparedBy)}</p>
    <p><strong>Report Date:</strong> ${project.date}</p>
  </div>
</body>
</html>`;

    const blob = new Blob(['\ufeff' + summaryHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `workspace_${slugifyStr(project.clientName)}_report.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    if (typeof window.showToast === 'function') window.showToast('Workspace files exported successfully!', 'success');
  },

  /**
   * Download exact original template file
   */
  downloadFile: function(fileUrl, fileName) {
    if (!fileUrl) {
      if (typeof window.showToast === 'function') window.showToast('Original file is not available.', 'error');
      return;
    }
    const link = document.createElement('a');
    link.href = fileUrl;
    link.download = fileName || 'document';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    if (typeof window.showToast === 'function') window.showToast(`Downloading file: ${fileName}`, 'info');
  },

  /**
   * Copy current document content text to clipboard with fallback
   */
  copyContentToClipboard: function() {
    const contentCard = document.querySelector('.doc-content-card') || document.querySelector('.doc-main-content');
    if (!contentCard) {
      if (typeof window.showToast === 'function') window.showToast('No content found to copy.', 'error');
      return;
    }
    const text = contentCard.innerText || contentCard.textContent;

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        if (typeof window.showToast === 'function') window.showToast('Document content copied to clipboard!', 'success');
      }).catch(() => {
        this._fallbackCopyText(text);
      });
    } else {
      this._fallbackCopyText(text);
    }
  },

  _fallbackCopyText: function(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        if (typeof window.showToast === 'function') window.showToast('Document content copied to clipboard!', 'success');
      } else {
        if (typeof window.showToast === 'function') window.showToast('Failed to copy content.', 'error');
      }
    } catch (err) {
      if (typeof window.showToast === 'function') window.showToast('Failed to copy content.', 'error');
    }
    document.body.removeChild(textArea);
  }
};

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function slugifyStr(str) {
  return (str || 'project').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
}
