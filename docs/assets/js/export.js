/**
 * Enhanced Export Utility Module
 * Supports client-side customized exports for PDF, Word (.doc/.docx), Excel (.csv/.xlsx), and JSON.
 * Captures user-selected checkboxes, custom unit rates, quantities, and client project metadata.
 */

window.ExportManager = {
  /**
   * Trigger clean browser PDF print layout capturing live user inputs
   */
  exportPDF: function() {
    const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
    const clientTitle = project ? `${project.projectName} - ${project.clientName}` : document.title;
    
    window.showToast('Preparing customized document for PDF export...', 'info');

    // Temporarily set document title for clean browser PDF filename
    const origTitle = document.title;
    document.title = clientTitle;

    setTimeout(() => {
      window.print();
      document.title = origTitle;
    }, 400);
  },

  /**
   * Export current customized page state (with checked items & inputs) as Word document
   */
  exportDOCX: function(fallbackUrl, fileName) {
    const contentCard = document.querySelector('.doc-content-card');
    const headerCard = document.querySelector('.doc-header-card');

    if (!contentCard) {
      if (fallbackUrl) return this.downloadFile(fallbackUrl, fileName);
      return window.showToast('Unable to capture document content.', 'error');
    }

    window.showToast('Generating customized Word document with your selections...', 'info');

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

    const headerHtml = headerCard ? `
      <div style="border-bottom: 2px solid #0f172a; padding-bottom: 15px; margin-bottom: 25px;">
        <h1 style="font-family: Arial, sans-serif; color: #0f172a;">${project ? escapeHtml(project.projectName) : 'Client Project Scope'}</h1>
        <p style="color: #475569; font-size: 14px;">
          <strong>Client:</strong> ${project ? escapeHtml(project.clientName) : 'N/A'} | 
          <strong>Prepared By:</strong> ${project ? escapeHtml(project.preparedBy) : 'Agency'} | 
          <strong>Date:</strong> ${new Date().toLocaleDateString()}
        </p>
      </div>
    ` : '';

    const fullWordHtml = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
        <meta charset='utf-8'>
        <title>Document Export</title>
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; color: #0f172a; line-height: 1.6; }
          table { width: 100%; border-collapse: collapse; margin: 15px 0; }
          th { background: #f1f5f9; color: #0f172a; font-weight: bold; padding: 8px; border: 1px solid #cbd5e1; }
          td { padding: 8px; border: 1px solid #e2e8f0; }
          h1, h2, h3 { color: #0f172a; }
          blockquote { border-left: 4px solid #3b82f6; padding-left: 10px; color: #475569; }
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
    link.download = (fileName || 'custom_document').replace(/\.[^/.]+$/, "") + "_customized.doc";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    window.showToast('Customized Word document downloaded successfully!', 'success');
  },

  /**
   * Export current customized table data / checklist items as Excel compatible CSV file
   */
  exportXLSX: function(fallbackUrl, fileName) {
    const tables = document.querySelectorAll('.doc-content-card table');
    const checkboxes = document.querySelectorAll('.doc-content-card input[type="checkbox"]');

    window.showToast('Generating customized Excel spreadsheet data...', 'info');

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
      return window.showToast('No table or checklist data found to export.', 'error');
    }

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', (fileName || 'custom_spreadsheet').replace(/\.[^/.]+$/, "") + "_customized.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    window.showToast('Customized Excel data downloaded successfully!', 'success');
  },

  /**
   * Download exact original template file
   */
  downloadFile: function(fileUrl, fileName) {
    if (!fileUrl) {
      window.showToast('Original template file is not available.', 'error');
      return;
    }
    const link = document.createElement('a');
    link.href = fileUrl;
    link.download = fileName || 'document';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.showToast(`Downloading original file: ${fileName}`, 'info');
  }
};

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
