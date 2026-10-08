Here is the complete document inventory for building a software product from scratch to end-of-life — **80+ documents organized into 9 phases of the SDLC**, from the smallest decision record to the biggest architecture blueprint. This is the full stack that any developer, team, or agent-based workflow needs.【turn0search5】【turn1fetch1】

## Master Document Map (Phase → Documents)

| Phase | Documents | Purpose | Primary Owner |
|-------|-----------|---------|---------------|
| **0. Discovery** | Vision statement, Business Case, Market Research, Competitor Analysis, Feasibility Study, Financial Model, Pitch Deck | Prove the idea is worth building | Founder / PM |
| **1. Requirements** | BRD, PRD, User Personas, User Journeys, User Stories, Use Cases, Roadmap, KPIs/OKRs | Define *what* to build and *why* | PM |
| **2. UX/UI Design** | IA, Sitemap, User Flows, Wireframes, Mockups, Prototype, Design System, Design Tokens, Copy Deck | Define *what it looks like* | Designer |
| **3. Architecture** | HLD, LLD, TSD, ADRs, Data Model/ERD, DB Schema, API Spec, Threat Model, Dependency Graph | Define *how it's built* | Architect / Tech Lead |
| **4. Development** | Coding Standards, Task Breakdown, Sprint Backlog, DoR/DoD, README, CONTRIBUTING, Git conventions | Execute the build | Developers |
| **5. Testing** | Test Strategy, Test Plan, Test Cases, Test Data, RTM, Bug Reports, UAT Plan, Perf/Security Test Plans | Verify it works | QA |
| **6. Deployment** | Deployment Plan, Release Notes, Rollback Plan, Runbooks, Config Docs, Go-Live Checklist | Ship it safely | DevOps / Release Mgr |
| **7. Operations** | Incident Playbook, Escalation Matrix, SLO/SLA, DR Plan, BCP, Backup Procedures, On-call Docs | Keep it running | SRE / Ops |
| **8. Legal & Compliance** | Privacy Policy, ToS, DPA, Data Map, DPIA, Security Policies, Audit Reports, SBOM | Stay legal & secure | Legal / Security |
| **9. Post-Launch** | GTM Strategy, Launch Checklist, User Manual, FAQ, Support SOPs, Retrospectives, Post-mortems, Deprecation Plan | Improve & eventually retire | PM / Support |

---

## Phase 0 — Discovery & Strategy Documents

| Document | What it contains |
|----------|-----------------|
| **Vision & Mission Statement** | The one-sentence future the product creates |
| **Business Case** | Problem, opportunity, cost/benefit, why now, alternatives considered |
| **Market Research Report** | TAM/SAM/SOM, target segments, primary + secondary research findings【turn2search18】 |
| **Competitor Analysis** | Feature matrix, positioning map, differentiation gaps, threats【turn2search17】 |
| **Feasibility Study** | Technical, operational, financial, legal feasibility |
| **Financial Model** | Revenue projections, cost structure, break-even, unit economics【turn2search16】 |
| **Business Model Canvas** | Value props, channels, revenue streams, key partners |
| **Pitch Deck** | Investor/stakeholder narrative |
| **Stakeholder Register** | Who's affected, their influence, communication needs |
| **Initial Risk Register** | Top risks with probability × impact |

---

## Phase 1 — Product Requirements Documents

| Document | What it contains |
|----------|-----------------|
| **BRD** (Business Requirements Doc) | Business objectives, stakeholder needs, high-level capabilities — the *why* at business level【turn0search7】 |
| **PRD** (Product Requirements Doc) | Features, scope, non-goals, acceptance criteria, decisions made — the single source of truth for *what* gets built【turn4fetch1】 |
| **User Personas** | Target users: goals, pains, behaviors, contexts【turn2search1】 |
| **User Journey Maps** | End-to-end experience across touchpoints, emotions, pain points |
| **User Stories** | "As a X, I want Y, so that Z" + acceptance criteria per story【turn1fetch0】 |
| **Use Cases** | Actor → system interactions with preconditions, main flow, alternate flows |
| **Product Roadmap** | Timeline of epics/releases/milestones — now, next, later |
| **Feature Prioritization** | MoSCoW / RICE / Kano scores justifying order |
| **Success Metrics (KPIs/OKRs)** | Measurable definitions of success per feature and overall |
| **Scope Statement + Non-Goals** | Explicit boundaries — critical because agents and devs expand scope when boundaries aren't written【turn4fetch1】 |

---

## Phase 2 — UX/UI Design Documents

| Document | What it contains |
|----------|-----------------|
| **Information Architecture (IA)** | Content structure, hierarchy, taxonomy |
| **Sitemap** | All screens/pages and their relationships |
| **User Flows** | Step-by-step paths users take to complete tasks, including error/empty states |
| **Wireframes** | Low-fidelity grayscale layouts — structure without visuals【turn2search2】 |
| **Mockups** | High-fidelity visual designs with branding, color, typography |
| **Interactive Prototype** | Clickable simulation for usability testing |
| **Design System / Style Guide** | Colors, typography, spacing, iconography, voice & tone rules |
| **UI Component Library + Design Tokens** | Reusable components with machine-readable token values |
| **Accessibility Checklist** | WCAG 2.1/2.2 AA compliance per component |
| **Content / Copy Deck** | All microcopy: labels, errors, empty states, toasts |

---

## Phase 3 — Technical Architecture Documents

| Document | What it contains |
|----------|-----------------|
| **HLD** (High-Level Design) | System components, services, tech stack, how they talk — the bird's-eye view【turn0search15】 |
| **LLD** (Low-Level Design) | Module internals, class diagrams, function signatures, file structure |
| **TSD** (Technical Spec Doc) | Detailed implementation specs per feature【turn0search7】 |
| **ADR** (Architecture Decision Records) | One record per significant decision: context → options → choice → consequences【turn3search18】 |
| **RFCs** | Proposals circulated for review before major/controversial changes【turn3search15】 |
| **Data Model / ERD** | Entities, relationships, cardinality |
| **Database Schema + Migrations** | Tables, indexes, constraints, versioned migration scripts |
| **API Specification** | OpenAPI/Swagger: endpoints, methods, request/response schemas, error codes, auth |
| **Data Flow Diagrams (DFD)** | How data moves through the system |
| **Sequence Diagrams** | Time-ordered interactions between components for key flows |
| **Threat Model** | Attack surfaces, trust boundaries, STRIDE analysis, mitigations【turn3search3】 |
| **Infrastructure Architecture** | Cloud topology, networking, regions, environments |
| **Dependency Graph** | Which components/services depend on which — critical for build order and blast-radius analysis |
| **Integration Contracts** | Third-party APIs, webhooks, event schemas |
| **NFRs** (Non-Functional Requirements) | Performance budgets, uptime targets, scalability limits, security rules |

---

## Phase 4 — Development Process Documents

| Document | What it contains |
|----------|-----------------|
| **Coding Standards / Style Guide** | Naming, formatting, patterns, anti-patterns, linting rules |
| **CLAUDE.md / AGENTS.md** | Rules loaded into every AI agent session — conventions, what never to touch【turn0search7】 |
| **Task Breakdown (WBS)** | Atomic, file-scoped tasks with acceptance criteria and dependency order |
| **Product Backlog** | Ordered list of all user stories/epics not yet started【turn3search6】 |
| **Sprint Backlog + Sprint Goal** | Committed work for the current sprint |
| **Definition of Ready** | Checklist a task must meet before development starts |
| **Definition of Done** | Checklist a task must meet to be "complete" — code, tests, docs, review |
| **Branching & Commit Conventions** | Git flow / trunk-based, commit message format, PR template |
| **README** | Project overview, setup instructions, how to run/test【turn1fetch0】 |
| **CONTRIBUTING.md** | How to propose changes, PR process, review expectations |
| **CODEOWNERS** | Who must review which paths |
| **Environment Setup Guide** | Local dev, staging, prod — dependencies, env vars, secrets handling |
| **Changelog** | Versioned log of every notable change (Keep a Changelog format) |
| **Burndown/Burnup Charts** | Sprint progress tracking |

---

## Phase 5 — QA / Testing Documents

| Document | What it contains |
|----------|-----------------|
| **Test Strategy** | Organization-wide approach: testing levels, types, tools, environments, entry/exit criteria |
| **Test Plan** | Per-release scope, schedule, resources, risks, deliverables【turn2search8】 |
| **Test Cases** | Input → action → expected result, step by step, per requirement |
| **Test Scenarios** | High-level user-path test conditions |
| **Test Data Specification** | What data to seed, anonymization rules |
| **RTM** (Requirements Traceability Matrix) | Maps every requirement → test case → result, proving full coverage【turn2search6】 |
| **Test Checklists** | Quick verification lists per feature |
| **Exploratory Test Charters** | Timeboxed missions for unscripted testing |
| **Bug/Defect Reports** | Repro steps, environment, severity, priority, evidence【turn2search9】 |
| **Test Execution Reports** | Pass/fail runs per cycle, coverage stats |
| **Performance/Load Test Plan + Results** | Benchmarks, thresholds, k6/JMeter scenarios |
| **Security Test Plan** | Pen-test scope, SAST/DAST config, results |
| **UAT Plan + Sign-off** | Business users' acceptance script and formal approval record |

---

## Phase 6 — Deployment & Release Documents

| Document | What it contains |
|----------|-----------------|
| **Deployment Plan** | Step-by-step release procedure, timing, owners, comms plan |
| **Go-Live Checklist** | Final gate: all sign-offs, monitoring armed, support briefed |
| **Rollback Plan** | Exact steps to revert to last stable version, decision triggers【turn1fetch1】 |
| **Runbooks** | Ordered procedures per known operation: prechecks → rollout → smoke tests → verification → ownership【turn2search10】 |
| **Release Notes** | What changed and why it matters, per version【turn3search13】 |
| **Config Reference** | Environment variables, feature flags, secrets inventory per environment |
| **IaC Documentation** | Terraform/CloudFormation module docs, state management |
| **CI/CD Pipeline Docs** | Pipeline stages as code + explanation of gates |
| **Data Migration Plan** | Schema/data conversion steps, validation queries, dry-run results |
| **Smoke Test Checklist** | 10–15 critical-path checks immediately post-deploy |
| **Cutover Plan** | For big-bang migrations: sequence, freeze windows, comms |

---

## Phase 7 — Operations & SRE Documents

| Document | What it contains |
|----------|-----------------|
| **Incident Response Playbook** | Severity classification → diagnosis → mitigation → comms → recovery → review【turn2search14】 |
| **Escalation Matrix** | Who to page at what severity, at what time |
| **On-call Documentation** | Rotation, handoff procedure, tooling access |
| **SLO/SLI/SLA Definitions** | Uptime targets, latency budgets, error budgets, customer-facing SLAs |
| **Monitoring & Alerting Guide** | What's monitored, alert thresholds, dashboard links |
| **Disaster Recovery Plan (DRP)** | RTO/RPO targets, failover procedure, recovery site strategy【turn2search11】 |
| **Business Continuity Plan (BCP)** | How the *business* operates during extended outage |
| **Backup & Restore Procedures** | Schedule, retention, tested-restore verification |
| **Capacity Planning Docs** | Load forecasts, scaling thresholds, cost projections |
| **Cost/FinOps Runbook** | Resource tagging, budget alerts, optimization cadence |
| **Internal Knowledge Base / Wiki** | Institutional memory: how-tos, tribal knowledge, FAQs |
| **Maintenance Schedule** | Patching windows, dependency update cadence, cert renewals |

---

## Phase 8 — Security, Legal & Compliance Documents

| Document | What it contains |
|----------|-----------------|
| **Privacy Policy + Terms of Service** | Public-facing legal agreements |
| **DPA** (Data Processing Agreement) | Required when handling EU customer data |
| **Data Map / Records of Processing** | What personal data exists, where, why, retention (GDPR Art. 30) |
| **DPIA** (Data Protection Impact Assessment) | Required for high-risk processing |
| **Security Policies** | Access control, encryption, password, remote work, incident disclosure |
| **Compliance Evidence Packs** | SOC 2 / ISO 27001 / HIPAA / PCI-DSS control evidence【turn3search3】 |
| **Penetration Test Reports** | Findings, severity, remediation status |
| **Vulnerability Management Process** | Scan cadence, SLA per severity, patch workflow |
| **SBOM** (Software Bill of Materials) | Every dependency and its license — supply-chain security |
| **License Compliance Register** | OSS licenses used, copyleft risk analysis |
| **Audit Log & Access Review Records** | Who accessed what, periodic access recertification |

---

## Phase 9 — Go-to-Market & Post-Launch Documents

| Document | What it contains |
|----------|-----------------|
| **GTM Strategy** | Positioning, pricing, channels, launch tiers |
| **Launch Checklist** | Cross-team tasks: eng, marketing, support, sales readiness【turn3search11】 |
| **User Manual / Help Center** | End-user documentation: tutorials, guides, troubleshooting【turn0search15】 |
| **Onboarding Flows** | First-run experience docs |
| **FAQ** | Deflected support questions |
| **Support SOPs** | How support handles common issues, refund policy, bug triage to eng |
| **Customer Feedback Log** | Structured capture of requests/complaints feeding the backlog |
| **Analytics & Telemetry Plan** | Event taxonomy, funnel definitions, dashboards |
| **Sprint Retrospective Notes** | What worked / didn't / actions per sprint |
| **Incident Post-mortems** | Blameless root-cause analyses with action items |
| **Quarterly Business Reviews** | Metrics vs. OKRs, strategy adjustments |
| **Deprecation / EOL Plan** | Sunset timeline, migration path, customer comms |

---

## Priority Tiers — What You Actually Need

The full list above is the enterprise/regulated-product ceiling. For practical purposes, documents fall into three tiers:

**🔴 Tier 1 — Non-negotiable (every product, even a weekend MVP):**
PRD → Architecture (HLD + ADRs) → Data Model + API Spec → Task Breakdown → README → Test Cases → Deployment Plan + Rollback → Release Notes → Changelog

**🟡 Tier 2 — Needed once real users arrive:**
Design System, User Journeys, Test Plan + RTM, Runbooks, Incident Playbook, Monitoring/SLOs, Privacy Policy + ToS, User Manual, Support SOPs, Retrospectives

**🟢 Tier 3 — Enterprise / regulated / scale stage:**
DPIA, SOC 2 evidence, SBOM, DRP + BCP, Pen-test reports, Formal UAT, Capacity planning, FinOps, Quarterly business reviews

## How This Maps to Your Fable Workflow

Tying this back to your orchestrator pattern: **Fable generates Tiers 1 (and later Tier 2) docs in Phases 0–3**, then converts Phase 3 output into the atomic task breakdown; **small models consume Phases 4–5 docs one task at a time**; and **Fable reviews against the Phase 5 acceptance criteria and RTM** before anything merges. Phases 6–9 are where you add human-owned process docs as the product matures — no need to generate them upfront.
