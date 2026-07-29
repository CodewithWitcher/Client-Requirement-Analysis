/**
 * Interactive Pricing Calculator & Checklist Controller
 * Handles live pricing computations, item toggles, custom client details, and auto-saving.
 */

document.addEventListener('DOMContentLoaded', () => {
  try { initProjectBanner(); } catch(e) { console.error('initProjectBanner error:', e); }
  try { initCalculatorListeners(); } catch(e) { console.error('initCalculatorListeners error:', e); }
  try { initMaintenancePlanListeners(); } catch(e) { console.error('initMaintenancePlanListeners error:', e); }
  try { initHourlyRatesListeners(); } catch(e) { console.error('initHourlyRatesListeners error:', e); }
  try { initChecklistListeners(); } catch(e) { console.error('initChecklistListeners error:', e); }
  try { checkWelcomeModal(); } catch(e) { console.error('checkWelcomeModal error:', e); }
  try { renderFloatingProfileWidget(); } catch(e) { console.error('renderFloatingProfileWidget error:', e); }
  try { initCalcActionDelegation(); } catch(e) { console.error('initCalcActionDelegation error:', e); }
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

  const pageSlug = getPageSlug();

  // ── Build-stamp migration: ONLY add/remove items, never wipe user state ──
  const excelViewer = document.querySelector('.excel-viewer[data-build-stamp]');
  if (excelViewer) {
    const currentStamp = excelViewer.getAttribute('data-build-stamp');
    const stampKey = `calc_stamp_${pageSlug}`;
    const savedStamp = localStorage.getItem(stampKey);
    if (savedStamp !== currentStamp) {
      // Excel was rebuilt — mark stamp as seen but DO NOT wipe user's saved state.
      // New items will get defaults; removed items will simply be orphaned in savedState
      // (they won't appear in the DOM so they won't affect calculations).
      localStorage.setItem(stampKey, currentStamp);
    }
  }

  // ── Step 1: Restore/init checkbox state FIRST, before attaching listeners ──
  // CRITICAL: State MUST be restored before event listeners are attached,
  // otherwise setting checkInput.checked triggers 'change' events that call
  // handleItemChange, which reads ALL rows' current DOM state and overwrites
  // the not-yet-restored rows with their HTML defaults (unchecked).
  window._calcRestoringState = true;
  const project = window.ProjectStorage.getProject();

  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }
  const savedState = project.calculators[pageSlug];
  let dirty = false;

  calcTables.forEach(table => {
    table.querySelectorAll('tr[data-item-id]').forEach(row => {
      const itemId = row.getAttribute('data-item-id');
      const itemName = row.getAttribute('data-item-name') || itemId;
      const checkInput = row.querySelector('.item-check');
      const costInput = row.querySelector('.item-cost');
      const qtyInput = row.querySelector('.item-qty');
      const rowTotalCell = row.querySelector('.item-row-total');
      const cells = row.querySelectorAll('td');
      const categoryFromDom = cells.length > 2 ? cells[2].textContent.trim() : 'General';

      const existing = savedState[itemId];

      if (existing && typeof existing === 'object') {
        // ── RETURNING VISITOR: restore exact saved state ──
        const savedChecked = existing.checked === true; // strict boolean
        if (checkInput) checkInput.checked = savedChecked;
        if (costInput && existing.cost !== undefined) costInput.value = existing.cost;
        if (qtyInput && existing.qty !== undefined) qtyInput.value = existing.qty;

        // Update row total visual to match saved state
        if (rowTotalCell) {
          const cost = parseFloat(existing.cost || 0);
          const qty = parseFloat(existing.qty || 1);
          const lineTotal = savedChecked ? cost * qty : 0;
          rowTotalCell.textContent = '₹' + lineTotal.toLocaleString('en-IN');
          rowTotalCell.style.opacity = savedChecked ? '1' : '0.4';
        }

        // Refresh metadata (name/category may have changed in rebuild)
        existing.name = itemName;
        existing.category = categoryFromDom;
        dirty = true;

      } else {
        // ── FIRST VISIT: read data-default-checked attr (not HTML checked) ──
        const defaultVal = checkInput ? checkInput.getAttribute('data-default-checked') : 'true';
        const isChecked = defaultVal !== 'false'; // anything that isn't explicitly false is on
        const cost = parseFloat(costInput ? costInput.value : 0) || 0;
        const qty = parseFloat(qtyInput ? qtyInput.value : 1) || 1;

        if (checkInput) checkInput.checked = isChecked;
        if (rowTotalCell) {
          const lineTotal = isChecked ? cost * qty : 0;
          rowTotalCell.textContent = '₹' + lineTotal.toLocaleString('en-IN');
          rowTotalCell.style.opacity = isChecked ? '1' : '0.4';
        }

        savedState[itemId] = {
          checked: isChecked,
          cost: cost,
          qty: qty,
          total: isChecked ? cost * qty : 0,
          name: itemName,
          category: categoryFromDom
        };
        dirty = true;
      }
    });
  });

  if (dirty) {
    window.ProjectStorage.saveProject(project);
  }
  recalculatePriceTotals();
  window._calcRestoringState = false;

  // ── Step 2: Attach event listeners AFTER state is fully restored ────────
  calcTables.forEach(table => {
    try {
      table.querySelectorAll('tr[data-item-id]').forEach(row => {
        const checkInput = row.querySelector('.item-check');
        const costInput = row.querySelector('.item-cost');
        const qtyInput = row.querySelector('.item-qty');
        [checkInput, costInput, qtyInput].forEach(input => {
          if (input) {
            input.addEventListener('change', () => handleItemChange(table, pageSlug));
            input.addEventListener('input', () => handleItemChange(table, pageSlug));
          }
        });
      });

      // ── Step 3: Inject action toolbar & restore custom rows ──
      injectPricingTableToolbar(table, pageSlug);
    } catch(e) {
      console.error('Error initializing table:', table, e);
    }
  });
}

function handleItemChange(table, pageSlug) {
  // Safety: don't save during state restoration to avoid overwriting not-yet-restored rows
  if (window._calcRestoringState) return;

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

  // Mark as having unsaved changes (pending explicit save)
  markUnsavedChanges();
}

/**
 * Mark that unsaved changes exist — updates Save button visual state
 */
function markUnsavedChanges() {
  const btn = document.getElementById('save-pricing-btn');
  if (!btn) return;
  btn.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
  btn.style.borderColor = '#f59e0b';
  btn.innerHTML = `
    <svg viewBox="0 0 24 24" style="width:16px;height:16px;fill:currentColor"><path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/></svg>
    ⚠️ Unsaved Changes — Click to Save
  `;
}

/**
 * Explicitly save all current pricing table states to localStorage
 */
function savePricingState() {
  const calcTables = document.querySelectorAll('.interactive-calc-table');
  const project = window.ProjectStorage.getProject();
  const pageSlug = getPageSlug();

  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }

  // Snapshot every row from every interactive pricing table
  calcTables.forEach(table => {
    const rows = table.querySelectorAll('tr[data-item-id]');
    rows.forEach(row => {
      const itemId = row.getAttribute('data-item-id');
      const itemName = row.getAttribute('data-item-name') || itemId;
      const checkInput = row.querySelector('.item-check');
      const costInput = row.querySelector('.item-cost');
      const qtyInput = row.querySelector('.item-qty');
      const rowTotalCell = row.querySelector('.item-row-total');
      const cells = row.querySelectorAll('td');
      const category = cells.length > 2 ? cells[2].textContent.trim() : 'General';

      const isChecked = checkInput ? checkInput.checked : true;
      const cost = parseFloat(costInput ? costInput.value : 0) || 0;
      const qty = parseFloat(qtyInput ? qtyInput.value : 1) || 1;
      const lineTotal = isChecked ? cost * qty : 0;

      // Update visible row total
      if (rowTotalCell) {
        rowTotalCell.textContent = '₹' + lineTotal.toLocaleString('en-IN');
        rowTotalCell.style.opacity = isChecked ? '1' : '0.4';
      }

      project.calculators[pageSlug][itemId] = {
        checked: isChecked,
        cost: cost,
        qty: qty,
        total: lineTotal,
        name: itemName,
        category: category
      };
    });
  });

  // Snapshot maintenance plan states
  const maintTables = document.querySelectorAll('.maintenance-table');
  maintTables.forEach(table => {
    const maintType = table.getAttribute('data-maint-type') || 'web';
    const stateKey = `maint_${maintType}`;
    const state = { prices: {}, selectedPlan: null };

    table.querySelectorAll('.maint-plan-price').forEach(input => {
      state.prices[input.getAttribute('data-plan')] = parseInt(input.value, 10) || 0;
    });

    const selectedRadio = table.querySelector('.maint-plan-radio:checked');
    state.selectedPlan = selectedRadio ? selectedRadio.value : null;
    project.calculators[pageSlug][stateKey] = state;
  });

  // Snapshot hourly rate states
  const ratesTables = document.querySelectorAll('.hourly-rates-table');
  ratesTables.forEach(table => {
    const ratesType = table.getAttribute('data-rates-type') || 'web';
    const stateKey = `rates_${ratesType}`;
    const state = {};

    table.querySelectorAll('tr[data-rate-id]').forEach(row => {
      const costInput = row.querySelector('.rate-cost');
      if (costInput) {
        state[row.getAttribute('data-rate-id')] = parseInt(costInput.value, 10) || 0;
      }
    });

    project.calculators[pageSlug][stateKey] = state;
  });

  window.ProjectStorage.saveProject(project);
  recalculatePriceTotals();
  updateHourlyRatesSummaryWidgets();

  // Update Save button to confirm saved state
  const btn = document.getElementById('save-pricing-btn');
  if (btn) {
    btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    btn.style.borderColor = '#10b981';
    btn.innerHTML = `
      <svg viewBox="0 0 24 24" style="width:16px;height:16px;fill:currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>
      ✅ Pricing Saved!
    `;
    setTimeout(() => {
      btn.innerHTML = `
        <svg viewBox="0 0 24 24" style="width:16px;height:16px;fill:currentColor"><path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/></svg>
        💾 Save Pricing Changes
      `;
    }, 2500);
  }

  if (typeof window.showToast === 'function') {
    window.showToast('✅ Pricing selections saved! Your proposal is now updated.', 'success');
  }
}

window.savePricingState = savePricingState;

/**
 * Calculate grand totals, taxes, multipliers, and payment milestones
 */
function recalculatePriceTotals() {
  const project = window.ProjectStorage.getProject();
  let subtotal = 0;

  // Sum up line totals across all calculator sheets
  Object.values(project.calculators || {}).forEach(sheetState => {
    Object.values(sheetState).forEach(item => {
      // Skip maintenance plan state objects and rate state objects
      if (item && typeof item === 'object' && item.checked !== undefined) {
        if (item.checked) {
          subtotal += (item.total || 0);
        }
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

  // ── Maintenance Plan Summary ──
  updateMaintenanceSummaryWidgets(project);
}

/**
 * Update maintenance plan summary widgets on the page
 */
function updateMaintenanceSummaryWidgets(project) {
  const pageSlug = getPageSlug();
  const calcState = project.calculators[pageSlug] || {};

  // WEB Maintenance
  const webMaint = calcState['maint_web'];
  if (webMaint && webMaint.selectedPlan) {
    const webMonthly = webMaint.prices[webMaint.selectedPlan] || 0;
    updateSummaryWidget('summary-web-maint-monthly', '₹' + webMonthly.toLocaleString('en-IN') + '/mo');
    updateSummaryWidget('summary-web-maint-yearly', '₹' + (webMonthly * 12).toLocaleString('en-IN') + '/yr');
  }

  // APP Maintenance
  const appMaint = calcState['maint_app'];
  if (appMaint && appMaint.selectedPlan) {
    const appMonthly = appMaint.prices[appMaint.selectedPlan] || 0;
    updateSummaryWidget('summary-app-maint-monthly', '₹' + appMonthly.toLocaleString('en-IN') + '/mo');
    updateSummaryWidget('summary-app-maint-yearly', '₹' + (appMonthly * 12).toLocaleString('en-IN') + '/yr');
  }
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

// ══════════════════════════════════════════════════════════════
//  MAINTENANCE PLANS — Dynamic Pricing & Plan Selector
// ══════════════════════════════════════════════════════════════

const USD_CONVERSION_RATE = 75; // ₹75 = $1

function initMaintenancePlanListeners() {
  const maintTables = document.querySelectorAll('.maintenance-table');
  if (!maintTables.length) return;

  const pageSlug = getPageSlug();
  const project = window.ProjectStorage.getProject();

  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }

  maintTables.forEach(table => {
    const maintType = table.getAttribute('data-maint-type') || 'web';
    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    // ── Convert static price header row to editable inputs ──
    const allRows = tbody.querySelectorAll('tr');
    let headerRow = null;
    let planNames = [];
    let planPrices = [];

    allRows.forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 6) {
        const firstCell = cells[0].textContent.trim();
        if (firstCell === '#') {
          // This is the header row: #, Service, Basic\n₹3K/mo, Standard\n₹8K/mo, etc.
          headerRow = row;
          for (let i = 2; i < cells.length; i++) {
            const cellText = cells[i].textContent.trim();
            // Parse: "Basic\n₹3K/mo" → name="Basic", price=3000
            const lines = cellText.split('\n');
            const planName = lines[0].trim();
            const priceStr = (lines[1] || '').replace(/[₹,\/moKk]/g, '').trim();
            let price = parseInt(priceStr, 10) || 0;
            // Handle "K" suffix: "3K" → 3000
            if (/[kK]/.test(lines[1] || '')) {
              price = price * 1000;
            }
            planNames.push({ name: planName, id: `${maintType}_${planName.toLowerCase()}`, price: price });
            planPrices.push(price);
          }
        }
      }
    });

    if (!headerRow || planNames.length === 0) return;

    // Get saved state
    const stateKey = `maint_${maintType}`;
    const savedState = project.calculators[pageSlug][stateKey] || {};

    // Convert header cells to editable inputs
    const headerCells = headerRow.querySelectorAll('td');
    for (let i = 2; i < headerCells.length; i++) {
      const planIdx = i - 2;
      if (planIdx < planNames.length) {
        const plan = planNames[planIdx];
        const savedPrice = (savedState.prices && savedState.prices[plan.id] !== undefined) ? savedState.prices[plan.id] : plan.price;
        headerCells[i].innerHTML = `${plan.name}<br><input type="number" class="maint-plan-price form-control" data-plan="${plan.id}" value="${savedPrice}" min="0" step="100" style="width:80px;margin-top:4px;padding:4px;text-align:center;">₹/mo`;
      }
    }

    // ── Add plan selector row ──
    let defaultSelected = maintType === 'web' ? `${maintType}_standard` : `${maintType}_standard`;
    if (savedState.selectedPlan) defaultSelected = savedState.selectedPlan;

    const selectorRow = document.createElement('tr');
    selectorRow.style.cssText = 'background:rgba(99,102,241,0.08);';
    let selectorHtml = '<td colspan="2" style="text-align:right;font-weight:700;padding:10px;">💡 Select Maintenance Plan:</td>';
    planNames.forEach(plan => {
      const checked = plan.id === defaultSelected ? ' checked' : '';
      selectorHtml += `<td style="text-align:center;"><input type="radio" name="${maintType}_maint_plan" value="${plan.id}" class="maint-plan-radio"${checked}></td>`;
    });
    selectorRow.innerHTML = selectorHtml;
    tbody.appendChild(selectorRow);

    // ── Add summary row ──
    const selectedPrice = savedState.prices && savedState.prices[defaultSelected] ? savedState.prices[defaultSelected] : (planNames.find(p => p.id === defaultSelected) || {}).price || 0;
    const summaryId = maintType === 'web' ? 'web-maint-summary-cost' : 'app-maint-summary-cost';
    const summaryRow = document.createElement('tr');
    summaryRow.id = maintType === 'web' ? 'web-maint-summary-row' : 'app-maint-summary-row';
    summaryRow.style.cssText = 'background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(5,150,105,0.06));font-weight:700;';
    const remainingCols = headerCells.length - 2; // cols after Service
    summaryRow.innerHTML = `<td colspan="2" style="text-align:right;padding:10px;">📌 Selected Plan Monthly Cost:</td><td colspan="${remainingCols}" style="text-align:center;font-size:1.2rem;color:#10b981;" id="${summaryId}">₹${selectedPrice.toLocaleString('en-IN')}/mo</td>`;
    tbody.appendChild(summaryRow);

    // ── Attach event listeners ──
    const priceInputs = table.querySelectorAll('.maint-plan-price');
    priceInputs.forEach(input => {
      input.addEventListener('input', () => handleMaintPlanChange(table, maintType, pageSlug));
      input.addEventListener('change', () => handleMaintPlanChange(table, maintType, pageSlug));
    });

    const radios = table.querySelectorAll('.maint-plan-radio');
    radios.forEach(radio => {
      radio.addEventListener('change', () => {
        if (radio.checked) handleMaintPlanChange(table, maintType, pageSlug);
      });
    });
  });
}

function handleMaintPlanChange(table, maintType, pageSlug) {
  const project = window.ProjectStorage.getProject();
  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }

  const stateKey = `maint_${maintType}`;
  const state = { prices: {}, selectedPlan: null };

  // Collect prices
  const priceInputs = table.querySelectorAll('.maint-plan-price');
  priceInputs.forEach(input => {
    const planId = input.getAttribute('data-plan');
    state.prices[planId] = parseInt(input.value, 10) || 0;
  });

  // Get selected plan
  const selectedRadio = table.querySelector('.maint-plan-radio:checked');
  state.selectedPlan = selectedRadio ? selectedRadio.value : null;

  project.calculators[pageSlug][stateKey] = state;
  window.ProjectStorage.saveProject(project);

  // Update summary
  updateMaintPlanSummary(table, maintType, state.selectedPlan);
  recalculatePriceTotals();

  if (typeof showGlobalSaveBar === 'function') showGlobalSaveBar();
}

function updateMaintPlanSummary(table, maintType, selectedPlanId) {
  const priceInputs = table.querySelectorAll('.maint-plan-price');
  let selectedPrice = 0;
  priceInputs.forEach(input => {
    if (input.getAttribute('data-plan') === selectedPlanId) {
      selectedPrice = parseInt(input.value, 10) || 0;
    }
  });

  const summaryId = maintType === 'web' ? 'web-maint-summary-cost' : 'app-maint-summary-cost';
  const summaryEl = document.getElementById(summaryId);
  if (summaryEl) {
    summaryEl.textContent = '₹' + selectedPrice.toLocaleString('en-IN') + '/mo';
  }

  // Also update the corresponding year cost if there's an element for it
  const yearSummaryId = maintType === 'web' ? 'web-maint-yearly-cost' : 'app-maint-yearly-cost';
  const yearEl = document.getElementById(yearSummaryId);
  if (yearEl) {
    yearEl.textContent = '₹' + (selectedPrice * 12).toLocaleString('en-IN') + '/yr';
  }
}

// ══════════════════════════════════════════════════════════════
//  HOURLY RATES — Dynamic Rate Editor with Auto-Calculation
// ══════════════════════════════════════════════════════════════

function initHourlyRatesListeners() {
  const ratesTables = document.querySelectorAll('.hourly-rates-table');
  if (!ratesTables.length) return;

  const pageSlug = getPageSlug();
  const project = window.ProjectStorage.getProject();

  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }

  // Map of rate names → rate IDs (for consistent identification across rebuilds)
  const rateNameMap = {
    'Junior Developer (0-2 yrs)': 'rate_web_junior_dev',
    'Mid-Level Developer (2-5 yrs)': 'rate_web_mid_dev',
    'Senior Developer (5-8 yrs)': 'rate_web_senior_dev',
    'Lead Developer (8+ yrs)': 'rate_web_lead_dev',
    'UI/UX Designer (Mid)': 'rate_web_ux_mid',
    'UI/UX Designer (Senior)': 'rate_web_ux_senior',
    'Full-Stack Developer (Mid)': 'rate_web_fs_mid',
    'Full-Stack Developer (Senior)': 'rate_web_fs_senior',
    'DevOps Engineer': 'rate_web_devops',
    'QA / Tester': 'rate_web_qa',
    'Project Manager': 'rate_web_pm',
    'Technical Architect': 'rate_web_architect'
  };

  ratesTables.forEach(table => {
    const ratesType = table.getAttribute('data-rates-type') || 'web';
    const stateKey = `rates_${ratesType}`;
    const savedState = project.calculators[pageSlug][stateKey] || {};

    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    const allRows = tbody.querySelectorAll('tr');

    allRows.forEach(row => {
      const cells = row.querySelectorAll('td');
      // Rate rows have 5 cells: #, Developer Level, Rate (₹/hr), Rate ($/hr), Monthly
      if (cells.length >= 4) {
        const nameCell = cells[1];
        const rateName = nameCell ? nameCell.textContent.trim() : '';
        // Check if this looks like a rate row (has a developer role name and numeric rate)
        const rateCell = cells[2];
        const rateText = rateCell ? rateCell.textContent.trim() : '';
        const rateValue = parseInt(rateText, 10);

        if (rateName && !isNaN(rateValue) && rateValue > 0) {
          // Determine rate ID from name map or generate one
          let rateId = rateNameMap[rateName];
          if (!rateId) {
            rateId = 'rate_' + ratesType + '_' + rateName.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
          }

          row.setAttribute('data-rate-id', rateId);
          row.setAttribute('data-rate-name', rateName);

          // Get saved rate or use default
          const savedRate = (savedState[rateId] !== undefined) ? savedState[rateId] : rateValue;

          // Convert Rate (₹/hr) cell to editable input
          cells[2].innerHTML = `<input type="number" class="rate-cost form-control" value="${savedRate}" min="0" step="50" style="width:85px;padding:4px;text-align:center;">`;

          // Convert Rate ($/hr) cell to calculated span
          const usdRate = Math.round(savedRate / USD_CONVERSION_RATE);
          cells[3].innerHTML = `<span class="rate-usd-val">$${usdRate}</span>`;

          // Convert Monthly cell to calculated span
          const monthlyRate = savedRate * 160;
          cells[4].innerHTML = `<span class="rate-monthly-val">₹${monthlyRate.toLocaleString('en-IN')}</span>`;

          // Attach listeners
          const costInput = row.querySelector('.rate-cost');
          if (costInput) {
            costInput.addEventListener('input', () => {
              updateRateRowDisplay(row);
              saveHourlyRatesState(table, ratesType, pageSlug);
            });
            costInput.addEventListener('change', () => {
              updateRateRowDisplay(row);
              saveHourlyRatesState(table, ratesType, pageSlug);
            });
          }
        }
      }
    });

    // Initial summary update
    updateHourlyRatesSummaryWidgets();
  });
}

function updateRateRowDisplay(row) {
  const costInput = row.querySelector('.rate-cost');
  const usdEl = row.querySelector('.rate-usd-val');
  const monthlyEl = row.querySelector('.rate-monthly-val');

  if (!costInput) return;

  const rateINR = parseInt(costInput.value, 10) || 0;
  const rateUSD = Math.round(rateINR / USD_CONVERSION_RATE);
  const monthlyINR = rateINR * 160;

  if (usdEl) usdEl.textContent = '$' + rateUSD;
  if (monthlyEl) monthlyEl.textContent = '₹' + monthlyINR.toLocaleString('en-IN');
}

function saveHourlyRatesState(table, ratesType, pageSlug) {
  const project = window.ProjectStorage.getProject();
  if (!project.calculators[pageSlug]) {
    project.calculators[pageSlug] = {};
  }

  const stateKey = `rates_${ratesType}`;
  const state = {};

  const rateRows = table.querySelectorAll('tr[data-rate-id]');
  rateRows.forEach(row => {
    const rateId = row.getAttribute('data-rate-id');
    const costInput = row.querySelector('.rate-cost');
    if (costInput) {
      state[rateId] = parseInt(costInput.value, 10) || 0;
    }
  });

  project.calculators[pageSlug][stateKey] = state;
  window.ProjectStorage.saveProject(project);

  updateHourlyRatesSummaryWidgets();
  if (typeof showGlobalSaveBar === 'function') showGlobalSaveBar();
}

/**
 * Update the hourly rates summary card at the bottom of the page
 */
function updateHourlyRatesSummaryWidgets() {
  const tables = document.querySelectorAll('.hourly-rates-table');
  if (!tables.length) return;

  // Use first table (WEB rates) for the summary
  const table = tables[0];
  const rateRows = table.querySelectorAll('tr[data-rate-id]');
  const rateMap = {};
  rateRows.forEach(row => {
    const rateId = row.getAttribute('data-rate-id');
    const costInput = row.querySelector('.rate-cost');
    if (costInput) {
      rateMap[rateId] = parseInt(costInput.value, 10) || 0;
    }
  });

  updateSummaryWidget('summary-rate-junior', '₹' + (rateMap['rate_web_junior_dev'] || 500).toLocaleString('en-IN') + '/hr');
  updateSummaryWidget('summary-rate-senior', '₹' + (rateMap['rate_web_senior_dev'] || 1800).toLocaleString('en-IN') + '/hr');
  updateSummaryWidget('summary-rate-fs-senior', '₹' + (rateMap['rate_web_fs_senior'] || 2200).toLocaleString('en-IN') + '/hr');
  updateSummaryWidget('summary-rate-architect', '₹' + (rateMap['rate_web_architect'] || 3000).toLocaleString('en-IN') + '/hr');
}

// ══════════════════════════════════════════════════════════════
//  DYNAMIC CATEGORY & LINE ITEM MANAGEMENT
// ══════════════════════════════════════════════════════════════

/**
 * Inject action toolbar at the bottom of each pricing calculator table
 * and restore previously saved custom rows from project state.
 */
function injectPricingTableToolbar(table, pageSlug) {
  const tbody = table.querySelector('tbody');
  if (!tbody) return;

  // Check if toolbar already exists in HTML (generated by build script)
  let toolbar = tbody.querySelector('.calc-toolbar-row');

  // Remove existing custom rows before re-injecting (but keep the static toolbar)
  tbody.querySelectorAll('tr[data-custom="true"], tr[data-custom-category="true"]').forEach(r => r.remove());

  const tableType = getTableType(table);

  // ── Restore custom rows from state ──
  const project = window.ProjectStorage.getProject();
  const customKey = `custom_${tableType}`;
  const customState = (project.calculators[pageSlug] && project.calculators[pageSlug][customKey]) || { categories: [] };

  if (customState.categories && customState.categories.length > 0) {
    customState.categories.forEach(cat => {
      renderCustomCategory(tbody, cat);
    });
  }

  // If toolbar doesn't exist yet (JS injection didn't happen or HTML missing), create it
  if (!toolbar) {
    toolbar = document.createElement('tr');
    toolbar.className = 'calc-toolbar-row';
    toolbar.setAttribute('data-toolbar', 'true');
    toolbar.style.cssText = 'background:rgba(99,102,241,0.04);border-top:2px dashed rgba(99,102,241,0.3);';

    const colSpan = table.querySelector('tr') ? table.querySelector('tr').children.length : 8;
    toolbar.innerHTML = `
      <td colspan="${colSpan}" style="padding:10px 14px;text-align:center;">
        <button class="calc-action-btn add-category-btn" data-action="add-category" title="Add a new category section">
          ➕ Add Category
        </button>
        <button class="calc-action-btn add-item-btn" data-action="add-item" title="Add a new line item to a category" style="margin-left:8px;">
          ➕ Add Line Item
        </button>
      </td>
    `;
    tbody.appendChild(toolbar);
  }

  // Re-number all rows
  renumberTableRows(table);
}

/**
 * Detect table type from its content — 'web' or 'app'
 */
function getTableType(table) {
  const headerCell = table.querySelector('th');
  if (headerCell) {
    const text = headerCell.textContent.trim();
    if (text.includes('APP:') || text.includes('APPLICATION')) return 'app';
  }
  return 'web';
}

/**
 * Render a custom category (header row + its items) into the tbody before the toolbar
 */
function renderCustomCategory(tbody, cat) {
  const colSpan = tbody.closest('table').querySelector('tr') ? tbody.closest('table').querySelector('tr').children.length : 8;

  // Category header row
  const catRow = document.createElement('tr');
  catRow.setAttribute('data-custom-category', 'true');
  catRow.setAttribute('data-category-name', cat.name);
  catRow.style.cssText = 'background:rgba(99,102,241,0.06);';
  catRow.innerHTML = `<td style="font-weight:700;color:var(--accent-indigo,#6366f1);">${escapeHtml(cat.name)}</td>`
    + `<td colspan="${colSpan - 1}" style="text-align:right;">
        <button class="calc-action-btn delete-cat-btn" data-action="delete-category" title="Delete this category and all its items" style="font-size:0.75rem;padding:2px 8px;color:#ef4444;">🗑️ Delete Category</button>
      </td>`;

  // Insert before toolbar (or at end if no toolbar)
  const toolbar = tbody.querySelector('.calc-toolbar-row');
  if (toolbar) {
    tbody.insertBefore(catRow, toolbar);
  } else {
    tbody.appendChild(catRow);
  }

  // Item rows — each inserted before toolbar
  (cat.items || []).forEach(item => {
    renderCustomItemRow(tbody, item, cat.name);
  });
}

/**
 * Render a single custom item row into the tbody
 */
function renderCustomItemRow(tbody, item, categoryName) {
  const colSpan = tbody.closest('table').querySelector('tr') ? tbody.closest('table').querySelector('tr').children.length : 8;
  const itemRow = document.createElement('tr');
  itemRow.setAttribute('data-custom', 'true');
  itemRow.setAttribute('data-item-id', item.id);
  itemRow.setAttribute('data-item-name', item.name);
  itemRow.setAttribute('data-category', categoryName);

  const checked = item.checked !== false;
  const cost = item.cost || 0;
  const qty = item.qty || 1;

  itemRow.innerHTML = `
    <td class="row-num">#</td>
    <td contenteditable="true" class="editable-item-name" style="min-width:150px;outline:none;border-bottom:1px dashed #cbd5e1;padding:6px;">${escapeHtml(item.name)}</td>
    <td style="color:var(--text-muted);font-size:0.85rem;">${escapeHtml(categoryName)}</td>
    <td><input type="number" class="item-cost form-control" value="${cost}" min="0" step="100" style="width:90px;padding:4px;text-align:center;"></td>
    <td><input type="number" class="item-qty form-control" value="${qty}" min="0" step="1" style="width:70px;padding:4px;text-align:center;"></td>
    <td><span class="item-row-total" style="opacity:${checked?'1':'0.4'}">₹${(checked ? cost * qty : 0).toLocaleString('en-IN')}</span></td>
    <td style="text-align:center;"><input type="checkbox" class="item-check" ${checked ? 'checked' : ''}></td>
    <td style="text-align:center;"><button class="calc-action-btn delete-item-btn" data-action="delete-item" title="Remove this line item" style="font-size:0.75rem;padding:2px 6px;color:#ef4444;">🗑️</button></td>
  `;

  const toolbar = tbody.querySelector('.calc-toolbar-row');
  if (toolbar) {
    tbody.insertBefore(itemRow, toolbar);
  } else {
    tbody.appendChild(itemRow);
  }

  // Attach listeners to the new row's inputs
  const pageSlug = getPageSlug();
  const table = tbody.closest('table');
  itemRow.querySelectorAll('.item-check, .item-cost, .item-qty').forEach(input => {
    input.addEventListener('change', () => {
      handleItemChange(table, pageSlug);
      saveCustomRowsState(table, pageSlug);
    });
    input.addEventListener('input', () => {
      handleItemChange(table, pageSlug);
      saveCustomRowsState(table, pageSlug);
    });
  });

  // Editable name
  const nameCell = itemRow.querySelector('.editable-item-name');
  if (nameCell) {
    nameCell.addEventListener('blur', () => {
      itemRow.setAttribute('data-item-name', nameCell.textContent.trim());
      item.name = nameCell.textContent.trim();
      saveCustomRowsState(table, pageSlug);
    });
  }
}

/**
 * Collect all custom rows from a table and save to project state
 */
function saveCustomRowsState(table, pageSlug) {
  const tableType = getTableType(table);
  const customKey = `custom_${tableType}`;
  const project = window.ProjectStorage.getProject();
  if (!project.calculators[pageSlug]) project.calculators[pageSlug] = {};

  const categories = [];
  let currentCat = null;

  const allRows = table.querySelectorAll('tbody > tr');
  allRows.forEach(row => {
    if (row.hasAttribute('data-custom-category')) {
      // Push previous category
      if (currentCat) categories.push(currentCat);
      currentCat = {
        name: row.getAttribute('data-category-name') || 'New Category',
        items: []
      };
    } else if (row.hasAttribute('data-custom') && currentCat) {
      const itemId = row.getAttribute('data-item-id');
      const nameCell = row.querySelector('.editable-item-name');
      const costInput = row.querySelector('.item-cost');
      const qtyInput = row.querySelector('.item-qty');
      const checkInput = row.querySelector('.item-check');
      const name = nameCell ? nameCell.textContent.trim() : (row.getAttribute('data-item-name') || 'New Item');

      currentCat.items.push({
        id: itemId,
        name: name,
        cost: parseFloat(costInput ? costInput.value : 0) || 0,
        qty: parseFloat(qtyInput ? qtyInput.value : 1) || 1,
        checked: checkInput ? checkInput.checked : true
      });
    } else if (row.hasAttribute('data-toolbar')) {
      // Toolbar row — push last category
      if (currentCat) categories.push(currentCat);
      currentCat = null;
    }
  });
  // Push any remaining category
  if (currentCat) categories.push(currentCat);

  project.calculators[pageSlug][customKey] = { categories: categories };
  window.ProjectStorage.saveProject(project);

  // ── Also save custom items in flat format for recalculatePriceTotals ──
  const tbody2 = table.querySelector('tbody');
  const customRows = tbody2.querySelectorAll('tr[data-custom="true"]');
  customRows.forEach(row => {
    const itemId = row.getAttribute('data-item-id');
    const checkInput = row.querySelector('.item-check');
    const costInput = row.querySelector('.item-cost');
    const qtyInput = row.querySelector('.item-qty');
    const nameCell = row.querySelector('.editable-item-name');
    const catCell = row.querySelectorAll('td')[2]; // 3rd td is category
    const name = nameCell ? nameCell.textContent.trim() : (row.getAttribute('data-item-name') || 'New Item');

    if (itemId) {
      const checked = checkInput ? checkInput.checked : true;
      const cost = parseFloat(costInput ? costInput.value : 0) || 0;
      const qty = parseFloat(qtyInput ? qtyInput.value : 1) || 1;
      project.calculators[pageSlug][itemId] = {
        checked: checked,
        cost: cost,
        qty: qty,
        total: checked ? cost * qty : 0,
        name: name,
        category: catCell ? catCell.textContent.trim() : 'Custom'
      };
    }
  });

  window.ProjectStorage.saveProject(project);

  if (typeof showGlobalSaveBar === 'function') showGlobalSaveBar();
}

/**
 * Prompt user to add a new category
 */
function addCategoryPrompt(btn) {
  const table = btn.closest('table');
  const tbody = table.querySelector('tbody');
  const catName = prompt('📂 Enter new category name:', 'e.g. THIRD-PARTY INTEGRATIONS');
  if (!catName || !catName.trim()) return;

  const pageSlug = getPageSlug();
  const catData = {
    name: catName.trim().toUpperCase(),
    items: [{
      id: 'custom_' + Date.now(),
      name: 'New Item',
      cost: 0,
      qty: 1,
      checked: true
    }]
  };

  renderCustomCategory(tbody, catData);
  renumberTableRows(table);
  saveCustomRowsState(table, pageSlug);
  recalculatePriceTotals();
}

/**
 * Prompt user to add a new line item to an existing category
 */
function addItemPrompt(btn) {
  const table = btn.closest('table');
  const tbody = table.querySelector('tbody');
  const pageSlug = getPageSlug();

  // Collect all category names from the table
  const categoryNames = [];
  const allRows = table.querySelectorAll('tbody > tr');
  allRows.forEach(row => {
    // Skip rows that are definitely not categories
    if (row.hasAttribute('data-item-id')) return;
    if (row.hasAttribute('data-toolbar')) return;
    if (row.hasAttribute('data-custom')) return;
    if (row.hasAttribute('data-custom-category')) {
      const name = row.getAttribute('data-category-name');
      if (name && !categoryNames.includes(name)) categoryNames.push(name);
      return;
    }

    // Check for built-in category: first td has text, all other tds are empty or only whitespace
    const cells = row.querySelectorAll('td');
    if (cells.length === 0) return;
    const firstText = cells[0].textContent.trim();
    if (!firstText) return;

    // Skip known non-category rows
    const skipPatterns = /^(#|\d+)$|Item \/ Parameter|PRICING CALCULATOR|Client Name|Project Name|Date|Platform/i;
    if (skipPatterns.test(firstText)) return;

    // Check that all other cells are empty (category rows have only the first cell filled)
    let allEmpty = true;
    for (let i = 1; i < cells.length; i++) {
      if (cells[i].textContent.trim() !== '') {
        allEmpty = false;
        break;
      }
    }

    if (allEmpty && !categoryNames.includes(firstText)) {
      categoryNames.push(firstText);
    }
  });

  if (categoryNames.length === 0) {
    alert('⚠️ No categories found. Please add a category first using "➕ Add Category".');
    return;
  }

  // Build modal HTML
  const optionsHtml = categoryNames.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
  const modalId = 'add-item-modal-' + Date.now();

  const modalHtml = `
    <div id="${modalId}" class="modal-overlay" style="z-index:12000;">
      <div class="modal-card" style="max-width:480px;width:100%;">
        <h3 style="font-family:var(--font-serif);margin-bottom:1rem;">➕ Add New Line Item</h3>
        <div class="form-group">
          <label style="font-weight:700;font-size:0.8rem;color:var(--text-muted);">Category</label>
          <select id="${modalId}-category" class="form-control" style="margin-top:4px;">${optionsHtml}</select>
        </div>
        <div class="form-group" style="margin-top:0.75rem;">
          <label style="font-weight:700;font-size:0.8rem;color:var(--text-muted);">Item Name</label>
          <input type="text" id="${modalId}-name" class="form-control" placeholder="e.g. Payment Gateway Integration" style="margin-top:4px;">
        </div>
        <div style="display:flex;gap:0.75rem;margin-top:0.75rem;">
          <div class="form-group" style="flex:1;">
            <label style="font-weight:700;font-size:0.8rem;color:var(--text-muted);">Unit Cost (₹)</label>
            <input type="number" id="${modalId}-cost" class="form-control" value="0" min="0" step="100" style="margin-top:4px;width:100%;">
          </div>
          <div class="form-group" style="flex:1;">
            <label style="font-weight:700;font-size:0.8rem;color:var(--text-muted);">Quantity</label>
            <input type="number" id="${modalId}-qty" class="form-control" value="1" min="1" step="1" style="margin-top:4px;width:100%;">
          </div>
        </div>
        <div style="display:flex;gap:0.5rem;margin-top:1.5rem;justify-content:flex-end;">
          <button class="export-btn" onclick="document.getElementById('${modalId}').remove()">Cancel</button>
          <button class="export-btn primary" id="${modalId}-confirm">✅ Add Item</button>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);

  // Attach confirm handler
  document.getElementById(`${modalId}-confirm`).addEventListener('click', () => {
    const catName = document.getElementById(`${modalId}-category`).value;
    const itemName = document.getElementById(`${modalId}-name`).value.trim();
    const cost = parseFloat(document.getElementById(`${modalId}-cost`).value) || 0;
    const qty = parseInt(document.getElementById(`${modalId}-qty`).value, 10) || 1;

    if (!itemName) {
      alert('⚠️ Please enter an item name.');
      return;
    }

    const itemData = {
      id: 'custom_' + Date.now(),
      name: itemName,
      cost: cost,
      qty: qty,
      checked: true
    };

    // Find if there's already a custom category with this name; if not, create one
    let foundCat = false;
    const existingCatRows = tbody.querySelectorAll('tr[data-custom-category]');
    existingCatRows.forEach(catRow => {
      if (catRow.getAttribute('data-category-name') === catName) {
        // Insert item before next category header or toolbar
        renderCustomItemRowAt(tbody, itemData, catName, catRow);
        foundCat = true;
      }
    });

    if (!foundCat) {
      // Category is a built-in one — just add the item before toolbar
      renderCustomItemRowAt(tbody, itemData, catName, null);
    }

    document.getElementById(modalId).remove();
    renumberTableRows(table);
    saveCustomRowsState(table, pageSlug);
    recalculatePriceTotals();
  });

  // Close on overlay click
  document.getElementById(modalId).addEventListener('click', function(e) {
    if (e.target === this) this.remove();
  });
}

/**
 * Render a custom item row at the correct position (after a specific category header or before toolbar)
 */
function renderCustomItemRowAt(tbody, item, categoryName, afterCatRow) {
  const itemRow = document.createElement('tr');
  itemRow.setAttribute('data-custom', 'true');
  itemRow.setAttribute('data-item-id', item.id);
  itemRow.setAttribute('data-item-name', item.name);
  itemRow.setAttribute('data-category', categoryName);

  const checked = item.checked !== false;
  const cost = item.cost || 0;
  const qty = item.qty || 1;

  itemRow.innerHTML = `
    <td class="row-num">#</td>
    <td contenteditable="true" class="editable-item-name" style="min-width:150px;outline:none;border-bottom:1px dashed #cbd5e1;padding:6px;">${escapeHtml(item.name)}</td>
    <td style="color:var(--text-muted);font-size:0.85rem;">${escapeHtml(categoryName)}</td>
    <td><input type="number" class="item-cost form-control" value="${cost}" min="0" step="100" style="width:90px;padding:4px;text-align:center;"></td>
    <td><input type="number" class="item-qty form-control" value="${qty}" min="0" step="1" style="width:70px;padding:4px;text-align:center;"></td>
    <td><span class="item-row-total" style="opacity:${checked?'1':'0.4'}">₹${(checked ? cost * qty : 0).toLocaleString('en-IN')}</span></td>
    <td style="text-align:center;"><input type="checkbox" class="item-check" ${checked ? 'checked' : ''}></td>
    <td style="text-align:center;"><button class="calc-action-btn delete-item-btn" data-action="delete-item" title="Remove this line item" style="font-size:0.75rem;padding:2px 6px;color:#ef4444;">🗑️</button></td>
  `;

  const toolbar = tbody.querySelector('.calc-toolbar-row');
  if (afterCatRow) {
    // Insert after this category's last item or before next category header
    let insertAfter = afterCatRow;
    let next = afterCatRow.nextElementSibling;
    while (next && !next.hasAttribute('data-custom-category') && !next.hasAttribute('data-toolbar')) {
      insertAfter = next;
      next = next.nextElementSibling;
    }
    if (insertAfter.nextElementSibling) {
      tbody.insertBefore(itemRow, insertAfter.nextElementSibling);
    } else {
      tbody.insertBefore(itemRow, toolbar);
    }
  } else {
    tbody.insertBefore(itemRow, toolbar);
  }

  // Attach listeners
  const table = tbody.closest('table');
  const pageSlug = getPageSlug();
  itemRow.querySelectorAll('.item-check, .item-cost, .item-qty').forEach(input => {
    input.addEventListener('change', () => {
      handleItemChange(table, pageSlug);
      saveCustomRowsState(table, pageSlug);
    });
    input.addEventListener('input', () => {
      handleItemChange(table, pageSlug);
      saveCustomRowsState(table, pageSlug);
    });
  });

  const nameCell = itemRow.querySelector('.editable-item-name');
  if (nameCell) {
    nameCell.addEventListener('blur', () => {
      itemRow.setAttribute('data-item-name', nameCell.textContent.trim());
      saveCustomRowsState(table, pageSlug);
    });
  }
}

/**
 * Delete a custom category and all its items
 */
function deleteCustomCategory(btn) {
  if (!confirm('Delete this category and ALL its items? This cannot be undone.')) return;

  const catRow = btn.closest('tr');
  const table = catRow.closest('table');
  const tbody = table.querySelector('tbody');
  const pageSlug = getPageSlug();

  // Remove the category header row
  catRow.remove();

  // Remove all items belonging to this category (until next category header or toolbar)
  let next = tbody.querySelector('.calc-toolbar-row');
  // Find items between this category and next category/toolbar and remove them
  // Since we already removed the catRow, we need to find orphan items
  const allCustomRows = tbody.querySelectorAll('tr[data-custom="true"]');
  allCustomRows.forEach(row => {
    const catAttr = row.getAttribute('data-category');
    // Check if this item is orphaned (its category header is gone)
    const catHeaders = tbody.querySelectorAll(`tr[data-custom-category][data-category-name="${catAttr}"]`);
    if (catHeaders.length === 0) {
      row.remove();
    }
  });

  renumberTableRows(table);
  saveCustomRowsState(table, pageSlug);
  recalculatePriceTotals();
}

/**
 * Delete a single custom line item
 */
function deleteCustomItem(btn) {
  const row = btn.closest('tr');
  const table = row.closest('table');
  const tbody = table.querySelector('tbody');
  const pageSlug = getPageSlug();
  const categoryName = row.getAttribute('data-category');

  row.remove();

  // Check if this was the last item in its custom category — if so, also remove the category header
  if (categoryName) {
    const remainingItems = tbody.querySelectorAll(`tr[data-custom="true"][data-category="${categoryName}"]`);
    if (remainingItems.length === 0) {
      const catHeader = tbody.querySelector(`tr[data-custom-category][data-category-name="${categoryName}"]`);
      if (catHeader) catHeader.remove();
    }
  }

  renumberTableRows(table);
  saveCustomRowsState(table, pageSlug);
  recalculatePriceTotals();
}

/**
 * Re-number all rows in a pricing table
 */
function renumberTableRows(table) {
  let counter = 0;
  const allRows = table.querySelectorAll('tbody > tr');
  allRows.forEach(row => {
    const numCell = row.querySelector('.row-num');
    if (numCell) {
      counter++;
      numCell.textContent = counter;
    } else {
      // Also renumber built-in rows (first td that's just a number)
      const firstTd = row.querySelector('td:first-child');
      if (firstTd && row.hasAttribute('data-item-id') && !row.hasAttribute('data-custom')) {
        counter++;
        firstTd.textContent = counter;
      }
    }
  });
}

// Expose functions globally for onclick handlers
window.addCategoryPrompt = addCategoryPrompt;
window.addItemPrompt = addItemPrompt;
window.deleteCustomCategory = deleteCustomCategory;
window.deleteCustomItem = deleteCustomItem;
window.injectPricingTableToolbar = injectPricingTableToolbar;
window.saveCustomRowsState = saveCustomRowsState;

/**
 * Event delegation for all calc action buttons (toolbar, delete, etc.)
 * Uses data-action attributes instead of inline onclick for reliability.
 */
function initCalcActionDelegation() {
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.getAttribute('data-action');

    switch (action) {
      case 'add-category':
        if (typeof addCategoryPrompt === 'function') addCategoryPrompt(btn);
        break;
      case 'add-item':
        if (typeof addItemPrompt === 'function') addItemPrompt(btn);
        break;
      case 'delete-category':
        if (typeof deleteCustomCategory === 'function') deleteCustomCategory(btn);
        break;
      case 'delete-item':
        if (typeof deleteCustomItem === 'function') deleteCustomItem(btn);
        break;
    }
  });
}

