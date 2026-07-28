/**
 * Smart Recommendation Assistant & AI Requirement Document Analyzer
 * 1. Wizard-style Smart Tool Recommender based on user goals
 * 2. Client Requirement Document Parser (DeepSeek API + Heuristic Keyword Engine)
 * 3. Client-Provided API Key Manager (LocalStorage Persistent & Test Connection)
 * 4. Floating Robot Chatbot Widget & Slide-Out AI Side Drawer
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
    this.updateHeaderApiKeyStatus();
  },

  getApiKey() {
    return this.deepseekApiKey || localStorage.getItem('deepseek_api_key') || '';
  },

  updateHeaderApiKeyStatus() {
    const key = this.getApiKey();
    const hasKey = !!(key && key.trim().length > 0);

    const btns = document.querySelectorAll('#header-api-key-btn, .api-key-btn, .header-api-key-btn, button[onclick*="openApiKeyModal"]');
    btns.forEach(btn => {
      btn.classList.add('header-api-key-btn');
      btn.onclick = (e) => {
        if (e) e.preventDefault();
        window.SmartAssistant.openApiKeyModal();
      };

      if (hasKey) {
        btn.innerHTML = '🟢 DeepSeek API Saved';
        btn.style.background = 'rgba(16, 185, 129, 0.15)';
        btn.style.borderColor = '#10b981';
        btn.style.color = '#059669';
        btn.style.fontWeight = '700';
      } else {
        btn.innerHTML = '🔑 DeepSeek Key';
        btn.style.background = '';
        btn.style.borderColor = '';
        btn.style.color = '';
        btn.style.fontWeight = '';
      }
    });
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
   * Call DeepSeek API
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
   * Built-in Heuristic Analysis Engine
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
    document.getElementById('ai-analysis-overlay')?.remove();
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
    document.getElementById('api-key-overlay')?.remove();
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

  /**
   * Render Floating Robot Chatbot Button & Welcome Speech Bubble
   */
  renderFloatingRobotWidget() {
    if (document.getElementById('floating-robot-btn')) return;

    const widgetHtml = `
      <div id="floating-robot-bubble" style="${sessionStorage.getItem('dismiss_robot_bubble') ? 'display:none;' : ''}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.25rem;">
          <strong style="color: var(--accent-indigo, #6366f1); font-size: 0.9rem;">🤖 AI Workspace Assistant</strong>
          <button style="background: none; border: none; font-size: 0.8rem; cursor: pointer; color: #64748b;" onclick="dismissRobotBubble(event)">✕</button>
        </div>
        <div>Need help scoping a project or analyzing a requirement document? Click me for AI recommendations & file analysis!</div>
      </div>

      <button id="floating-robot-btn" onclick="window.SmartAssistant.openAiSideDrawer()" title="Open AI Assistant Studio">
        <div class="robot-pulse-ring"></div>
        🤖
      </button>
    `;

    document.body.insertAdjacentHTML('beforeend', widgetHtml);
  },

  /**
   * Open Slide-out AI Side Drawer
   */
  openAiSideDrawer() {
    document.getElementById('floating-robot-bubble')?.remove();
    document.getElementById('ai-drawer-overlay')?.remove();

    const isPage = window.location.pathname.includes('/pages/');
    const prefix = isPage ? '' : 'pages/';

    const hasKey = !!this.getApiKey();

    const drawerHtml = `
      <div id="ai-drawer-overlay" class="ai-drawer-overlay" onclick="closeAiSideDrawer(event)">
        <div class="ai-drawer-card" onclick="event.stopPropagation()">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span style="font-size: 1.5rem;">🤖</span>
              <div>
                <h3 style="margin: 0; font-family: var(--font-serif); font-size: 1.2rem;">AI Assistant & Tools Studio</h3>
                <span style="font-size: 0.75rem; color: ${hasKey ? 'var(--accent-emerald)' : 'var(--accent-amber)'}; font-weight: 700;">
                  ${hasKey ? '🟢 Client API Key Saved' : '⚪ Using Free Rule Engine'}
                </span>
              </div>
            </div>
            <button class="export-btn" onclick="closeAiSideDrawer()">✕ Close</button>
          </div>

          <!-- Section 1: Step-by-Step Recommender -->
          <div style="background: #f8fafc; padding: 1.25rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
            <h4 style="font-size: 1rem; color: var(--text-main); margin-bottom: 0.75rem;">🎯 Step-by-Step Tool Recommender</h4>
            
            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label style="font-size: 0.8rem;">Project Type:</label>
              <select id="drawer-wizard-platform" class="form-control" style="font-size: 0.85rem;">
                <option value="web">🌐 Website / Web Application</option>
                <option value="app">📱 Mobile Application (iOS/Android)</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label style="font-size: 0.8rem;">Primary Goal:</label>
              <select id="drawer-wizard-intent" class="form-control" style="font-size: 0.85rem;">
                <option value="pricing">💰 Calculate Pricing & Costs</option>
                <option value="interview">📋 Client Discovery Questionnaire</option>
                <option value="proposal">📝 Generate Formal Proposal</option>
                <option value="checklist">✅ Project Lifecycle Checklist</option>
                <option value="guide">📖 Complete Requirement Guide</option>
              </select>
            </div>

            <button class="export-btn primary" style="width: 100%; justify-content: center; font-size: 0.85rem; padding: 0.5rem;" onclick="handleDrawerRecommend()">
              🚀 Recommend & Open Tool
            </button>

            <div id="drawer-recommend-output" style="margin-top: 0.75rem; display: none;"></div>
          </div>

          <!-- Section 2: AI Document Analyzer -->
          <div style="background: #f8fafc; padding: 1.25rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
              <h4 style="font-size: 1rem; color: var(--text-main); margin: 0;">📄 AI Document Requirement Analyzer</h4>
              <button class="export-btn" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" onclick="window.SmartAssistant.openApiKeyModal()">🔑 Key</button>
            </div>

            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label style="font-size: 0.8rem;">Upload Client Requirement File (.txt, .md, .docx, .json):</label>
              <input type="file" id="drawer-ai-file-input" class="form-control" accept=".txt,.md,.docx,.json" style="font-size: 0.8rem;">
            </div>

            <div class="form-group" style="margin-bottom: 0.85rem;">
              <label style="font-size: 0.8rem;">Client / Project Title:</label>
              <input type="text" id="drawer-ai-client-title" class="form-control" placeholder="e.g. Acme App" style="font-size: 0.85rem;">
            </div>

            <button class="export-btn" style="width: 100%; justify-content: center; background: var(--accent-indigo, #6366f1); color: #fff; border-color: var(--accent-indigo, #6366f1); font-size: 0.85rem; padding: 0.5rem;" onclick="handleDrawerAiAnalyze()">
              🤖 Analyze Document & Match Features
            </button>
          </div>

          <!-- Section 3: Deep Technical Architecture Studio -->
          <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(59, 130, 246, 0.04)); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.3);">
            <h4 style="font-size: 1rem; color: var(--accent-indigo, #6366f1); margin-bottom: 0.5rem;">🧠 AI Technical Intelligence Studio</h4>
            <p style="font-size: 0.82rem; color: var(--text-muted, #64748b); line-height: 1.5; margin-bottom: 0.85rem;">
              Generate complete Technical Architecture Specs, Deployment Pipelines, SEO Reports, REST API Contracts, and Risk Matrices automatically.
            </p>
            <a href="${prefix}ai-intelligence-engine.html" class="export-btn primary" style="width: 100%; justify-content: center; font-size: 0.85rem; background: var(--accent-indigo, #6366f1); border-color: var(--accent-indigo, #6366f1); text-decoration: none;">
              ⚡ Launch Deep AI Technical Studio
            </a>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', drawerHtml);
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

function dismissRobotBubble(e) {
  if (e) e.stopPropagation();
  sessionStorage.setItem('dismiss_robot_bubble', 'true');
  document.getElementById('floating-robot-bubble')?.remove();
}

function closeAiSideDrawer(e) {
  if (e && e.target && e.target.id !== 'ai-drawer-overlay' && !e.target.classList.contains('export-btn')) {
    return;
  }
  document.getElementById('ai-drawer-overlay')?.remove();
}

function handleDrawerRecommend() {
  const plat = document.getElementById('drawer-wizard-platform').value;
  const intent = document.getElementById('drawer-wizard-intent').value;
  const rec = window.SmartAssistant.getRecommendation(plat, intent);
  const out = document.getElementById('drawer-recommend-output');

  const isPage = window.location.pathname.includes('/pages/');
  const prefix = isPage ? '' : 'pages/';

  out.style.display = 'block';
  out.innerHTML = `
    <div style="background: rgba(16, 185, 129, 0.08); padding: 0.85rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3);">
      <div style="font-weight: 700; color: var(--accent-emerald); font-size: 0.88rem;">Recommended: ${rec.title}</div>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0.25rem 0 0.5rem 0;">${rec.desc}</p>
      <a href="${prefix}${rec.slug}.html" class="export-btn primary" style="font-size: 0.78rem; padding: 0.35rem 0.65rem;">🚀 Open ${rec.title}</a>
    </div>
  `;
}

async function handleDrawerAiAnalyze() {
  const fileInput = document.getElementById('drawer-ai-file-input');
  const clientTitle = document.getElementById('drawer-ai-client-title').value.trim();

  if (!fileInput.files || !fileInput.files[0]) {
    alert("Please select a client requirement document file first.");
    return;
  }

  closeAiSideDrawer();
  await window.SmartAssistant.analyzeDocumentFile(fileInput.files[0], clientTitle, clientTitle);
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.SmartAssistant) {
    window.SmartAssistant.updateHeaderApiKeyStatus();
    window.SmartAssistant.renderFloatingRobotWidget();
  }
});

window.openApiKeyModal = function() {
  if (window.SmartAssistant) {
    window.SmartAssistant.openApiKeyModal();
  }
};
