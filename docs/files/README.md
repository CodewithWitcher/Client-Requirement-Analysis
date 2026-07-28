# 💼 Price Module — Client Project Pricing & Requirements Toolkit

> A comprehensive toolkit for freelance developers and agencies to gather client requirements, estimate pricing, and deliver professional proposals for **Website** and **Mobile Application** projects — with an integrated **Web Document Hub** and **Static Site Generator** for GitHub Pages.

---

## 🌐 Static Web Hub & Documentation Site

This repository features a static site generator in Python that compiles all Markdown (`.md`), Word (`.docx`), and Excel (`.xlsx`) documents into an interactive, glassy web interface with Boska typography and multi-format exports.

### 🌟 Key Web Features
- **All-in-One Dashboard (`docs/index.html`)**: Clickable document cards with real-time live search and file-type badges (`MD`, `DOCX`, `XLSX`).
- **Interactive Document Views**: Rendered Markdown text, formatted Word documents, and multi-sheet tabbed Excel spreadsheets.
- **Multi-Format Content Exports**: One-click extraction as PDF, Word (.docx), Excel (.xlsx), or Original file downloads.
- **Modern Light Glassmorphism UI**: High accessibility contrast, Boska font typography, backdrop blur cards, and responsive mobile layout.
- **GitHub Pages Ready**: 100% static output stored in `/docs` — zero backend runtime needed.

---

## 💻 Quick Start & Build Guide

### 1. Installation
Install the python document parsing dependencies:

```bash
pip install -r requirements.txt
```

### 2. Build the Static Web Site
Run the single build command to scan all documents, generate web pages, and update the static site in `docs/`:

```bash
python scripts/build_site.py
```
*(On Windows with Python Launcher, you can also run `py scripts/build_site.py`)*

### 3. Preview Locally
Open `docs/index.html` directly in any web browser, or launch a quick local preview server:

```bash
python -m http.server 8000 --directory docs
```
Then navigate to `http://localhost:8000`.

---

## 🚀 GitHub Pages Deployment Steps

To host the interactive web interface for free on GitHub Pages:

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Build static document site for GitHub Pages"
   git push origin main
   ```
2. In your GitHub Repository, navigate to **Settings** &rarr; **Pages**.
3. Under **Build and deployment**:
   - **Source**: Select `Deploy from a branch`.
   - **Branch**: Select `main` and set the folder to `/docs`.
4. Click **Save**.
5. Within 1–2 minutes, your website will be live at `https://<username>.github.io/<repository-name>/`.

---

## 📁 Repository Structure

```
Client-Requirement-Analysis/
│
├── README.md                          ← You are here
├── requirements.txt                   ← Python dependencies
│
├── scripts/                           ← Python generators & build scripts
│   ├── build_site.py                  ← Main static site generator command
│   ├── generate_excel.py              ← Excel spreadsheet generator
│   └── generate_word.py               ← Word proposal generator
│
├── docs/                              ← Generated static website (GitHub Pages publish folder)
│   ├── index.html                     ← Main Hub index page with search & filter
│   ├── pages/                         ← Converted document preview pages (.html)
│   ├── assets/                        ← Shared CSS (Boska fonts, glassmorphism) & JS
│   └── files/                         ← Preserved original & export download files
│
├── Questionnaire/                     ← Client-facing questionnaires
│   ├── website/
│   └── application/
│
├── checklists/                        ← Pre-project & post-project checklists
│
├── Template/                          ← Excel calculators & Word proposal templates
│   ├── excel template/
│   └── word template/
│
└── overview/                          ← Module overview guides
```

---

## 📋 What's Covered

### For Websites
| Category | Parameters |
|----------|-----------|
| Domain & Hosting | Domain registration, SSL, hosting type, CDN, server location |
| Database | Type, size, backups, migrations, scaling |
| Tech Stack | Frontend, backend, CMS, frameworks, languages |
| Design & UX | Custom vs template, responsive, wireframes, revisions |
| Pages & Features | Static/dynamic pages, forms, search, auth, dashboards |
| E-Commerce | Product catalog, cart, checkout, inventory, shipping |
| Payment Integration | Gateways, multi-currency, subscriptions, invoicing |
| SEO & Analytics | On-page SEO, tracking, sitemap, schema markup |
| Security | SSL, firewalls, DDoS, GDPR, data protection |

### For Mobile Applications
| Category | Parameters |
|----------|-----------|
| Platform | iOS, Android, cross-platform, PWA |
| App Store & Deployment | Play Store, App Store, ASO, developer accounts |
| Design & UX | Platform guidelines, animations, dark mode, theming |
| Features | Auth, notifications, chat, geolocation, camera, offline |
| Backend & API | Custom backend, BaaS, real-time, file storage |

---

## 📄 Export Formats Supported

Each document page includes top action buttons allowing users to export or download content:
- 📄 **Export as PDF**: Triggers clean printable document layout optimized for PDF saving.
- 📝 **Export as Word (.docx)**: Pre-formatted downloadable Word document.
- 📊 **Export as Excel (.xlsx)**: Pre-formatted downloadable Excel spreadsheet.
- 💾 **Download Original**: Downloads the source Markdown, Word, or Excel file preserved in the repo.
