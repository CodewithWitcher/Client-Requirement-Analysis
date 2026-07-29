/**
 * Dynamic Client Proposal & Report Generator Module
 * Compiles active project state, selected requirements, line-item costs, GST rates, 
 * complexity multipliers, proposal dates, statuses, and custom payment milestone percentages into a live re-calculating proposal.
 * Includes interactive "How It Works & Data Sources" guidance modal.
 */

window.ProposalGenerator = {
  /**
   * Render complete client proposal document view inside container
   */
  renderProposal: function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const project = window.ProjectStorage.getProject();
    
    // Ensure default values exist
    if (project.gstRate === undefined) project.gstRate = 18;
    if (project.discount === undefined) project.discount = 0;
    if (project.complexity === undefined) project.complexity = 1.0;
    if (!project.date) project.date = new Date().toISOString().split('T')[0];
    if (!project.status) project.status = 'Draft Proposal';
    if (!project.milestones) {
      project.milestones = { kickoff: 35, design: 20, dev: 30, handover: 15 };
    }

    const standardPlatforms = ['Website', 'Android', 'iOS', 'Mobile', 'Both'];
    const isCustomPlatform = !standardPlatforms.includes(project.platform);
    const platformVal = isCustomPlatform ? 'Custom' : project.platform;
    const customPlatformText = isCustomPlatform ? project.platform : '';

    let totalEstimate = 0;
    const selectedLineItems = [];

    // Aggregate line items selected across all calculator sheets
    Object.entries(project.calculators || {}).forEach(([sheetSlug, items]) => {
      Object.entries(items).forEach(([itemId, itemData]) => {
        if (itemData.checked && itemData.total > 0) {
          totalEstimate += itemData.total;
          selectedLineItems.push({
            id: itemId,
            sheet: sheetSlug,
            name: itemData.name || itemId,
            cost: itemData.cost,
            qty: itemData.qty,
            total: itemData.total
          });
        }
      });
    });

    const platformMult = (project.platform === 'Both') ? 1.4 : (project.platform === 'Mobile' ? 1.2 : 1.0);
    const complexityMult = parseFloat(project.complexity || 1.0);
    const adjustedSubtotal = Math.round(totalEstimate * platformMult * complexityMult);

    const discountRate = parseFloat(project.discount || 0);
    const discountAmount = Math.round(adjustedSubtotal * (discountRate / 100));
    const discountedSubtotal = adjustedSubtotal - discountAmount;

    const gstRate = parseFloat(project.gstRate !== undefined ? project.gstRate : 18);
    const gstAmount = Math.round(discountedSubtotal * (gstRate / 100));
    const grandTotal = discountedSubtotal + gstAmount;

    // Custom Milestones Split
    const ms = project.milestones;
    const mKickoffPct = parseFloat(ms.kickoff !== undefined ? ms.kickoff : 35);
    const mDesignPct = parseFloat(ms.design !== undefined ? ms.design : 20);
    const mDevPct = parseFloat(ms.dev !== undefined ? ms.dev : 30);
    const mHandoverPct = parseFloat(ms.handover !== undefined ? ms.handover : 15);

    const mKickoff = Math.round(grandTotal * (mKickoffPct / 100));
    const mDesign = Math.round(grandTotal * (mDesignPct / 100));
    const mDev = Math.round(grandTotal * (mDevPct / 100));
    const mHandover = Math.round(grandTotal * (mHandoverPct / 100));

    let rowsHtml = '';
    selectedLineItems.forEach((item, index) => {
      rowsHtml += `
        <tr>
          <td>${index + 1}</td>
          <td>${escapeHtml(item.name)}</td>
          <td>₹${(item.cost || 0).toLocaleString('en-IN')}</td>
          <td>${item.qty || 1}</td>
          <td><strong>₹${(item.total || 0).toLocaleString('en-IN')}</strong></td>
        </tr>
      `;
    });

    if (!selectedLineItems.length) {
      rowsHtml = `
        <tr>
          <td colspan="5" style="padding: 2rem; background: rgba(99, 102, 241, 0.04); border: 1px dashed var(--accent-indigo);">
            <div style="text-align: center; max-width: 600px; margin: 0 auto;">
              <span style="font-size: 2rem;">💡</span>
              <h3 style="font-size: 1.1rem; color: var(--text-main); margin: 0.5rem 0;">No Custom Line-Items Selected Yet</h3>
              <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 1.25rem;">
                Proposal items are populated automatically when you check features in pricing calculators or reference guides. Click below to open a calculator and select scope items:
              </p>
              <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
                <a href="template-excel-template-website-pricing-calculator.html" class="export-btn primary" style="font-size: 0.82rem;">📊 Website Calculator</a>
                <a href="template-excel-template-application-pricing-calculator.html" class="export-btn primary" style="font-size: 0.82rem;">📊 App Calculator</a>
                <button class="export-btn" style="font-size: 0.82rem;" onclick="ProposalGenerator.openHowItWorksModal()">❓ How Proposal Data Works</button>
              </div>
            </div>
          </td>
        </tr>
      `;
    }

    container.innerHTML = `
      <!-- Interactive Metadata & Financial Controls Bar -->
      <div class="no-print" style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
          <div style="font-weight: 800; font-family: var(--font-serif); font-size: 1.1rem; color: var(--text-main);">
            Proposal Metadata & System Parameters
          </div>
          <button class="export-btn" style="padding: 0.3rem 0.75rem; font-size: 0.8rem; background: rgba(99, 102, 241, 0.1); border-color: var(--accent-indigo); color: var(--accent-indigo);" onclick="ProposalGenerator.openHowItWorksModal()">
            ❓ How Proposal Data Works & Sources
          </button>
        </div>

        <div class="form-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
          <div class="form-group">
            <label>Proposal Date:</label>
            <input type="date" class="form-control" value="${project.date}" onchange="ProposalGenerator.updateParam('date', this.value)">
          </div>

          <div class="form-group">
            <label>Proposal Status:</label>
            <select class="form-control" onchange="ProposalGenerator.updateParam('status', this.value)">
              <option value="Draft Proposal" ${project.status === 'Draft Proposal' ? 'selected' : ''}>Draft Proposal</option>
              <option value="Finalized Proposal" ${project.status === 'Finalized Proposal' ? 'selected' : ''}>Finalized Proposal</option>
              <option value="Approved Scope" ${project.status === 'Approved Scope' ? 'selected' : ''}>Approved Scope</option>
              <option value="In Execution" ${project.status === 'In Execution' ? 'selected' : ''}>In Execution</option>
            </select>
          </div>

          <div class="form-group">
            <label>Scope Platform:</label>
            <select id="proposal-platform-select" class="form-control" onchange="ProposalGenerator.handlePlatformChange(this.value)">
              <option value="Website" ${platformVal === 'Website' ? 'selected' : ''}>🌐 Website / Web App Only</option>
              <option value="Android" ${platformVal === 'Android' ? 'selected' : ''}>🤖 Android App Only</option>
              <option value="iOS" ${platformVal === 'iOS' ? 'selected' : ''}>🍎 iOS App Only</option>
              <option value="Mobile" ${platformVal === 'Mobile' ? 'selected' : ''}>📱 Both Android & iOS Mobile Apps</option>
              <option value="Both" ${platformVal === 'Both' ? 'selected' : ''}>⚡ Both Website & Mobile Apps (All Platforms)</option>
              <option value="Custom" ${platformVal === 'Custom' ? 'selected' : ''}>⚙️ Custom Platform...</option>
            </select>
            <div id="proposal-custom-platform-container" style="margin-top: 0.5rem; display: ${isCustomPlatform ? 'block' : 'none'};">
              <input type="text" id="proposal-custom-platform-input" class="form-control" placeholder="Enter Custom Platform Name" value="${escapeHtml(customPlatformText)}" onchange="ProposalGenerator.updateCustomPlatform(this.value)">
            </div>
          </div>

          <div class="form-group">
            <label>GST Tax Rate (%):</label>
            <input type="number" class="form-control" value="${gstRate}" min="0" max="30" step="1" onchange="ProposalGenerator.updateParam('gstRate', this.value)">
          </div>

          <div class="form-group">
            <label>Discount Rate (%):</label>
            <input type="number" class="form-control" value="${discountRate}" min="0" max="50" step="1" onchange="ProposalGenerator.updateParam('discount', this.value)">
          </div>

          <div class="form-group">
            <label>Complexity Multiplier:</label>
            <select class="form-control" onchange="ProposalGenerator.updateParam('complexity', this.value)">
              <option value="1.0" ${complexityMult === 1.0 ? 'selected' : ''}>1.0x — Standard Scope</option>
              <option value="1.2" ${complexityMult === 1.2 ? 'selected' : ''}>1.2x — Medium Complexity</option>
              <option value="1.5" ${complexityMult === 1.5 ? 'selected' : ''}>1.5x — Enterprise Scale</option>
            </select>
          </div>
        </div>

        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed rgba(99, 102, 241, 0.2);">
          <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-subtle); margin-bottom: 0.5rem;">Custom Milestone Payment Splits (%):</div>
          <div class="form-grid" style="grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem;">
            <div class="form-group">
              <label>1. Advance Kickoff (%):</label>
              <input type="number" class="form-control" value="${mKickoffPct}" min="0" max="100" onchange="ProposalGenerator.updateMilestone('kickoff', this.value)">
            </div>
            <div class="form-group">
              <label>2. UI/UX Design (%):</label>
              <input type="number" class="form-control" value="${mDesignPct}" min="0" max="100" onchange="ProposalGenerator.updateMilestone('design', this.value)">
            </div>
            <div class="form-group">
              <label>3. Development (%):</label>
              <input type="number" class="form-control" value="${mDevPct}" min="0" max="100" onchange="ProposalGenerator.updateMilestone('dev', this.value)">
            </div>
            <div class="form-group">
              <label>4. Handover (%):</label>
              <input type="number" class="form-control" value="${mHandoverPct}" min="0" max="100" onchange="ProposalGenerator.updateMilestone('handover', this.value)">
            </div>
          </div>
        </div>
      </div>

      <div class="proposal-document">
        <!-- Proposal Header -->
        <div class="proposal-header-banner">
          <div>
            <span class="badge badge-docx">CLIENT PROPOSAL & REQUIREMENT REPORT</span>
            <h1 style="margin-top: 0.5rem; font-size: 2.2rem;">${escapeHtml(project.projectName)}</h1>
            <p style="color: var(--text-muted); font-size: 1rem;">Prepared for <strong>${escapeHtml(project.clientName)}</strong> by <strong>${escapeHtml(project.preparedBy)}</strong></p>
          </div>
          <div style="text-align: right; font-size: 0.9rem; color: var(--text-subtle);">
            <div><strong>Date:</strong> ${project.date}</div>
            <div><strong>Scope:</strong> ${project.platform} Platform</div>
            <div><strong>Status:</strong> ${escapeHtml(project.status)}</div>
          </div>
        </div>

        <!-- Executive Summary -->
        <div class="proposal-section">
          <h2>1. Executive Summary & Scope</h2>
          <p>
            This proposal outlines the functional parameters, design deliverables, technical specifications, and estimated pricing for 
            <strong>${escapeHtml(project.projectName)}</strong>. The scoping model accounts for targeted platform optimization, security, analytics, and quality assurance.
          </p>
        </div>

        <!-- Selected Requirements & Pricing Table -->
        <div class="proposal-section">
          <h2>2. Functional Deliverables & Pricing Breakdown</h2>
          <div class="table-responsive">
            <table class="doc-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Deliverable / Parameter</th>
                  <th>Unit Rate (₹)</th>
                  <th>Qty</th>
                  <th>Total (₹)</th>
                </tr>
              </thead>
              <tbody>
                ${rowsHtml}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Summary Totals -->
        <div class="proposal-summary-grid">
          <div class="summary-card">
            <h3>Investment Summary</h3>
            <div class="summary-row"><span>Base Scope Subtotal:</span><span>₹${totalEstimate.toLocaleString('en-IN')}</span></div>
            <div class="summary-row"><span>Platform (${project.platform}) & Complexity (${complexityMult}x):</span><span>₹${adjustedSubtotal.toLocaleString('en-IN')}</span></div>
            <div class="summary-row"><span>Discount (${discountRate}%):</span><span>-₹${discountAmount.toLocaleString('en-IN')}</span></div>
            <div class="summary-row"><span>GST (${gstRate}%):</span><span>₹${gstAmount.toLocaleString('en-IN')}</span></div>
            <div class="summary-row grand-total"><span>Grand Total Investment:</span><span>₹${grandTotal.toLocaleString('en-IN')}</span></div>
          </div>

          <div class="summary-card">
            <h3>Payment Milestone Schedule</h3>
            <div class="milestone-item"><span>Milestone 1: Project Kickoff & Advance (${mKickoffPct}%)</span><strong>₹${mKickoff.toLocaleString('en-IN')}</strong></div>
            <div class="milestone-item"><span>Milestone 2: Design & UI/UX Signoff (${mDesignPct}%)</span><strong>₹${mDesign.toLocaleString('en-IN')}</strong></div>
            <div class="milestone-item"><span>Milestone 3: Core Feature Development (${mDevPct}%)</span><strong>₹${mDev.toLocaleString('en-IN')}</strong></div>
            <div class="milestone-item"><span>Milestone 4: QA, Deployment & Handover (${mHandoverPct}%)</span><strong>₹${mHandover.toLocaleString('en-IN')}</strong></div>
          </div>
        </div>

        <!-- Terms & Acceptance -->
        <div class="proposal-section" style="margin-top: 2rem;">
          <h2>3. Acceptance & Sign-off</h2>
          <p>Upon acceptance of this scope of work, client authorization will initiate Phase 1 project onboarding.</p>
          
          <div style="display: flex; justify-content: space-between; margin-top: 3rem; gap: 2rem;">
            <div style="flex: 1; border-top: 1px solid #cbd5e1; padding-top: 0.5rem; text-align: center;">
              <strong>${escapeHtml(project.clientName)}</strong><br>Client Representative
            </div>
            <div style="flex: 1; border-top: 1px solid #cbd5e1; padding-top: 0.5rem; text-align: center;">
              <strong>${escapeHtml(project.preparedBy)}</strong><br>Authorized Lead
            </div>
          </div>
        </div>
      </div>
    `;
  },

  /**
   * Guidance Modal: How Proposal Builder Works & Data Sources
   */
  openHowItWorksModal: function() {
    const modalHtml = `
      <div id="proposal-help-overlay" class="modal-overlay">
        <div class="modal-card" style="max-width: 680px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0;">
            <h3 style="font-family: var(--font-serif); font-size: 1.3rem;">💡 How Proposal Builder Works & Data Sources</h3>
            <button class="export-btn" onclick="document.getElementById('proposal-help-overlay').remove()">✕ Close</button>
          </div>

          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.25rem;">
            The <strong>Interactive Proposal Builder</strong> aggregates live data from your client workspace. When you select features or check items in pricing calculators or requirement guides, they automatically flow into this proposal document!
          </p>

          <h4 style="font-size: 1rem; margin-bottom: 0.75rem; color: var(--text-main);">🔗 Direct Links to Data Source Pages:</h4>
          
          <div style="display: grid; gap: 0.75rem; margin-bottom: 1.5rem;">
            <a href="template-excel-template-website-pricing-calculator.html" class="explorer-item" style="text-decoration: none;">
              <div>
                <strong style="color: var(--text-main);">📊 Website Pricing Calculator</strong>
                <div style="font-size: 0.8rem; color: var(--text-subtle);">Check website features & cost items to populate website proposal lines</div>
              </div>
              <span class="badge badge-xlsx">XLSX</span>
            </a>

            <a href="template-excel-template-application-pricing-calculator.html" class="explorer-item" style="text-decoration: none;">
              <div>
                <strong style="color: var(--text-main);">📊 Application Pricing Calculator</strong>
                <div style="font-size: 0.8rem; color: var(--text-subtle);">Check mobile app features & cost items to populate app proposal lines</div>
              </div>
              <span class="badge badge-xlsx">XLSX</span>
            </a>

            <a href="docs-website-website-requirements-complete-guide.html" class="explorer-item" style="text-decoration: none;">
              <div>
                <strong style="color: var(--text-main);">📖 Website Requirements Guide</strong>
                <div style="font-size: 0.8rem; color: var(--text-subtle);">Click "+ Add to Scope" on specific website requirement sections</div>
              </div>
              <span class="badge badge-md">MD</span>
            </a>

            <a href="docs-application-application-requirements-complete-guide.html" class="explorer-item" style="text-decoration: none;">
              <div>
                <strong style="color: var(--text-main);">📖 Application Requirements Guide</strong>
                <div style="font-size: 0.8rem; color: var(--text-subtle);">Click "+ Add to Scope" on specific mobile app requirement sections</div>
              </div>
              <span class="badge badge-md">MD</span>
            </a>

            <a href="ai-intelligence-engine.html" class="explorer-item" style="text-decoration: none; background: rgba(99, 102, 241, 0.04); border-color: rgba(99, 102, 241, 0.3);">
              <div>
                <strong style="color: var(--accent-indigo);">🧠 AI Technical Intelligence Studio</strong>
                <div style="font-size: 0.8rem; color: var(--text-subtle);">Upload client requirement PDF to generate AI architecture & auto-fill scope</div>
              </div>
              <span class="badge badge-md" style="background: var(--accent-indigo); color: #fff;">AI STUDIO</span>
            </a>
          </div>

          <h4 style="font-size: 1rem; margin-bottom: 0.5rem; color: var(--text-main);">⚡ 3-Step Simple Workflow:</h4>
          <ol style="padding-left: 1.25rem; font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">
            <li>Visit any of the calculator or guide pages linked above.</li>
            <li>Check the boxes for the features your client needs.</li>
            <li>Return to <strong>Proposal Builder</strong> — your tailored proposal, GST rates, and milestones will automatically update!</li>
          </ol>

          <div style="display: flex; justify-content: flex-end; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
            <button class="export-btn primary" onclick="document.getElementById('proposal-help-overlay').remove()">Got it! Close Guide</button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
  },

  handlePlatformChange(val) {
    const container = document.getElementById('proposal-custom-platform-container');
    if (container) {
      container.style.display = (val === 'Custom') ? 'block' : 'none';
    }
    if (val !== 'Custom') {
      this.updateParam('platform', val);
    } else {
      const customText = document.getElementById('proposal-custom-platform-input')?.value.trim() || 'Custom';
      this.updateParam('platform', customText);
    }
  },

  updateCustomPlatform(val) {
    this.updateParam('platform', val.trim() || 'Custom');
  },

  /**
   * Update single parameter and trigger real-time proposal re-render
   */
  updateParam: function(param, val) {
    if (window.ProjectStorage) {
      const proj = window.ProjectStorage.getProject();
      proj[param] = val;
      window.ProjectStorage.saveProject(proj);
      this.renderProposal('proposal-output-container');
      if (window.showToast) window.showToast(`Updated proposal ${param}!`, 'info');
    }
  },

  /**
   * Update milestone split percentage
   */
  updateMilestone: function(mKey, val) {
    if (window.ProjectStorage) {
      const proj = window.ProjectStorage.getProject();
      if (!proj.milestones) proj.milestones = { kickoff: 35, design: 20, dev: 30, handover: 15 };
      proj.milestones[mKey] = parseFloat(val) || 0;
      window.ProjectStorage.saveProject(proj);
      this.renderProposal('proposal-output-container');
      if (window.showToast) window.showToast('Updated milestone payment schedule!', 'info');
    }
  }
};

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
