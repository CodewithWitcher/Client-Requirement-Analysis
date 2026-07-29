/**
 * Interactive Pricing Calculator & Checklist Controller
 * Handles live pricing computations, item toggles, custom client details, and auto-saving.
 */

document.addEventListener('DOMContentLoaded', () => {
  initProjectBanner();
  initCalculatorListeners();
  initChecklistListeners();
  checkWelcomeModal();
  renderFloatingProfileWidget();
});

// Sync data between open tabs in real-time
window.addEventListener('storage', (e) => {
  if (e.key === window.ProjectStorage.STORAGE_KEY || e.key === window.ProjectStorage.ACTIVE_KEY) {
    if (typeof initProjectBanner === 'function') initProjectBanner();
    if (typeof recalculatePriceTotals === 'function') recalculatePriceTotals();
    if (window.ProposalGenerator && typeof window.ProposalGenerator.renderProposal === 'function') {
      window.ProposalGenerator.renderProposal('proposal-output-container');
    }
  }
});

/**
 * Render active client banner & metadata form inputs
 */
function initProjectBanner() {
  const bannerContainer = document.getElementById('project-banner-container');
  if (!bannerContainer) return;

  const project = window.ProjectStorage.getProject();

  bannerContainer.innerHTML = `
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

/**
 * Initialize interactive listeners on tables with pricing items
 */
function initCalculatorListeners() {
  const calcTables = document.querySelectorAll('.interactive-calc-table');
  if (!calcTables.length) return;

  const project = window.ProjectStorage.getProject();
  const pageSlug = getPageSlug();

  // Ensure the calculator slot exists for this page
  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }
  const savedState = project.calculators[pageSlug];

  let stateUpdated = false;
  calcTables.forEach(table => {
    const rows = table.querySelectorAll('tr[data-item-id]');
    rows.forEach(row => {
      const itemId = row.getAttribute('data-item-id');
      const itemName = row.getAttribute('data-item-name') || itemId;
      const checkInput = row.querySelector('.item-check');
      const costInput = row.querySelector('.item-cost');
      const qtyInput = row.querySelector('.item-qty');
      const cells = row.querySelectorAll('td');
      const categoryFromDom = cells.length > 2 ? cells[2].textContent.trim() : 'General';

      if (savedState[itemId] !== undefined && savedState[itemId] !== null && typeof savedState[itemId] === 'object') {
        // Restore saved state — always apply the saved checked value explicitly
        if (checkInput) checkInput.checked = savedState[itemId].checked === true;
        if (costInput && savedState[itemId].cost !== undefined) costInput.value = savedState[itemId].cost;
        if (qtyInput && savedState[itemId].qty !== undefined) qtyInput.value = savedState[itemId].qty;
        // Ensure category is always up-to-date from DOM
        savedState[itemId].name = itemName;
        savedState[itemId].category = categoryFromDom;
        stateUpdated = true;
      } else {
        // First visit — initialize state from current HTML defaults
        const isChecked = checkInput ? checkInput.checked : true;
        const cost = parseFloat(costInput ? costInput.value : 0) || 0;
        const qty = parseFloat(qtyInput ? qtyInput.value : 1) || 1;
        savedState[itemId] = {
          checked: isChecked,
          cost: cost,
          qty: qty,
          total: isChecked ? cost * qty : 0,
          name: itemName,
          category: categoryFromDom
        };
        stateUpdated = true;
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

  if (stateUpdated) {
    window.ProjectStorage.saveProject(project);
  }

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
    const itemName = row.getAttribute('data-item-name') || itemId;
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

    const cells = row.querySelectorAll('td');
    const category = cells.length > 2 ? cells[2].textContent.trim() : 'General';

    project.calculators[pageSlug][itemId] = {
      checked: isChecked,
      cost: cost,
      qty: qty,
      total: lineTotal,
      name: itemName,
      category: category
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

  const platformMult = (project.platform === 'Both') ? 1.4 : (project.platform === 'Mobile' ? 1.2 : 1.0);
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

function checkWelcomeModal() {
  const path = window.location.pathname;
  const isLandingPage = path.endsWith('index.html') || path === '/' || path.endsWith('/') || path.endsWith('Client-Requirement-Analysis/') || path.endsWith('Client-Requirement-Analysis/docs/') || path.endsWith('docs/index.html');
  if (!isLandingPage) return;

  if (!sessionStorage.getItem('welcome_shown')) {
    sessionStorage.setItem('welcome_shown', 'true');
    openWelcomeModal();
  }
}

function openWelcomeModal() {
  const projects = window.ProjectStorage.getAllProjects();
  const activeId = window.ProjectStorage.getActiveProjectId();
  
  let optionsHtml = '';
  Object.values(projects).forEach(p => {
    const isSelected = p.id === activeId ? 'selected' : '';
    optionsHtml += `<option value="${p.id}">${escapeHtml(p.projectName)} (${escapeHtml(p.clientName)})</option>`;
  });

  const modalHtml = `
    <div id="welcome-modal-overlay" class="modal-overlay">
      <div class="modal-card" style="text-align: center; max-width: 500px;">
        <span style="font-size: 3rem;">👋</span>
        <h2 style="margin-top: 0.5rem; margin-bottom: 0.5rem; font-family: var(--font-serif); color: var(--text-main);">Welcome to Client Scoping Hub!</h2>
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 1.5rem; line-height: 1.5;">
          Select an existing client project from your local storage workspace, or create a new one to begin.
        </p>
        
        <div class="form-group" style="text-align: left; margin-bottom: 1.5rem;">
          <label style="font-weight: 700; font-size: 0.8rem; color: var(--text-muted);">Load Existing Customer:</label>
          <select id="welcome-project-select" class="form-control" style="width: 100%; margin-top: 0.35rem;">
            ${optionsHtml}
          </select>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.65rem;">
          <button class="export-btn primary" style="width: 100%; justify-content: center; padding: 0.75rem;" onclick="confirmWelcomeSwitch()">
            💼 Work on Selected Project
          </button>
          <button class="export-btn" style="width: 100%; justify-content: center; padding: 0.75rem;" onclick="createWelcomeNewProject()">
            ✨ Start a New Client Project
          </button>
          <button class="export-btn" style="width: 100%; justify-content: center; padding: 0.75rem; border: none; background: transparent; color: var(--text-subtle); cursor: pointer;" onclick="closeWelcomeModal()">
            Dismiss / Cancel
          </button>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closeWelcomeModal() {
  document.getElementById('welcome-modal-overlay')?.remove();
}

function confirmWelcomeSwitch() {
  const sel = document.getElementById('welcome-project-select');
  if (sel) {
    window.ProjectStorage.setActiveProjectId(sel.value);
    closeWelcomeModal();
    if (window.showToast) window.showToast('Loaded client project!', 'success');
    setTimeout(() => location.reload(), 400);
  }
}

function createWelcomeNewProject() {
  closeWelcomeModal();
  createNewProjectPrompt();
}

window.checkWelcomeModal = checkWelcomeModal;
window.openWelcomeModal = openWelcomeModal;
window.closeWelcomeModal = closeWelcomeModal;
window.confirmWelcomeSwitch = confirmWelcomeSwitch;
window.createWelcomeNewProject = createWelcomeNewProject;

function openProjectProfileModal() {
  const project = window.ProjectStorage.getProject();
  const projects = window.ProjectStorage.getAllProjects();
  
  let optionsHtml = '';
  Object.values(projects).forEach(p => {
    const isSelected = p.id === project.id ? 'selected' : '';
    optionsHtml += `<option value="${p.id}" ${isSelected}>${escapeHtml(p.projectName)} (${escapeHtml(p.clientName)})</option>`;
  });

  const standardPlatforms = ['Website', 'Android', 'iOS', 'Mobile', 'Both'];
  const isCustomPlatform = !standardPlatforms.includes(project.platform);
  const platformVal = isCustomPlatform ? 'Custom' : project.platform;
  const customPlatformText = isCustomPlatform ? project.platform : '';

  const modalHtml = `
    <div id="profile-edit-modal-overlay" class="modal-overlay">
      <div class="modal-card" style="max-width: 600px; width: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0;">
          <h3 style="font-family: var(--font-serif); font-size: 1.35rem; display: flex; align-items: center; gap: 0.5rem; color: var(--text-main);">
            <span>💼</span> Edit Client Workspace Profile
          </h3>
          <button class="export-btn" onclick="closeProjectProfileModal()">✕ Close</button>
        </div>

        <div style="background: rgba(99, 102, 241, 0.04); border: 1px solid rgba(99, 102, 241, 0.15); padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
          <div>
            <label style="font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Active Project Profile:</label>
            <select id="modal-profile-project-select" class="form-control" style="margin-top: 0.25rem; min-width: 200px;">
              ${optionsHtml}
            </select>
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: flex-end; margin-top: auto;">
            <button class="export-btn primary" onclick="confirmModalSwitchProject()">Load</button>
            <button class="export-btn" onclick="modalCreateNewProject()">+ New</button>
            <button class="export-btn" style="color: #ef4444; border-color: #ef4444;" onclick="modalDeleteProject('${project.id}')">🗑️ Delete</button>
          </div>
        </div>

        <div class="form-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem;">
          <div class="form-group">
            <label>Client Name</label>
            <input type="text" id="modal-client-name" class="form-control" value="${escapeHtml(project.clientName)}" placeholder="e.g. Acme Corporation">
          </div>
          <div class="form-group">
            <label>Project Scope Title</label>
            <input type="text" id="modal-project-name" class="form-control" value="${escapeHtml(project.projectName)}" placeholder="e.g. Mobile E-Commerce App">
          </div>
          <div class="form-group">
            <label>Prepared By / Agency</label>
            <input type="text" id="modal-prepared-by" class="form-control" value="${escapeHtml(project.preparedBy)}" placeholder="e.g. Witcher Tech Studio">
          </div>
          <div class="form-group">
            <label>Target Platform</label>
            <select id="modal-platform" class="form-control" onchange="toggleModalCustomPlatformInput(this.value)">
              <option value="Website" ${platformVal === 'Website' ? 'selected' : ''}>🌐 Website / Web App Only</option>
              <option value="Android" ${platformVal === 'Android' ? 'selected' : ''}>🤖 Android App Only</option>
              <option value="iOS" ${platformVal === 'iOS' ? 'selected' : ''}>🍎 iOS App Only</option>
              <option value="Mobile" ${platformVal === 'Mobile' ? 'selected' : ''}>📱 Both Android & iOS Mobile Apps</option>
              <option value="Both" ${platformVal === 'Both' ? 'selected' : ''}>⚡ Both Website & Mobile Apps (All Platforms)</option>
              <option value="Custom" ${platformVal === 'Custom' ? 'selected' : ''}>⚙️ Custom Platform...</option>
            </select>
            <div id="modal-custom-platform-container" style="margin-top: 0.5rem; display: ${isCustomPlatform ? 'block' : 'none'};">
              <input type="text" id="modal-custom-platform-input" class="form-control" placeholder="Enter Custom Platform Name (e.g. Smart TV App)" value="${escapeHtml(customPlatformText)}">
            </div>
          </div>
          <div class="form-group">
            <label>Complexity Multiplier</label>
            <select id="modal-complexity" class="form-control">
              <option value="1.0" ${project.complexity === '1.0' ? 'selected' : ''}>1.0x — Standard / Simple</option>
              <option value="1.3" ${project.complexity === '1.3' ? 'selected' : ''}>1.3x — Medium Complexity</option>
              <option value="1.5" ${project.complexity === '1.5' ? 'selected' : ''}>1.5x — High Complexity</option>
              <option value="2.0" ${project.complexity === '2.0' ? 'selected' : ''}>2.0x — Enterprise Level</option>
            </select>
          </div>
          <div class="form-group">
            <label>Discount (%)</label>
            <input type="number" id="modal-discount" class="form-control" min="0" max="50" value="${project.discount || 0}">
          </div>
        </div>

        <div style="background: rgba(245, 158, 11, 0.05); border: 1px solid rgba(245, 158, 11, 0.2); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;">
          <div style="font-size: 0.82rem; color: #b45309; line-height: 1.5;">
            ⚠️ <strong>Browser Storage Warning:</strong> Client profiles, checkboxes, and customized estimates are saved locally in your browser memory. Clearing browser history/cache will erase unsaved data.
          </div>
          <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
            <button class="export-btn" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" onclick="ProjectStorage.exportJSON()">💾 Backup Project JSON</button>
            <label class="export-btn" style="padding: 0.35rem 0.75rem; font-size: 0.8rem; cursor: pointer;">
              📂 Import Backup JSON
              <input type="file" accept=".json" style="display: none;" onchange="handleModalImportFile(event)">
            </label>
          </div>
        </div>

        <div style="display: flex; gap: 0.5rem; justify-content: flex-end; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
          <button class="export-btn" onclick="closeProjectProfileModal()">Cancel</button>
          <button class="export-btn primary" onclick="saveProjectProfileModal()">💾 Save & Apply Changes</button>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closeProjectProfileModal() {
  document.getElementById('profile-edit-modal-overlay')?.remove();
}

function toggleModalCustomPlatformInput(val) {
  const container = document.getElementById('modal-custom-platform-container');
  if (container) {
    container.style.display = (val === 'Custom') ? 'block' : 'none';
  }
}
window.toggleModalCustomPlatformInput = toggleModalCustomPlatformInput;

function saveProjectProfileModal() {
  const project = window.ProjectStorage.getProject();
  project.clientName = document.getElementById('modal-client-name')?.value || 'Client';
  project.projectName = document.getElementById('modal-project-name')?.value || 'Project';
  project.preparedBy = document.getElementById('modal-prepared-by')?.value || 'Agency';
  
  const platformSel = document.getElementById('modal-platform')?.value;
  if (platformSel === 'Custom') {
    project.platform = document.getElementById('modal-custom-platform-input')?.value.trim() || 'Custom';
  } else {
    project.platform = platformSel || 'Both';
  }
  
  project.complexity = document.getElementById('modal-complexity')?.value || '1.0';
  project.discount = parseFloat(document.getElementById('modal-discount')?.value || 0);

  window.ProjectStorage.saveProject(project);
  closeProjectProfileModal();
  if (window.showToast) window.showToast('Saved and updated client details globally!', 'success');
  setTimeout(() => location.reload(), 400);
}

function confirmModalSwitchProject() {
  const sel = document.getElementById('modal-profile-project-select');
  if (sel) {
    window.ProjectStorage.setActiveProjectId(sel.value);
    closeProjectProfileModal();
    if (window.showToast) window.showToast('Loaded client project!', 'success');
    setTimeout(() => location.reload(), 400);
  }
}

function modalCreateNewProject() {
  closeProjectProfileModal();
  createNewProjectPrompt();
}

function modalDeleteProject(id) {
  if (confirm('Are you sure you want to delete this client profile? All checked features and custom rates will be permanently erased.')) {
    const success = window.ProjectStorage.deleteClientProfile(id);
    if (success) {
      closeProjectProfileModal();
      if (window.showToast) window.showToast('Deleted client profile.', 'success');
      setTimeout(() => location.reload(), 400);
    }
  }
}

function handleModalImportFile(evt) {
  const file = evt.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      window.ProjectStorage.importJSON(e.target.result);
      closeProjectProfileModal();
    };
    reader.readAsText(file);
  }
}

function renderFloatingProfileWidget() {
  if (document.getElementById('floating-profile-btn')) return;

  const btnHtml = `
    <button id="floating-profile-btn" onclick="openProjectProfileModal()" title="Edit Client Workspace Profile">
      💼
    </button>
  `;
  document.body.insertAdjacentHTML('beforeend', btnHtml);
}

window.openProjectProfileModal = openProjectProfileModal;
window.closeProjectProfileModal = closeProjectProfileModal;
window.saveProjectProfileModal = saveProjectProfileModal;
window.confirmModalSwitchProject = confirmModalSwitchProject;
window.modalCreateNewProject = modalCreateNewProject;
window.modalDeleteProject = modalDeleteProject;
window.handleModalImportFile = handleModalImportFile;
window.renderFloatingProfileWidget = renderFloatingProfileWidget;

