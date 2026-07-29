/**
 * Document Hub - Interactive JavaScript
 * Multi-Client Profile Switcher, Interactive Task Checklists, Multi-dimensional search, File Explorer Drawer, 
 * Section Scope Selector, TOC ScrollSpy, Sheet Tabs, and Live WYSIWYG Document Editor & Persistence Engine.
 */

document.addEventListener('DOMContentLoaded', () => {
  renderClientProfileSwitcher();
  initSearchAndFilter();
  initSheetTabs();
  initCopyButtons();
  initSectionScopeSelectors();
  initTocScrollSpy();
  initLiveDocumentEditor();
  initInteractiveTaskChecklists();
  if (window.SmartAssistant) window.SmartAssistant.updateHeaderApiKeyStatus();
});

/**
 * Render Interactive Multi-Client Profile Switcher Bar & Warning Notice
 */
function renderClientProfileSwitcher() {
  const container = document.getElementById('project-banner-container');
  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  if (!project || !container) return;

  container.innerHTML = `
    <div class="project-banner-card" style="padding: 0.75rem 1.5rem; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem;">
      <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; font-size: 0.9rem;">
        <span class="badge badge-docx">Active Client Workspace</span>
        <span style="color: var(--text-main); font-weight: 600;">Client: <span style="font-weight: 700; color: var(--accent-indigo);">${escapeHtml(project.clientName)}</span></span>
        <span style="color: var(--text-light);">|</span>
        <span style="color: var(--text-muted);">Project: <strong>${escapeHtml(project.projectName)}</strong></span>
        <span style="color: var(--text-light);">|</span>
        <span style="color: var(--text-muted);">Platform: <strong>${project.platform} Platform</strong></span>
        <span style="color: var(--text-light);">|</span>
        <span style="color: var(--text-muted);">Complexity: <strong>${project.complexity}x</strong></span>
        <span style="color: var(--text-light);">|</span>
        <span style="color: var(--text-muted);">Discount: <strong>${project.discount || 0}%</strong></span>
      </div>
      <div style="display: flex; align-items: center; gap: 0.5rem;">
        <button class="export-btn" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" onclick="openProjectProfileModal()">✏️ Edit Profile</button>
        <button class="export-btn" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" onclick="openProjectManagerModal()">📁 Switch Client</button>
      </div>
    </div>
  `;
}

function switchClientProfile(id) {
  if (window.ProjectStorage) {
    window.ProjectStorage.setActiveProjectId(id);
    if (window.showToast) window.showToast('Switched active client profile!', 'info');
    setTimeout(() => location.reload(), 300);
  }
}

function promptNewClientProfile() {
  const clientName = prompt('Enter New Client Name:', 'Beta Corp');
  if (!clientName) return;
  const projectName = prompt('Enter Project Scope Title:', 'Mobile App Development');
  if (window.ProjectStorage) {
    window.ProjectStorage.createClientProfile(clientName, projectName);
    if (window.showToast) window.showToast(`Created new client profile for ${clientName}!`, 'success');
    setTimeout(() => location.reload(), 400);
  }
}

function deleteCurrentClientProfile() {
  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  if (!project) return;
  if (!confirm(`Are you sure you want to delete client profile "${project.clientName}"?`)) return;

  if (window.ProjectStorage.deleteClientProfile(project.id)) {
    if (window.showToast) window.showToast('Client profile deleted.', 'info');
    setTimeout(() => location.reload(), 400);
  }
}

function updateClientInfo(field, val) {
  if (window.ProjectStorage) {
    const proj = window.ProjectStorage.getProject();
    proj[field] = val;
    window.ProjectStorage.saveProject(proj);
    if (window.showToast) window.showToast('Updated client profile details!', 'info');
  }
}

/**
 * Handle interactive task checkboxes in Markdown files (Checklists & Questionnaires)
 */
function initInteractiveTaskChecklists() {
  const checkboxes = document.querySelectorAll('.interactive-checklist-item, .rendered-markdown input[type="checkbox"]');
  if (!checkboxes.length) return;

  const pageSlug = getPageSlug();
  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  const savedChecklist = project ? (project.checklists[pageSlug] || {}) : {};

  let totalCount = checkboxes.length;
  let checkedCount = 0;

  checkboxes.forEach((cb, idx) => {
    const cbId = cb.getAttribute('data-cb-id') || `cb-${idx}`;
    cb.setAttribute('data-cb-id', cbId);

    // Restore saved state
    if (savedChecklist[cbId]) {
      cb.checked = true;
      checkedCount++;
    } else if (cb.checked) {
      checkedCount++;
    }

    // Toggle click listener
    cb.addEventListener('change', () => {
      const isChecked = cb.checked;

      if (window.ProjectStorage) {
        const curProj = window.ProjectStorage.getProject();
        if (!curProj.checklists[pageSlug]) curProj.checklists[pageSlug] = {};
        curProj.checklists[pageSlug][cbId] = isChecked;
        window.ProjectStorage.saveProject(curProj);
      }

      updateChecklistProgressBar();
    });
  });

  updateChecklistProgressBar();

  function updateChecklistProgressBar() {
    let currentChecked = 0;
    checkboxes.forEach(cb => {
      if (cb.checked) currentChecked++;
    });

    const percent = Math.round((currentChecked / totalCount) * 100) || 0;
    const textEl = document.getElementById('checklist-progress-text');
    const barEl = document.getElementById('checklist-progress-bar');

    if (textEl) textEl.textContent = `${currentChecked} of ${totalCount} completed (${percent}%)`;
    if (barEl) barEl.style.width = `${percent}%`;
  }
}

/**
 * Filter document cards on main dashboard
 */
function initSearchAndFilter() {
  const searchInput = document.getElementById('search-input');
  const typeFilterBtns = document.querySelectorAll('.type-filter');
  const topicFilterBtns = document.querySelectorAll('.topic-filter');
  const docCards = document.querySelectorAll('.doc-card');
  const visibleCountEl = document.getElementById('visible-count');
  const noResultsEl = document.getElementById('no-results');

  let currentType = 'all';
  let currentTopic = 'all';
  let currentQuery = '';

  function filterCards() {
    let visibleCount = 0;

    docCards.forEach(card => {
      const type = card.getAttribute('data-type') || '';
      const topics = (card.getAttribute('data-topics') || '').split(' ');
      const title = card.getAttribute('data-title') || '';
      const text = card.textContent.toLowerCase();

      const matchesType = (currentType === 'all') || (type === currentType);
      const matchesTopic = (currentTopic === 'all') || topics.includes(currentTopic);
      const matchesQuery = !currentQuery || title.toLowerCase().includes(currentQuery) || text.includes(currentQuery);

      if (matchesType && matchesTopic && matchesQuery) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (visibleCountEl) visibleCountEl.textContent = visibleCount;
    if (noResultsEl) noResultsEl.style.display = (visibleCount === 0) ? 'block' : 'none';
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentQuery = e.target.value.trim().toLowerCase();
      filterCards();
    });
  }

  typeFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      typeFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentType = btn.getAttribute('data-filter') || 'all';
      filterCards();
    });
  });

  topicFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      topicFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTopic = btn.getAttribute('data-topic') || 'all';
      filterCards();
    });
  });
}

/**
 * Live WYSIWYG Document Content Editor & LocalStorage Persistence Engine
 */
function initLiveDocumentEditor() {
  const contentCard = document.querySelector('.doc-content-card');
  const exportToolbar = document.querySelector('.export-toolbar');
  if (!contentCard || !exportToolbar) return;

  const pageSlug = getPageSlug();
  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  const storageKey = `edited_doc_${project ? project.id : 'default'}_${pageSlug}`;

  // Restore saved edits if present in localStorage
  const savedHtml = localStorage.getItem(storageKey);
  if (savedHtml) {
    contentCard.innerHTML = savedHtml;
    if (window.showToast) window.showToast('Loaded your saved proposal edits!', 'info');
  }

  // Inject Edit, Save, and Reset buttons into export toolbar
  const editBtnHtml = `
    <button id="toggle-edit-mode-btn" class="export-btn" style="background: rgba(245, 158, 11, 0.12); border-color: var(--accent-amber); color: #d97706; font-weight: 700;" onclick="toggleLiveEditMode()">
      ✏️ Edit Proposal / Document
    </button>
    <button id="save-doc-edit-btn" class="export-btn primary" style="display: none; background: var(--accent-emerald); border-color: var(--accent-emerald);" onclick="saveDocumentEdits()">
      💾 Save Changes
    </button>
    <button id="reset-doc-edit-btn" class="export-btn" style="display: none; background: rgba(239, 68, 68, 0.1); border-color: #ef4444; color: #ef4444;" onclick="resetDocumentEdits()">
      ↩️ Reset Original
    </button>
  `;

  exportToolbar.insertAdjacentHTML('beforeend', editBtnHtml);
}

let isEditModeActive = false;

function toggleLiveEditMode() {
  const contentCard = document.querySelector('.doc-content-card');
  const toggleBtn = document.getElementById('toggle-edit-mode-btn');
  const saveBtn = document.getElementById('save-doc-edit-btn');
  const resetBtn = document.getElementById('reset-doc-edit-btn');

  if (!contentCard) return;

  isEditModeActive = !isEditModeActive;

  if (isEditModeActive) {
    contentCard.setAttribute('contenteditable', 'true');
    contentCard.style.outline = '2px dashed var(--accent-amber)';
    contentCard.style.borderRadius = 'var(--radius-lg)';

    toggleBtn.textContent = '⏸ Pause Editing';
    saveBtn.style.display = 'inline-flex';
    resetBtn.style.display = 'inline-flex';

    if (!document.getElementById('edit-mode-banner')) {
      const bannerHtml = `
        <div id="edit-mode-banner" contenteditable="false" style="background: rgba(245, 158, 11, 0.15); border: 1px solid var(--accent-amber); color: var(--text-main); padding: 0.85rem 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; justify-content: space-between; user-select: none;">
          <span>✏️ Live Edit Mode Active — Click any text, heading, pricing table cell, or section on this page to edit directly!</span>
          <button class="export-btn primary" style="padding: 0.35rem 0.85rem; font-size: 0.8rem; background: var(--accent-emerald); border-color: var(--accent-emerald);" onclick="saveDocumentEdits()">💾 Save Changes</button>
        </div>
      `;
      contentCard.insertAdjacentHTML('afterbegin', bannerHtml);
    }

    if (window.showToast) window.showToast('Live Edit Mode enabled! Click any text to edit.', 'info');
  } else {
    disableLiveEditMode();
  }
}

function disableLiveEditMode() {
  const contentCard = document.querySelector('.doc-content-card');
  const toggleBtn = document.getElementById('toggle-edit-mode-btn');
  const saveBtn = document.getElementById('save-doc-edit-btn');
  const resetBtn = document.getElementById('reset-doc-edit-btn');
  const banner = document.getElementById('edit-mode-banner');

  if (!contentCard) return;

  isEditModeActive = false;
  contentCard.removeAttribute('contenteditable');
  contentCard.style.outline = 'none';

  if (banner) banner.remove();
  if (toggleBtn) toggleBtn.textContent = '✏️ Edit Proposal / Document';
  if (saveBtn) saveBtn.style.display = 'none';
  if (resetBtn) resetBtn.style.display = 'none';
}

function saveDocumentEdits() {
  const contentCard = document.querySelector('.doc-content-card');
  if (!contentCard) return;

  const banner = document.getElementById('edit-mode-banner');
  if (banner) banner.remove();

  const pageSlug = getPageSlug();
  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  const storageKey = `edited_doc_${project ? project.id : 'default'}_${pageSlug}`;

  localStorage.setItem(storageKey, contentCard.innerHTML);

  disableLiveEditMode();
  if (window.showToast) window.showToast('Document edits saved successfully! Ready to export PDF/Word/Excel.', 'success');
}

function resetDocumentEdits() {
  if (!confirm('Are you sure you want to reset this proposal to its original template text? Custom changes will be lost.')) return;

  const pageSlug = getPageSlug();
  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  const storageKey = `edited_doc_${project ? project.id : 'default'}_${pageSlug}`;

  localStorage.removeItem(storageKey);
  window.location.reload();
}

/**
 * Handle section scope selection toggles in Markdown guides
 */
function initSectionScopeSelectors() {
  const scopeBtns = document.querySelectorAll('.section-scope-btn');
  if (!scopeBtns.length) return;

  const project = window.ProjectStorage ? window.ProjectStorage.getProject() : null;
  const pageSlug = getPageSlug();
  const savedSections = project ? (project.questionnaires[pageSlug] || {}) : {};

  scopeBtns.forEach(btn => {
    const secId = btn.getAttribute('data-sec-id');
    if (savedSections[secId]) {
      btn.classList.add('selected');
      btn.textContent = '✓ Added to Scope';
    }

    btn.addEventListener('click', () => {
      const isSel = btn.classList.toggle('selected');
      btn.textContent = isSel ? '✓ Added to Scope' : '+ Add to Scope';

      if (window.ProjectStorage) {
        const curProj = window.ProjectStorage.getProject();
        if (!curProj.questionnaires[pageSlug]) curProj.questionnaires[pageSlug] = {};
        curProj.questionnaires[pageSlug][secId] = isSel;
        window.ProjectStorage.saveProject(curProj);
        if (window.showToast) {
          window.showToast(isSel ? 'Section added to client project scope!' : 'Section removed from scope.', 'info');
        }
      }
    });
  });
}

/**
 * TOC ScrollSpy - Highlight active section link as user scrolls
 */
function initTocScrollSpy() {
  const tocLinks = document.querySelectorAll('.doc-sidebar-toc a');
  if (!tocLinks.length) return;

  const headings = Array.from(tocLinks).map(link => {
    const id = link.getAttribute('href').replace('#', '');
    return document.getElementById(id);
  }).filter(Boolean);

  window.addEventListener('scroll', () => {
    let currentId = '';
    const scrollPos = window.scrollY + 120;

    headings.forEach(heading => {
      if (heading.offsetTop <= scrollPos) {
        currentId = heading.id;
      }
    });

    tocLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  });
}

/**
 * Handle Excel sheet tab switching
 */
function initSheetTabs() {
  const sheetBtns = document.querySelectorAll('.sheet-tab-btn');

  sheetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-sheet-target');
      const container = btn.closest('.excel-viewer') || document;

      container.querySelectorAll('.sheet-tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.sheet-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

/**
 * Copy code button
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
          if (window.showToast) window.showToast('Code copied to clipboard!');
        });
      });
      pre.appendChild(btn);
    }
  });
}

/**
 * File Explorer Modal Drawer - Browse and open primary tools
 */
function openFileExplorerModal() {
  const isPage = window.location.pathname.includes('/pages/');
  const prefix = isPage ? '' : 'pages/';

  const docs = [
    { title: "Application Pricing Calculator (Interactive)", slug: "template-excel-template-application-pricing-calculator", type: "XLSX" },
    { title: "Website Pricing Calculator (Interactive)", slug: "template-excel-template-website-pricing-calculator", type: "XLSX" },
    { title: "Application Client Questionnaire", slug: "questionnaire-application-application-client-questionnaire", type: "MD" },
    { title: "Website Client Questionnaire", slug: "questionnaire-website-website-client-questionnaire", type: "MD" },
    { title: "Application Client Proposal", slug: "template-word-template-application-client-proposal", type: "DOCX" },
    { title: "Website Client Proposal", slug: "template-word-template-website-client-proposal", type: "DOCX" },
    { title: "Application Project Checklist", slug: "checklists-application-project-checklist", type: "MD" },
    { title: "Website Project Checklist", slug: "checklists-website-project-checklist", type: "MD" },
    { title: "Application Requirements Complete Guide", slug: "docs-application-application-requirements-complete-guide", type: "MD" },
    { title: "Website Requirements Complete Guide", slug: "docs-website-website-requirements-complete-guide", type: "MD" },
    { title: "Repository Toolkit Guide", slug: "readme", type: "MD" }
  ];

  let listHtml = '';
  docs.forEach(d => {
    listHtml += `
      <a href="${prefix}${d.slug}.html" class="explorer-item">
        <span style="font-weight: 600;">${escapeHtml(d.title)}</span>
        <span class="badge badge-md">${d.type}</span>
      </a>
    `;
  });

  const modalHtml = `
    <div id="file-explorer-overlay" class="modal-overlay">
      <div class="modal-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h3>📁 File Explorer — Primary Tools</h3>
          <button class="export-btn" onclick="closeFileExplorerModal()">✕ Close</button>
        </div>
        <div class="search-box" style="margin-bottom: 1rem;">
          <input type="text" id="explorer-search" class="search-input" placeholder="Search primary tools..." oninput="filterExplorerItems(this.value)">
        </div>
        <div class="explorer-list" id="explorer-list">
          ${listHtml}
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closeFileExplorerModal() {
  document.getElementById('file-explorer-overlay')?.remove();
}

function filterExplorerItems(query) {
  const items = document.querySelectorAll('.explorer-item');
  const q = query.toLowerCase().trim();
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = (!q || text.includes(q)) ? 'flex' : 'none';
  });
}

function getPageSlug() {
  const path = window.location.pathname;
  return path.split('/').pop().replace('.html', '') || 'index';
}

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function handleBannerImportFile(evt) {
  const file = evt.target.files[0];
  if (file && window.ProjectStorage) {
    const reader = new FileReader();
    reader.onload = function(e) {
      window.ProjectStorage.importJSON(e.target.result);
    };
    reader.readAsText(file);
  }
}

window.openFileExplorerModal = openFileExplorerModal;
window.closeFileExplorerModal = closeFileExplorerModal;
window.filterExplorerItems = filterExplorerItems;
window.toggleLiveEditMode = toggleLiveEditMode;
window.disableLiveEditMode = disableLiveEditMode;
window.saveDocumentEdits = saveDocumentEdits;
window.resetDocumentEdits = resetDocumentEdits;
window.switchClientProfile = switchClientProfile;
window.promptNewClientProfile = promptNewClientProfile;
window.deleteCurrentClientProfile = deleteCurrentClientProfile;
window.updateClientInfo = updateClientInfo;
window.handleBannerImportFile = handleBannerImportFile;

/**
 * Global Toast Notification Manager
 */
window.showToast = function(message, type = 'info') {
  let container = document.getElementById('toast-notification-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-notification-container';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '999999';
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    container.style.gap = '10px';
    container.style.pointerEvents = 'none';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.style.pointerEvents = 'auto';
  toast.style.padding = '12px 20px';
  toast.style.borderRadius = '10px';
  toast.style.fontFamily = 'var(--font-sans, sans-serif)';
  toast.style.fontSize = '0.9rem';
  toast.style.fontWeight = '600';
  toast.style.color = '#ffffff';
  toast.style.boxShadow = '0 10px 25px rgba(0,0,0,0.2)';
  toast.style.transition = 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)';
  toast.style.transform = 'translateY(-10px)';
  toast.style.opacity = '0';

  if (type === 'success') {
    toast.style.background = 'linear-gradient(135deg, #059669, #10b981)';
    toast.innerHTML = `✓ ${message}`;
  } else if (type === 'error') {
    toast.style.background = 'linear-gradient(135deg, #dc2626, #ef4444)';
    toast.innerHTML = `✕ ${message}`;
  } else {
    toast.style.background = 'linear-gradient(135deg, #1e293b, #334155)';
    toast.innerHTML = `ℹ ${message}`;
  }

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';
  });

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }, 3500);
};
