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
    },
    agent_prompt: {
      id: "agent_prompt",
      title: "AI Coding Agent Master Prompt",
      icon: "🤖",
      category: "AI Coding",
      desc: "A comprehensive developer instruction prompt tailored for AI coding agents (Cursor, Claude Code, Antigravity, etc.) to implement the project.",
      targetSlug: "overview-website-pricing-module-overview"
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

    if (docType === 'agent_prompt') {
      return `You are a Senior CTO & Principal AI Integration Architect. Generate a Master System Implementation Prompt tailored for an AI Coding Agent (e.g. Cursor, Antigravity, Claude Code, GitHub Copilot) to build the ${projName} (${projType}) for ${clientName}.

### Instructions:
Generate a structured, extremely clear, and actionable markdown system prompt that a developer can copy-paste directly into an AI coding agent. The prompt must force the agent to follow a strict, professional engineering methodology:

1. **Pre-requisite / Phase 0 (Research & Repository Analysis)**:
   - Instruct the coding agent to thoroughly read and analyze the existing codebase first. Do not write code before analyzing the existing codebase structure.
   - It MUST read all generated project reference documents which are saved in the project repository:
     - Technical Architecture Specification
     - Tech Stack Decision Report
     - REST API Endpoint Contract
     - Deployment & Infrastructure Guide
     - Security & OWASP Compliance Checklist
     - Performance & Scalability Blueprint
     - Risk Assessment Matrix
   - It MUST not start coding until it understands the complete system design.

2. **Phase 1: Task Checklist Creation (\`todo.md\`)**:
   - Instruct the agent to create a \`todo.md\` file outlining all component tasks, database migrations, and integrations, split into progressive implementation phases (Phase 1, Phase 2, Phase 3).

3. **Phase 2: Progressive Implementation**:
   - Explicitly instruct the agent to work on only one task checklist item at a time.
   - It must mark items as in-progress [ / ] and completed [ x ] in \`todo.md\` as it works.

4. **Phase 3: Rigorous Testing & Security Verification**:
   - Instruct the agent that after implementing each component, it must run verification tests, security audits, and sanity checks to ensure no regression or breakages occur.

### Context Summary for the Coding Agent:
- Industry/Domain: ${context.answers?.industry || 'General'}
- Hosting Preference: ${context.answers?.hostingPreference || 'Cloud'}
- Traffic Scale: ${context.answers?.trafficScale || 'MVP'}
- Urgency: ${context.answers?.timeline || 'MVP'}

Output ONLY the raw coding agent markdown prompt. Do not add intro or outro notes.`;
    }

    return `You are a seasoned, visionary Senior Chief Technology Officer (CTO) and Principal Enterprise Software Architect. 
Your goal is to generate an exceptionally detailed, professional, production-ready enterprise technical document titled "${docDef.title}" for ${clientName}'s ${projName} (Target Platform: ${projType}).

### Role Directive:
- Write with the authority, clarity, and deep technical insight of a CTO advising a Fortune 500 engineering team.
- Provide concrete architectural patterns, deep technology trade-offs, structured database schema definitions, real-world deployment pipeline configs, and robust security risk mitigation matrices.
- Never use generic placeholders or high-level filler descriptions. Include exact folder structures, library names, class names, API paths, and configuration file snippets (YAML/JSON/Terraform/Docker) where relevant.

### Project Intake Context & Clarifying Requirements:
${answers}

### Client Requirement Document Excerpt:
"""
${docText}
"""

### Document Specific Instructions:
Produce a comprehensive, publication-quality document in valid Github Markdown. Ensure it is structurally sound, using clear headers, comparative tables, database models, API endpoint structures, and code blocks with syntax highlighting. Focus on scalability, security, load handling, and clean-code practices.

Output ONLY the final markdown content. Do not include introductory notes or chat commentary.`;
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
    } else if (docType === 'agent_prompt') {
      content += `## 2. AI Coding Agent Master System Prompt\n\n`;
      content += `Copy the prompt below to paste into your AI coding agent/IDE (e.g. Cursor, Antigravity, Claude Code, GitHub Copilot):\n\n`;
      content += `\`\`\`markdown\n`;
      content += `You are an AI Software Engineer coding agent. Your goal is to build the ${project} (${platform}) for ${client}.\n\n`;
      content += `### Phase 0: Research existing code and generated documentation (Technical Architecture, API Contracts, Security Compliance Checklist).\n`;
      content += `### Phase 1: Create a todo.md file outlining all component tasks split into Phase 1, Phase 2, and Phase 3.\n`;
      content += `### Phase 2: Execute tasks in todo.md one-by-one, marking progress.\n`;
      content += `### Phase 3: Verify and run security checks on each component built before proceeding.\n`;
      content += `\`\`\`\n\n`;
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
  },

  /**
   * Refine prompt using workspace memory history context
   */
  async generateRefinedPrompt(newRefinementText, apiKey) {
    if (!window.ProjectStorage) return null;
    const project = window.ProjectStorage.getProject();
    if (!project.aiPromptRefinements) project.aiPromptRefinements = [];
    
    // Add new refinement to history
    project.aiPromptRefinements.push({
      timestamp: new Date().toISOString(),
      text: newRefinementText
    });
    window.ProjectStorage.saveProject(project);

    const previousPrompt = project.aiGeneratedDocs?.['agent_prompt']?.markdown || '';
    const clientName = project.clientName || "Client";
    const projName = project.projectName || "Project";
    const platform = project.platform || "Website";

    const prompt = `You are a Senior CTO & Principal AI Integration Architect.
We have an existing AI Coding Agent Master Prompt for the project "${projName}" (${platform}) of ${clientName}.
The user wants to refine this prompt by adding new features, requirements, or fixing existing bugs.

### Existing Master Prompt:
\`\`\`markdown
${previousPrompt}
\`\`\`

### History of Refinement Requests:
${project.aiPromptRefinements.map((r, i) => `${i + 1}. [${r.timestamp}] ${r.text}`).join('\n')}

### Latest New Refinement Request:
"""
${newRefinementText}
"""

### Instructions:
Update the Master Coding Agent Prompt to cleanly incorporate these new features, requirement constraints, and bug-fix directives. Ensure that the strict Phase-based methodology, todo.md checklist creation, progressive coding, and component-by-component testing rules are still maintained. Output the updated Master Prompt.

Output ONLY the new raw markdown prompt. No chat commentary.`;

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
      const updatedMarkdown = data.choices[0].message.content;

      // Save back to project state
      if (!project.aiGeneratedDocs) project.aiGeneratedDocs = {};
      project.aiGeneratedDocs['agent_prompt'] = {
        id: 'agent_prompt',
        title: 'AI Coding Agent Master Prompt',
        icon: '🤖',
        targetSlug: 'overview-website-pricing-module-overview',
        markdown: updatedMarkdown,
        generatedAt: new Date().toISOString()
      };
      window.ProjectStorage.saveProject(project);
      return updatedMarkdown;
    } catch (err) {
      console.error("Refined prompt generation failed:", err);
      throw err;
    }
  }
};
