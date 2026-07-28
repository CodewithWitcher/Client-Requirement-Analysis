/**
 * Interactive Pricing Calculator & Checklist Controller
 * Handles live pricing computations, item toggles, custom client details, and auto-saving.
 */

document.addEventListener('DOMContentLoaded', () => {
  initProjectBanner();
  initCalculatorListeners();
  initChecklistListeners();
});

/**
 * Render active client banner & metadata form inputs
 */
function initProjectBanner() {
  const bannerContainer = document.getElementById('project-banner-container');
  if (!bannerContainer) return;

  const project = window.ProjectStorage.getProject();

  bannerContainer.innerHTML = `
    <div class="project-banner-card">
      <div class="banner-title-row">
        <div>
          <span class="badge badge-docx">Interactive Client Workspace</span>
          <h2 style="margin-top: 0.25rem;">${escapeHtml(project.projectName)}</h2>
        </div>
        <div class="banner-actions">
          <button class="export-btn" onclick="openProjectManagerModal()">📁 Switch / New Project</button>
          <button class="export-btn primary" onclick="ProjectStorage.exportJSON()">💾 Backup Project (JSON)</button>
        </div>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label>Client Name</label>
          <input type="text" id="client-name-input" class="form-control" value="${escapeHtml(project.clientName)}" placeholder="e.g. Acme Enterprises">
        </div>
        <div class="form-group">
          <label>Project Title</label>
          <input type="text" id="project-name-input" class="form-control" value="${escapeHtml(project.projectName)}" placeholder="e.g. Mobile E-Commerce App">
        </div>
        <div class="form-group">
          <label>Prepared By</label>
          <input type="text" id="prepared-by-input" class="form-control" value="${escapeHtml(project.preparedBy)}" placeholder="e.g. Witcher Tech Studio">
        </div>
        <div class="form-group">
          <label>Platform Target</label>
          <select id="platform-select" class="form-control">
            <option value="Single" ${project.platform === 'Single' ? 'selected' : ''}>Single Platform (Android or iOS / Web)</option>
            <option value="Both" ${project.platform === 'Both' ? 'selected' : ''}>Both Platforms (Android + iOS / Cross-Platform)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Complexity Multiplier</label>
          <select id="complexity-select" class="form-control">
            <option value="1.0" ${project.complexity === '1.0' ? 'selected' : ''}>1.0x — Standard / Simple</option>
            <option value="1.3" ${project.complexity === '1.3' ? 'selected' : ''}>1.3x — Medium Complexity</option>
            <option value="1.5" ${project.complexity === '1.5' ? 'selected' : ''}>1.5x — High Complexity</option>
            <option value="2.0" ${project.complexity === '2.0' ? 'selected' : ''}>2.0x — Enterprise Level</option>
          </select>
        </div>
        <div class="form-group">
          <label>Discount (%)</label>
          <input type="number" id="discount-input" class="form-control" min="0" max="50" value="${project.discount || 0}">
        </div>
      </div>
    </div>
  `;

  // Bind project level form changes
  const inputs = ['client-name-input', 'project-name-input', 'prepared-by-input', 'platform-select', 'complexity-select', 'discount-input'];
  inputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', updateProjectMetadata);
      el.addEventListener('input', updateProjectMetadata);
    }
  });
}

function updateProjectMetadata() {
  const project = window.ProjectStorage.getProject();
  project.clientName = document.getElementById('client-name-input')?.value || 'Client';
  project.projectName = document.getElementById('project-name-input')?.value || 'Project';
  project.preparedBy = document.getElementById('prepared-by-input')?.value || 'Agency';
  project.platform = document.getElementById('platform-select')?.value || 'Both';
  project.complexity = document.getElementById('complexity-select')?.value || '1.0';
  project.discount = parseFloat(document.getElementById('discount-input')?.value || 0);

  window.ProjectStorage.saveProject(project);
  recalculatePriceTotals();
}

/**
 * Initialize interactive listeners on tables with pricing items
 */
function initCalculatorListeners() {
  const calcTables = document.querySelectorAll('.interactive-calc-table');
  if (!calcTables.length) return;

  const project = window.ProjectStorage.getProject();
  const pageSlug = getPageSlug();
  const savedState = project.calculators[pageSlug] || {};

  calcTables.forEach(table => {
    const rows = table.querySelectorAll('tr[data-item-id]');
    rows.forEach(row => {
      const itemId = row.getAttribute('data-item-id');
      const checkInput = row.querySelector('.item-check');
      const costInput = row.querySelector('.item-cost');
      const qtyInput = row.querySelector('.item-qty');

      // Restore saved state if exists
      if (savedState[itemId]) {
        if (checkInput) checkInput.checked = savedState[itemId].checked;
        if (costInput) costInput.value = savedState[itemId].cost;
        if (qtyInput) qtyInput.value = savedState[itemId].qty;
      }

      // Attach recalculation event listeners
      [checkInput, costInput, qtyInput].forEach(input => {
        if (input) {
          input.addEventListener('change', () => handleItemChange(table, pageSlug));
          input.addEventListener('input', () => handleItemChange(table, pageSlug));
        }
      });
    });
  });

  recalculatePriceTotals();
}

function handleItemChange(table, pageSlug) {
  const project = window.ProjectStorage.getProject();
  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }

  const rows = table.querySelectorAll('tr[data-item-id]');
  rows.forEach(row => {
    const itemId = row.getAttribute('data-item-id');
    const checkInput = row.querySelector('.item-check');
    const costInput = row.querySelector('.item-cost');
    const qtyInput = row.querySelector('.item-qty');
    const rowTotalCell = row.querySelector('.item-row-total');

    const isChecked = checkInput ? checkInput.checked : true;
    const cost = parseFloat(costInput ? costInput.value : 0) || 0;
    const qty = parseFloat(qtyInput ? qtyInput.value : 1) || 1;
    const lineTotal = isChecked ? (cost * qty) : 0;

    if (rowTotalCell) {
      rowTotalCell.textContent = '₹' + lineTotal.toLocaleString('en-IN');
      rowTotalCell.style.opacity = isChecked ? '1' : '0.4';
    }

    project.calculators[pageSlug][itemId] = {
      checked: isChecked,
      cost: cost,
      qty: qty,
      total: lineTotal
    };
  });

  window.ProjectStorage.saveProject(project);
  recalculatePriceTotals();
}

/**
 * Calculate grand totals, taxes, multipliers, and payment milestones
 */
function recalculatePriceTotals() {
  const project = window.ProjectStorage.getProject();
  let subtotal = 0;

  // Sum up line totals across all calculator sheets
  Object.values(project.calculators || {}).forEach(sheetState => {
    Object.values(sheetState).forEach(item => {
      if (item.checked) {
        subtotal += (item.total || 0);
      }
    });
  });

  const platformMult = (project.platform === 'Both') ? 1.4 : 1.0;
  const complexityMult = parseFloat(project.complexity || 1.0);
  const adjustedSubtotal = Math.round(subtotal * platformMult * complexityMult);

  const discountAmount = Math.round(adjustedSubtotal * ((project.discount || 0) / 100));
  const discountedSubtotal = adjustedSubtotal - discountAmount;

  const gstAmount = Math.round(discountedSubtotal * 0.18);
  const grandTotal = discountedSubtotal + gstAmount;

  // Update summary widgets on page if present
  updateSummaryWidget('summary-subtotal', '₹' + subtotal.toLocaleString('en-IN'));
  updateSummaryWidget('summary-adjusted', '₹' + adjustedSubtotal.toLocaleString('en-IN'));
  updateSummaryWidget('summary-discount', '-₹' + discountAmount.toLocaleString('en-IN'));
  updateSummaryWidget('summary-gst', '₹' + gstAmount.toLocaleString('en-IN'));
  updateSummaryWidget('summary-grandtotal', '₹' + grandTotal.toLocaleString('en-IN'));

  // Update Milestones
  updateSummaryWidget('milestone-advance', '₹' + Math.round(grandTotal * 0.35).toLocaleString('en-IN'));
  updateSummaryWidget('milestone-design', '₹' + Math.round(grandTotal * 0.20).toLocaleString('en-IN'));
  updateSummaryWidget('milestone-dev', '₹' + Math.round(grandTotal * 0.30).toLocaleString('en-IN'));
  updateSummaryWidget('milestone-handover', '₹' + Math.round(grandTotal * 0.15).toLocaleString('en-IN'));
}

function updateSummaryWidget(elementId, formattedValue) {
  const el = document.getElementById(elementId);
  if (el) el.textContent = formattedValue;
}

/**
 * Handle interactive checkboxes on Checklist documents
 */
function initChecklistListeners() {
  const checkboxes = document.querySelectorAll('.interactive-checklist-item');
  if (!checkboxes.length) return;

  const project = window.ProjectStorage.getProject();
  const pageSlug = getPageSlug();
  const savedChecklist = project.checklists[pageSlug] || {};

  checkboxes.forEach((cb, index) => {
    const cbId = cb.getAttribute('data-cb-id') || `cb-${index}`;
    if (savedChecklist[cbId] !== undefined) {
      cb.checked = savedChecklist[cbId];
    }

    cb.addEventListener('change', () => {
      if (!project.checklists[pageSlug]) project.checklists[pageSlug] = {};
      project.checklists[pageSlug][cbId] = cb.checked;
      window.ProjectStorage.saveProject(project);
      updateChecklistProgressBar();
    });
  });

  updateChecklistProgressBar();
}

function updateChecklistProgressBar() {
  const checkboxes = document.querySelectorAll('.interactive-checklist-item');
  if (!checkboxes.length) return;

  const total = checkboxes.length;
  let checkedCount = 0;
  checkboxes.forEach(cb => { if (cb.checked) checkedCount++; });

  const pct = Math.round((checkedCount / total) * 100);

  let bar = document.getElementById('checklist-progress-bar');
  let text = document.getElementById('checklist-progress-text');

  if (bar) bar.style.width = pct + '%';
  if (text) text.textContent = `${checkedCount} of ${total} items completed (${pct}%)`;
}

function getPageSlug() {
  const path = window.location.pathname;
  return path.split('/').pop().replace('.html', '') || 'index';
}

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/**
 * Project Switcher Modal
 */
function openProjectManagerModal() {
  const projects = window.ProjectStorage.getAllProjects();
  const activeId = window.ProjectStorage.getActiveProjectId();

  let optionsHtml = '';
  Object.values(projects).forEach(p => {
    const isSelected = p.id === activeId ? 'selected' : '';
    optionsHtml += `<option value="${p.id}" ${isSelected}>${escapeHtml(p.projectName)} (${escapeHtml(p.clientName)})</option>`;
  });

  const modalHtml = `
    <div id="project-modal-overlay" class="modal-overlay">
      <div class="modal-card">
        <h3>📁 Switch or Create Client Project</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">Select an existing saved client project or start a new one.</p>
        
        <div class="form-group">
          <label>Select Project</label>
          <select id="modal-project-select" class="form-control">
            ${optionsHtml}
          </select>
        </div>

        <div style="display: flex; gap: 0.5rem; margin-top: 1.5rem; justify-content: flex-end;">
          <button class="export-btn" onclick="createNewProjectPrompt()">+ New Project</button>
          <button class="export-btn primary" onclick="confirmSwitchProject()">Load Selected</button>
          <button class="export-btn" onclick="closeProjectModal()">Cancel</button>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closeProjectModal() {
  document.getElementById('project-modal-overlay')?.remove();
}

function confirmSwitchProject() {
  const sel = document.getElementById('modal-project-select');
  if (sel) {
    window.ProjectStorage.setActiveProjectId(sel.value);
    closeProjectModal();
    if (window.showToast) window.showToast('Loaded client project!', 'success');
    setTimeout(() => location.reload(), 400);
  }
}

function createNewProjectPrompt() {
  const name = prompt('Enter New Project / Client Title:', 'New Client Project');
  if (name) {
    const newId = 'proj_' + Date.now();
    const newProj = {
      id: newId,
      clientName: name,
      projectName: name,
      preparedBy: 'Agency',
      date: new Date().toISOString().split('T')[0],
      platform: 'Both',
      complexity: '1.0',
      discount: 0,
      calculators: {},
      questionnaires: {},
      checklists: {},
      updatedAt: new Date().toISOString()
    };
    window.ProjectStorage.saveProject(newProj);
    window.ProjectStorage.setActiveProjectId(newId);
    closeProjectModal();
    if (window.showToast) window.showToast(`Created new project: ${name}`, 'success');
    setTimeout(() => location.reload(), 400);
  }
}

window.openProjectManagerModal = openProjectManagerModal;
window.closeProjectModal = closeProjectModal;
window.confirmSwitchProject = confirmSwitchProject;
window.createNewProjectPrompt = createNewProjectPrompt;
