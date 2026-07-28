/**
 * Smart Recommendation Assistant & AI Requirement Document Analyzer
 * 1. Wizard-style Smart Tool Recommender based on user goals
 * 2. Client Requirement Document Parser (DeepSeek API + Heuristic Keyword Engine)
 * 3. Client-Provided API Key Manager (LocalStorage Persistent & Test Connection)
 */

window.SmartAssistant = {
  // Recommendation Catalog
  catalog: {
    web_questionnaire: {
      title: "Website Client Questionnaire",
      slug: "questionnaire-website-website-client-questionnaire",
      type: "MD",
      desc: "Perfect for initial discovery calls with website clients to gather business goals, pages, and feature needs."
    },
    web_calculator: {
      title: "Website Pricing Calculator",
      slug: "template-excel-template-website-pricing-calculator",
      type: "XLSX",
      desc: "Interactive spreadsheet to calculate itemized website costs, GST (18%), discount, and 4-phase payment milestone splits."
    },
    web_proposal: {
      title: "Website Client Proposal",
      slug: "template-word-template-website-client-proposal",
      type: "DOCX",
      desc: "Formal client proposal template for website development projects."
    },
    web_checklist: {
      title: "Website Project Checklist",
      slug: "checklists-website-project-checklist",
      type: "MD",
      desc: "Step-by-step checklist covering pre-project kickoff, design, build, and handover tasks."
    },
    web_guide: {
      title: "Website Requirements Complete Guide",
      slug: "docs-website-website-requirements-complete-guide",
      type: "MD",
      desc: "Master reference guide covering domain, hosting, SSL, tech stack, and e-commerce parameters."
    },

    app_questionnaire: {
      title: "Application Client Questionnaire",
      slug: "questionnaire-application-application-client-questionnaire",
      type: "MD",
      desc: "Tailored discovery questionnaire for mobile app (iOS/Android) client interviews."
    },
    app_calculator: {
      title: "Application Pricing Calculator",
      slug: "template-excel-template-application-pricing-calculator",
      type: "XLSX",
      desc: "Interactive pricing calculator for mobile apps, push notifications, auth, and API backends."
    },
    app_proposal: {
      title: "Application Client Proposal",
      slug: "template-word-template-application-client-proposal",
      type: "DOCX",
      desc: "Formal client proposal template for mobile application projects."
    },
    app_checklist: {
      title: "Application Project Checklist",
      slug: "checklists-application-project-checklist",
      type: "MD",
      desc: "Step-by-step task checklist for iOS & Android mobile app delivery lifecycles."
    },
    app_guide: {
      title: "Application Requirements Complete Guide",
      slug: "docs-application-application-requirements-complete-guide",
      type: "MD",
      desc: "Master reference guide covering mobile OS, cross-platform vs native, backend APIs, and app store compliance."
    }
  },

  // DeepSeek API Configuration (Stored locally in client browser)
  deepseekApiKey: localStorage.getItem('deepseek_api_key') || '',

  setApiKey(key) {
    this.deepseekApiKey = (key || '').trim();
    if (this.deepseekApiKey) {
      localStorage.setItem('deepseek_api_key', this.deepseekApiKey);
      if (window.showToast) window.showToast('DeepSeek API Key saved securely in your browser!', 'success');
    } else {
      localStorage.removeItem('deepseek_api_key');
      if (window.showToast) window.showToast('DeepSeek API Key cleared.', 'info');
    }
  },

  getApiKey() {
    return this.deepseekApiKey || localStorage.getItem('deepseek_api_key') || '';
  },

  /**
   * Recommend exact tool based on platform and intent
   */
  getRecommendation(platform, intent) {
    if (platform === 'web') {
      if (intent === 'interview') return this.catalog.web_questionnaire;
      if (intent === 'pricing') return this.catalog.web_calculator;
      if (intent === 'proposal') return this.catalog.web_proposal;
      if (intent === 'checklist') return this.catalog.web_checklist;
      return this.catalog.web_guide;
    } else {
      if (intent === 'interview') return this.catalog.app_questionnaire;
      if (intent === 'pricing') return this.catalog.app_calculator;
      if (intent === 'proposal') return this.catalog.app_proposal;
      if (intent === 'checklist') return this.catalog.app_checklist;
      return this.catalog.app_guide;
    }
  },

  /**
   * Client-side Requirement Document Parser
   */
  async analyzeDocumentFile(file, clientName, projectTitle) {
    const text = await this.extractTextFromFile(file);
    if (!text || text.length < 10) {
      alert("Could not extract readable text from the uploaded document.");
      return;
    }

    if (window.showToast) window.showToast("Analyzing client requirements...", "info");

    let matchedAnalysis = null;
    const apiKey = this.getApiKey();

    if (apiKey) {
      try {
        matchedAnalysis = await this.callDeepSeekAPI(text, apiKey);
      } catch (err) {
        console.warn("DeepSeek API Call failed, falling back to local analysis engine:", err);
        if (window.showToast) window.showToast("DeepSeek API call failed. Using built-in rule engine fallback.", "warning");
        matchedAnalysis = this.heuristicAnalysisEngine(text);
      }
    } else {
      matchedAnalysis = this.heuristicAnalysisEngine(text);
    }

    // Save to ProjectStorage
    if (window.ProjectStorage) {
      const proj = window.ProjectStorage.getProject();
      if (clientName) proj.clientName = clientName;
      if (projectTitle) proj.projectTitle = projectTitle;
      proj.aiAnalysis = matchedAnalysis;
      
      // Auto-check matched line items in active workspace
      if (matchedAnalysis.matchedItems && matchedAnalysis.matchedItems.length > 0) {
        matchedAnalysis.matchedItems.forEach(itemId => {
          proj.checkedItems[itemId] = true;
        });
      }

      window.ProjectStorage.saveProject(proj);
    }

    this.renderAnalysisResultModal(matchedAnalysis, clientName, projectTitle);
  },

  /**
   * Extract raw text from file (.txt, .md, .json, .docx)
   */
  extractTextFromFile(file) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        resolve(e.target.result || '');
      };
      reader.readAsText(file);
    });
  },

  /**
   * Call DeepSeek API (https://api.deepseek.com/v1/chat/completions)
   */
  async callDeepSeekAPI(documentText, apiKey) {
    const prompt = `You are a Senior Technical Project Estimator. Analyze this client requirement document and extract key features, recommended tech stack, estimated complexity (Low, Medium, High), and line-item requirement tags.

Client Document Text:
"""
${documentText.slice(0, 4000)}
"""

Return JSON format strictly:
{
  "summary": "Brief 2-line summary of client project scope",
  "projectType": "Website or Mobile App",
  "recommendedStack": ["React", "Node.js", "PostgreSQL", "Tailwind"],
  "complexityMultiplier": 1.2,
  "keyFeaturesExtracted": ["User Authentication", "Payment Gateway", "Admin Dashboard", "Push Notifications"],
  "matchedItems": ["item_1", "item_7", "item_12", "item_25", "item_40"]
}`;

    const res = await fetch("https://api.deepseek.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: "deepseek-chat",
        messages: [{ role: "user", content: prompt }],
        response_format: { type: "json_object" }
      })
    });

    if (!res.ok) throw new Error(`DeepSeek API returned HTTP ${res.status}`);
    const data = await res.json();
    return JSON.parse(data.choices[0].message.content);
  },

  /**
   * Built-in Heuristic Analysis Engine (Fallback when no DeepSeek key provided)
   */
  heuristicAnalysisEngine(text) {
    const lowerText = text.toLowerCase();
    const isMobile = lowerText.includes('app') || lowerText.includes('ios') || lowerText.includes('android') || lowerText.includes('flutter');
    const isWeb = lowerText.includes('website') || lowerText.includes('dashboard') || lowerText.includes('web');

    const keyFeatures = [];
    const matchedItems = [];
    let complexity = 1.0;

    if (lowerText.includes('auth') || lowerText.includes('login') || lowerText.includes('signup')) {
      keyFeatures.push('User Authentication & Role Management');
      matchedItems.push('item_7');
    }
    if (lowerText.includes('payment') || lowerText.includes('stripe') || lowerText.includes('razorpay')) {
      keyFeatures.push('Payment Gateway Integration');
      matchedItems.push('item_12');
      complexity += 0.15;
    }
    if (lowerText.includes('e-commerce') || lowerText.includes('cart') || lowerText.includes('checkout') || lowerText.includes('product')) {
      keyFeatures.push('E-Commerce & Product Catalog');
      matchedItems.push('item_18');
      complexity += 0.25;
    }
    if (lowerText.includes('admin') || lowerText.includes('dashboard') || lowerText.includes('cms')) {
      keyFeatures.push('Admin Control Panel & Analytics');
      matchedItems.push('item_25');
    }
    if (lowerText.includes('push') || lowerText.includes('notification')) {
      keyFeatures.push('Push Notification Service');
      matchedItems.push('item_32');
    }
    if (lowerText.includes('seo') || lowerText.includes('google')) {
      keyFeatures.push('SEO Optimization & Analytics Setup');
      matchedItems.push('item_40');
    }

    if (!keyFeatures.length) {
      keyFeatures.push('Standard Requirement Scope Gathering', 'Core UI/UX Page Layouts', 'Database Architecture Setup');
      matchedItems.push('item_1', 'item_7', 'item_12');
    }

    return {
      summary: `Analyzed client document containing ${text.split(' ').length} words. Extracted ${keyFeatures.length} core requirement modules.`,
      projectType: isMobile ? 'Mobile Application (iOS/Android)' : (isWeb ? 'Website / Web App' : 'Full-Stack Solution'),
      recommendedStack: isMobile ? ['Flutter / React Native', 'Node.js', 'PostgreSQL', 'Firebase'] : ['Next.js / React', 'Node.js', 'MongoDB / Postgres', 'Stripe'],
      complexityMultiplier: parseFloat(complexity.toFixed(2)),
      keyFeaturesExtracted: keyFeatures,
      matchedItems: matchedItems
    };
  },

  /**
   * Render Analysis Modal
   */
  renderAnalysisResultModal(analysis, clientName, projectTitle) {
    const modalHtml = `
      <div id="ai-analysis-overlay" class="modal-overlay">
        <div class="modal-card" style="max-width: 720px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0;">
            <h3>🤖 AI Client Requirement Analysis Report</h3>
            <button class="export-btn" onclick="document.getElementById('ai-analysis-overlay').remove()">✕ Close</button>
          </div>

          <div style="background: rgba(59, 130, 246, 0.06); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid rgba(59, 130, 246, 0.2);">
            <div style="font-weight: 700; font-size: 1.1rem; color: var(--text-main); margin-bottom: 0.35rem;">
              Client: ${this.escapeHtml(clientName || 'Unassigned Client')} • ${this.escapeHtml(projectTitle || 'New Project Scope')}
            </div>
            <p style="font-size: 0.92rem; color: var(--text-muted);">${this.escapeHtml(analysis.summary)}</p>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: #f8fafc; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0;">
              <span style="font-size: 0.75rem; font-weight: 700; color: var(--text-subtle); text-transform: uppercase;">Project Classification</span>
              <div style="font-weight: 800; font-size: 1.05rem; margin-top: 0.25rem;">${this.escapeHtml(analysis.projectType)}</div>
            </div>
            <div style="background: #f8fafc; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0;">
              <span style="font-size: 0.75rem; font-weight: 700; color: var(--text-subtle); text-transform: uppercase;">Complexity Multiplier</span>
              <div style="font-weight: 800; font-size: 1.05rem; margin-top: 0.25rem; color: var(--accent-indigo);">${analysis.complexityMultiplier}x Multiplier</div>
            </div>
          </div>

          <div style="margin-bottom: 1.5rem;">
            <h4 style="font-size: 1rem; margin-bottom: 0.5rem;">Extracted Core Feature Requirements:</h4>
            <ul style="padding-left: 1.25rem; font-size: 0.92rem; color: var(--text-main);">
              ${analysis.keyFeaturesExtracted.map(f => `<li style="margin-bottom: 0.35rem;"><strong>✓ ${this.escapeHtml(f)}</strong></li>`).join('')}
            </ul>
          </div>

          <div style="margin-bottom: 1.5rem;">
            <h4 style="font-size: 1rem; margin-bottom: 0.5rem;">Recommended Technical Stack:</h4>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              ${analysis.recommendedStack.map(s => `<span class="badge badge-md">${this.escapeHtml(s)}</span>`).join('')}
            </div>
          </div>

          <div style="display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
            <a href="pages/interactive-proposal-builder.html" class="export-btn primary">✨ Open Proposal Builder with This Scope</a>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
  },

  /**
   * Modal Dialog for Managing Client-Provided DeepSeek API Key
   */
  openApiKeyModal() {
    const existingKey = this.getApiKey();
    const hasKey = !!existingKey;

    const modalHtml = `
      <div id="api-key-overlay" class="modal-overlay">
        <div class="modal-card" style="max-width: 540px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0;">
            <h3>🔑 Configure DeepSeek API Key</h3>
            <button class="export-btn" onclick="document.getElementById('api-key-overlay').remove()">✕ Close</button>
          </div>

          <div style="background: ${hasKey ? 'rgba(16, 185, 129, 0.08)' : 'rgba(245, 158, 11, 0.08)'}; border: 1px solid ${hasKey ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.3)'}; padding: 0.85rem 1.25rem; border-radius: 10px; margin-bottom: 1.25rem; font-size: 0.88rem; display: flex; align-items: center; justify-content: space-between;">
            <div>
              <span style="font-weight: 700;">Active AI Status:</span>
              <span style="color: ${hasKey ? 'var(--accent-emerald)' : 'var(--accent-amber)'}; font-weight: 700;">
                ${hasKey ? '🟢 Client API Key Saved' : '⚪ Using Built-in Free Rule Engine'}
              </span>
            </div>
          </div>

          <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.25rem; line-height: 1.5;">
            Enter your personal DeepSeek API key (e.g. <code>sk-...</code>). Your key is stored <strong>100% locally in your own browser's LocalStorage</strong> and is never sent to any server except directly to <code>api.deepseek.com</code>.
          </p>

          <div class="form-group" style="margin-bottom: 1.25rem;">
            <label>DeepSeek API Key:</label>
            <div style="position: relative;">
              <input type="password" id="modal-deepseek-key-input" class="form-control" placeholder="sk-..." value="${this.escapeHtml(existingKey)}" style="padding-right: 4.5rem;">
              <button class="export-btn" style="position: absolute; right: 4px; top: 4px; padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="toggleApiKeyVisibility()">👁️ Show</button>
            </div>
          </div>

          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: flex-end; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
            ${hasKey ? '<button class="export-btn" style="color: #ef4444; border-color: #ef4444;" onclick="clearApiKeyFromModal()">🗑️ Clear Saved Key</button>' : ''}
            <button class="export-btn" onclick="testApiKeyFromModal()">🧪 Test Connection</button>
            <button class="export-btn primary" onclick="saveApiKeyFromModal()">💾 Save API Key</button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
  },

  escapeHtml(str) {
    return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
};

function toggleApiKeyVisibility() {
  const input = document.getElementById('modal-deepseek-key-input');
  if (input) {
    input.type = input.type === 'password' ? 'text' : 'password';
  }
}

function saveApiKeyFromModal() {
  const input = document.getElementById('modal-deepseek-key-input');
  if (input) {
    window.SmartAssistant.setApiKey(input.value);
    document.getElementById('api-key-overlay')?.remove();
  }
}

function clearApiKeyFromModal() {
  window.SmartAssistant.setApiKey('');
  document.getElementById('api-key-overlay')?.remove();
}

async function testApiKeyFromModal() {
  const input = document.getElementById('modal-deepseek-key-input');
  const key = input ? input.value.trim() : '';

  if (!key) {
    alert("Please enter an API key to test.");
    return;
  }

  if (window.showToast) window.showToast("Testing DeepSeek API connection...", "info");

  try {
    const res = await fetch("https://api.deepseek.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${key}`
      },
      body: JSON.stringify({
        model: "deepseek-chat",
        messages: [{ role: "user", content: "Reply with JSON: {\"status\": \"ok\"}" }],
        response_format: { type: "json_object" }
      })
    });

    if (res.ok) {
      alert("✅ DeepSeek API Key connection successful!");
    } else {
      alert(`❌ API Key test failed (HTTP ${res.status}). Please check your key.`);
    }
  } catch (err) {
    alert(`❌ Network or API Key error: ${err.message}`);
  }
}
