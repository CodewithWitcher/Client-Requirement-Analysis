/**
 * Client Proposal & Report Generator Module
 * Compiles active project state, selected requirements, line-item costs, and milestones into a printable proposal report.
 */

window.ProposalGenerator = {
  /**
   * Render complete client proposal document view inside container
   */
  renderProposal: function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const project = window.ProjectStorage.getProject();
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
            cost: itemData.cost,
            qty: itemData.qty,
            total: itemData.total
          });
        }
      });
    });

    const platformMult = (project.platform === 'Both') ? 1.4 : 1.0;
    const complexityMult = parseFloat(project.complexity || 1.0);
    const adjustedSubtotal = Math.round(totalEstimate * platformMult * complexityMult);

    const discountAmount = Math.round(adjustedSubtotal * ((project.discount || 0) / 100));
    const discountedSubtotal = adjustedSubtotal - discountAmount;

    const gstAmount = Math.round(discountedSubtotal * 0.18);
    const grandTotal = discountedSubtotal + gstAmount;

    // Milestones
    const mAdvance = Math.round(grandTotal * 0.35);
    const mDesign = Math.round(grandTotal * 0.20);
    const mDev = Math.round(grandTotal * 0.30);
    const mHandover = Math.round(grandTotal * 0.15);

    let rowsHtml = '';
    selectedLineItems.forEach((item, index) => {
      rowsHtml += `
        <tr>
          <td>${index + 1}</td>
          <td>Parameter item (${escapeHtml(item.id)})</td>
          <td>₹${(item.cost || 0).toLocaleString('en-IN')}</td>
          <td>${item.qty || 1}</td>
          <td><strong>₹${(item.total || 0).toLocaleString('en-IN')}</strong></td>
        </tr>
      `;
    });

    if (!selectedLineItems.length) {
      rowsHtml = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">No custom line-items currently selected. Open a pricing calculator page to select project scope features.</td></tr>`;
    }

    container.innerHTML = `
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
            <div><strong>Status:</strong> Draft Proposal</div>
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
            <div class="summary-row"><span>Platform & Complexity Adj:</span><span>₹${adjustedSubtotal.toLocaleString('en-IN')}</span></div>
            <div class="summary-row"><span>Discount (${project.discount || 0}%):</span><span>-₹${discountAmount.toLocaleString('en-IN')}</span></div>
            <div class="summary-row"><span>GST (18%):</span><span>₹${gstAmount.toLocaleString('en-IN')}</span></div>
            <div class="summary-row grand-total"><span>Grand Total Investment:</span><span>₹${grandTotal.toLocaleString('en-IN')}</span></div>
          </div>

          <div class="summary-card">
            <h3>Payment Milestone Schedule</h3>
            <div class="milestone-item"><span>Milestone 1: Project Kickoff & Advance (35%)</span><strong>₹${mAdvance.toLocaleString('en-IN')}</strong></div>
            <div class="milestone-item"><span>Milestone 2: Design & UI/UX Signoff (20%)</span><strong>₹${mDesign.toLocaleString('en-IN')}</strong></div>
            <div class="milestone-item"><span>Milestone 3: Core Feature Development (30%)</span><strong>₹${mDev.toLocaleString('en-IN')}</strong></div>
            <div class="milestone-item"><span>Milestone 4: QA, Deployment & Handover (15%)</span><strong>₹${mHandover.toLocaleString('en-IN')}</strong></div>
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
  }
};

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
