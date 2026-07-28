/**
 * Document Hub - Interactive JavaScript
 * Handlers for search, file-type filtering, sheet tabs, and toast notifications.
 */

document.addEventListener('DOMContentLoaded', () => {
  initSearchAndFilter();
  initSheetTabs();
  initCopyButtons();
});

/**
 * Filter document cards by search query and type badges
 */
function initSearchAndFilter() {
  const searchInput = document.getElementById('search-input');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const docCards = document.querySelectorAll('.doc-card');
  const visibleCountEl = document.getElementById('visible-count');
  const noResultsEl = document.getElementById('no-results');

  let currentCategory = 'all';
  let currentQuery = '';

  function filterCards() {
    let visibleCount = 0;

    docCards.forEach(card => {
      const type = card.getAttribute('data-type');
      const title = card.getAttribute('data-title') || '';
      const text = card.textContent.toLowerCase();

      const matchesCategory = (currentCategory === 'all') || (type === currentCategory);
      const matchesQuery = !currentQuery || title.toLowerCase().includes(currentQuery) || text.includes(currentQuery);

      if (matchesCategory && matchesQuery) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (visibleCountEl) {
      visibleCountEl.textContent = visibleCount;
    }

    if (noResultsEl) {
      noResultsEl.style.display = (visibleCount === 0) ? 'block' : 'none';
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentQuery = e.target.value.trim().toLowerCase();
      filterCards();
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      currentCategory = btn.getAttribute('data-filter') || 'all';
      filterCards();
    });
  });
}

/**
 * Handle multi-sheet tab switching for Excel table previews
 */
function initSheetTabs() {
  const sheetBtns = document.querySelectorAll('.sheet-tab-btn');

  sheetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-sheet-target');
      const container = btn.closest('.doc-content-card') || document;

      // Deactivate siblings
      container.querySelectorAll('.sheet-tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.sheet-pane').forEach(p => p.classList.remove('active'));

      // Activate selected
      btn.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
}

/**
 * Copy code snippet buttons
 */
function initCopyButtons() {
  document.querySelectorAll('pre code').forEach((codeBlock) => {
    const pre = codeBlock.parentNode;
    if (pre && !pre.querySelector('.copy-code-btn')) {
      const btn = document.createElement('button');
      btn.className = 'copy-code-btn';
      btn.textContent = 'Copy';
      btn.style.cssText = 'position: absolute; right: 10px; top: 10px; background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; cursor: pointer;';
      pre.style.position = 'relative';

      btn.addEventListener('click', () => {
        navigator.clipboard.writeText(codeBlock.textContent).then(() => {
          showToast('Code copied to clipboard!');
        });
      });
      pre.appendChild(btn);
    }
  });
}

/**
 * Display toast notification message
 */
function showToast(message, type = 'info') {
  let toastContainer = document.querySelector('.toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>
    <span>${message}</span>
  `;

  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(20px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

window.showToast = showToast;
