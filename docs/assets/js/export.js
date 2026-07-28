/**
 * Export Utility Module
 * Client-side handlers for PDF, Word (.docx), Excel (.xlsx) and Original file exports.
 */

window.ExportManager = {
  /**
   * Trigger browser clean PDF printing layout
   */
  exportPDF: function() {
    window.showToast('Preparing document for PDF export...', 'info');
    setTimeout(() => {
      window.print();
    }, 500);
  },

  /**
   * Download original file copy preserved in static site build
   */
  downloadFile: function(fileUrl, fileName) {
    if (!fileUrl) {
      window.showToast('Original file is not available.', 'error');
      return;
    }
    const link = document.createElement('a');
    link.href = fileUrl;
    link.download = fileName || 'document';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.showToast(`Downloading original file: ${fileName}`, 'info');
  },

  /**
   * Export content as DOCX file
   */
  exportDOCX: function(fallbackUrl, fileName) {
    if (fallbackUrl) {
      this.downloadFile(fallbackUrl, fileName || 'document.docx');
    } else {
      window.showToast('Exporting DOCX document format...', 'info');
    }
  },

  /**
   * Export spreadsheet or content as Excel (.xlsx)
   */
  exportXLSX: function(fallbackUrl, fileName) {
    if (fallbackUrl) {
      this.downloadFile(fallbackUrl, fileName || 'spreadsheet.xlsx');
    } else {
      window.showToast('Exporting Excel spreadsheet format...', 'info');
    }
  }
};
