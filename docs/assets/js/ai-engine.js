/**
 * AI-Powered Requirement Intelligence Engine
 * Advanced DeepSeek AI Document Generation, Intake Wizard, Multi-Doc Generation Pipeline,
 * Auto-Fill Workspace Integration, Diff Engine, and PDF Text Extractor.
 */

window.AIEngine = {
  /**
   * Available Document Deliverables Definitions
   */
  docTypes: {
    arch: {
      id: "arch",
      title: "Technical Architecture Specification",
      icon: "🏗️",
      category: "Architecture",
      desc: "Complete system architecture design, database schema, API layer structure, caching, and component interaction models.",
      targetSlug: "docs-website-website-requirements-complete-guide"
    },
    deploy: {
      id: "deploy",
      title: "Deployment & Infrastructure Guide",
      icon: "🚀",
      category: "DevOps",
      desc: "Cloud provider recommendations, server provisioning, CI/CD pipeline YAML, Docker configs, and environment variable lists.",
      targetSlug: "checklists-website-project-checklist"
    },
    seo: {
      id: "seo",
      title: "SEO & Growth Strategy Report",
      icon: "📈",
      category: "Marketing & SEO",
      desc: "Target keyword matrix, page-by-page meta tags, schema.org JSON-LD structured data, sitemap architecture, and Web Vitals.",
      targetSlug: "docs-website-website-requirements-complete-guide"
    },
    stack: {
      id: "stack",
      title: "Technology Stack Decision Report",
      icon: "💻",
      category: "Engineering",
      desc: "Framework comparisons, recommended stack with technical trade-off reasoning, library selections per subsystem.",
      targetSlug: "overview-website-pricing-module-overview"
    },
    timeline: {
      id: "timeline",
      title: "Project Timeline & Sprint Plan",
      icon: "📅",
      category: "Management",
      desc: "Sprint-by-sprint breakdown, key milestones, team role allocations, dependency graph, and critical path delivery dates.",
      targetSlug: "checklists-application-project-checklist"
    },
    risk: {
      id: "risk",
      title: "Risk Assessment & Mitigation Matrix",
      icon: "🛡️",
      category: "Governance",
      desc: "Technical risk rating (probability x impact), 3rd party dependency risks, performance bottlenecks, and contingency plans.",
      targetSlug: "overview-application-pricing-quick-guide"
    },
    api: {
      id: "api",
      title: "REST API Endpoint Contract",
      icon: "🔌",
      category: "Backend",
      desc: "Full RESTful API specification with HTTP methods, paths, request payloads, response schemas, and authentication headers.",
      targetSlug: "docs-application-application-requirements-complete-guide"
    },
    security: {
      id: "security",
      title: "Security & OWASP Compliance Checklist",
      icon: "🔒",
      category: "Security",
      desc: "OWASP Top 10 mitigation checklist, data encryption standard, auth flows, CORS policies, and GDPR data handling audit.",
      targetSlug: "checklists-application-project-checklist"
    },
    perf: {
      id: "perf",
      title: "Performance & Scalability Blueprint",
      icon: "⚡",
      category: "Performance",
      desc: "Target benchmarks, load testing scenarios, CDN topology, database indexing strategy, and memory caching setup.",
      targetSlug: "docs-application-application-requirements-complete-guide"
    },
    exec: {
      id: "exec",
      title: "Client Executive Summary",
      icon: "📄",
      category: "Executive",
      desc: "Non-technical 1-page executive summary tailored for client presentations, budget justifications, and project scope sign-off.",
      targetSlug: "template-word-template-website-client-proposal"
    }
  },

  /**
   * PDF Text Extraction via PDF.js or raw reader
   */
  async extractTextFromPDF(file) {
    if (file.type === "application/pdf") {
      try {
        if (window.pdfjsLib) {
          const arrayBuffer = await file.arrayBuffer();
          const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
          let fullText = "";
          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(" ");
            fullText += `\n--- Page ${i} ---\n` + pageText;
          }
          return fullText.trim();
        }
      } catch (err) {
        console.warn("PDF.js extraction failed, falling back to FileReader text extraction:", err);
      }
    }
    // Fallback text extraction
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result || "");
      reader.readAsText(file);
    });
  },

  /**
   * Build DeepSeek Prompt per Document Type
   */
  buildPromptForDocType(docType, context) {
    const docDef = this.docTypes[docType];
    const clientName = context.clientName || "Client";
    const projName = context.projectName || "Project";
    const projType = context.projectType || "Website";
    const answers = JSON.stringify(context.answers || {}, null, 2);
    const docText = (context.docText || "").slice(0, 5000);

    return `You are a Principal Solutions Architect & Senior Technical Lead. Generate a comprehensive, professional, production-grade technical document titled "${docDef.title}" for ${clientName}'s ${projName} (${projType}).

### Project Intake Context & Clarifying Requirements:
${answers}

### Client Requirement Document Excerpt:
"""
${docText}
"""

### Document Instructions:
Produce a complete markdown-formatted document. Include detailed sections, tables, code snippets, config blocks, and actionable architectural guidance. Do not use generic filler text; tailor every detail specifically to the provided client requirement and intake context.

Output ONLY valid markdown content.`;
  },

  /**
   * Call DeepSeek API for a specific document
   */
  async generateSingleDocument(docType, context, apiKey) {
    const docDef = this.docTypes[docType];
    if (!apiKey) {
      return this.buildFallbackDocument(docType, context);
    }

    const prompt = this.buildPromptForDocType(docType, context);

    try {
      const res = await fetch("https://api.deepseek.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: "deepseek-chat",
          messages: [{ role: "user", content: prompt }]
        })
      });

      if (!res.ok) throw new Error(`DeepSeek API error HTTP ${res.status}`);
      const data = await res.json();
      const markdown = data.choices[0].message.content;
      return {
        id: docType,
        title: docDef.title,
        icon: docDef.icon,
        targetSlug: docDef.targetSlug,
        markdown: markdown,
        generatedAt: new Date().toISOString()
      };
    } catch (err) {
      console.warn(`DeepSeek generation failed for ${docType}, using intelligent fallback:`, err);
      return this.buildFallbackDocument(docType, context);
    }
  },

  /**
   * Run Parallel Batch Generation Pipeline
   */
  async generateAllSelected(selectedDocTypes, context, progressCallback) {
    const apiKey = window.SmartAssistant ? window.SmartAssistant.getApiKey() : '';
    const results = [];
    const total = selectedDocTypes.length;

    for (let i = 0; i < total; i++) {
      const docType = selectedDocTypes[i];
      const docDef = this.docTypes[docType];
      if (progressCallback) progressCallback(i, total, docDef.title);

      const docResult = await this.generateSingleDocument(docType, context, apiKey);
      results.push(docResult);

      if (progressCallback) progressCallback(i + 1, total, docDef.title);
    }

    // Auto-fill into project storage
    this.autoFillWorkspace(results);

    return results;
  },

  /**
   * Auto-fill generated documents into ProjectStorage & page mapping
   */
  autoFillWorkspace(generatedDocs) {
    if (!window.ProjectStorage) return;
    const project = window.ProjectStorage.getProject();
    if (!project.aiGeneratedDocs) project.aiGeneratedDocs = {};

    generatedDocs.forEach(doc => {
      project.aiGeneratedDocs[doc.id] = doc;

      // Auto-fill into specific page storage key if requested
      if (doc.targetSlug) {
        const storageKey = `edited_doc_${project.id}_${doc.targetSlug}`;
        // Store as AI draft
        const draftKey = `ai_draft_${project.id}_${doc.targetSlug}`;
        localStorage.setItem(draftKey, doc.markdown);
      }
    });

    window.ProjectStorage.saveProject(project);
  },

  /**
   * Intelligent Fallback Engine per Document Type
   */
  buildFallbackDocument(docType, context) {
    const docDef = this.docTypes[docType];
    const client = context.clientName || "Acme Client";
    const project = context.projectName || "Enterprise Solution";
    const platform = context.projectType || "Web & Mobile";
    const answers = context.answers || {};

    let content = `# ${docDef.icon} ${docDef.title}\n\n`;
    content += `**Client:** ${client}  \n`;
    content += `**Project Title:** ${project}  \n`;
    content += `**Target Platform:** ${platform}  \n`;
    content += `**Generated Date:** ${new Date().toLocaleDateString()}  \n\n`;

    content += `---\n\n## 1. Executive Context & Objectives\n\n`;
    content += `This ${docDef.title} has been compiled based on requirement analysis for **${client}**. Key project attributes:\n\n`;
    content += `- **Primary Objective:** Deliver a high-performance ${platform} tailored to client requirements.\n`;
    content += `- **SEO & Marketing Strategy:** ${answers.seoPriority || 'Standard SEO & Google Analytics Integration'}\n`;
    content += `- **Hosting & Infrastructure:** ${answers.hostingPreference || 'AWS Cloud Container Infrastructure'}\n`;
    content += `- **Estimated Target Scale:** ${answers.trafficScale || '10,000+ monthly active users'}\n\n`;

    if (docType === 'arch') {
      content += `## 2. System Architecture Blueprint\n\n`;
      content += `\`\`\`
+-------------------------------------------------------+
|                 Client Presentation Layer              |
|        (React / Next.js / Flutter Mobile Client)       |
+--------------------------+----------------------------+
                           | REST API / HTTPS
+--------------------------v----------------------------+
|                   API Gateway & Auth                  |
|                 (JWT Bearer / Node.js)                |
+--------------------------+----------------------------+
                           |
            +--------------+--------------+
            |                             |
+-----------v-----------+     +-----------v-----------+
|   Core Business Logic |     |  Database & Cache     |
|   (Express / Python)  |     | (PostgreSQL / Redis)  |
+-----------------------+     +-----------------------+
\`\`\`\n\n`;
      content += `### Data Layer & Schema Overview\n\n| Entity | Table Name | Key Attributes |\n| :--- | :--- | :--- |\n| Users | \`users\` | \`id, email, password_hash, role, created_at\` |\n| Projects | \`projects\` | \`id, client_id, title, status, budget\` |\n| Audit Logs | \`audit_logs\` | \`id, user_id, action, timestamp\` |\n\n`;
    } else if (docType === 'deploy') {
      content += `## 2. CI/CD & Deployment Pipeline\n\n`;
      content += `### Recommended Technology Stack\n- **Cloud Infrastructure:** Docker Containers on AWS ECS / DigitalOcean App Platform\n- **CI/CD Automation:** GitHub Actions Pipeline\n- **Database Service:** Managed PostgreSQL RDS with SSL\n\n`;
      content += `### GitHub Actions Deployment Workflow (\`.github/workflows/deploy.yml\`)\n\n\`\`\`yaml
name: Production Deployment Pipeline
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js Environment
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install Dependencies & Run Automated Tests
        run: |
          npm ci
          npm run test
      - name: Build & Deploy Container
        run: |
          echo "Building production release bundle..."
\`\`\`\n\n`;
    } else if (docType === 'seo') {
      content += `## 2. SEO & Growth Architecture\n\n`;
      content += `### Target Keyword Strategy Matrix\n\n| Keyword Category | Target Search Term | Intent | Page Mapping |\n| :--- | :--- | :--- | :--- |\n| Core Brand | ${client} ${project} | Navigational | Homepage (\`/\`) |\n| Service Category | Custom ${platform} Development | Commercial | Services (\`/services\`) |\n| Location / Niche | ${platform} Agency Solutions | Transactional | Contact (\`/contact\`) |\n\n`;
      content += `### Schema.org JSON-LD Structured Data Template\n\n\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "${client}",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "${project} Solution Platform"
}
\`\`\`\n\n`;
    } else {
      content += `## 2. Standard Technical Specifications & Execution Guidelines\n\n`;
      content += `1. **Scalability Standards:** Microservice ready module structures.\n`;
      content += `2. **Security Compliance:** AES-256 bit encryption at rest, TLS 1.3 in transit.\n`;
      content += `3. **Quality Assurance:** Unit test coverage minimum 80%, end-to-end integration tests.\n\n`;
    }

    content += `## 3. Developer & Delivery Action Items\n\n`;
    content += `- [x] Review requirement specification with engineering lead.\n`;
    content += `- [ ] Configure environment secret credentials.\n`;
    content += `- [ ] Setup CI/CD build pipelines and staging server.\n`;
    content += `- [ ] Perform pre-launch security & performance audits.\n`;

    return {
      id: docType,
      title: docDef.title,
      icon: docDef.icon,
      targetSlug: docDef.targetSlug,
      markdown: content,
      generatedAt: new Date().toISOString()
    };
  }
};
