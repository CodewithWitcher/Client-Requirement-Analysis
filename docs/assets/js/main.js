/**
 * Document Hub - Interactive JavaScript
 * Multi-dimensional search, File Explorer Drawer, Section Scope Selector, TOC ScrollSpy, and Sheet Tabs.
 */

document.addEventListener('DOMContentLoaded', () => {
  initSearchAndFilter();
  initSheetTabs();
  initCopyButtons();
  initSectionScopeSelectors();
  initTocScrollSpy();
});

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

window.openFileExplorerModal = openFileExplorerModal;
window.closeFileExplorerModal = closeFileExplorerModal;
window.filterExplorerItems = filterExplorerItems;
