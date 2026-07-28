# 💼 Price Module — Client Project Pricing & Requirements Toolkit

> A comprehensive toolkit for freelance developers and agencies to gather client requirements, estimate pricing, and deliver professional proposals for **Website** and **Mobile Application** projects — with an integrated **Interactive Web Document Hub** and **Static Site Generator** for GitHub Pages.

---

## 🌐 Interactive Web Hub & Documentation Site

This repository features a static site generator in Python that compiles all Markdown (`.md`), Word (`.docx`), and Excel (`.xlsx`) documents into an interactive, glassy web interface with **Cabinet Grotesk** typography and multi-format exports.

### 🌟 Key Web Features
- **All-in-One Dashboard (`docs/index.html`)**: Clickable document cards with real-time live search and file-type badges (`MD`, `DOCX`, `XLSX`).
- **Interactive Document Views**: Rendered Markdown text, formatted Word documents, and multi-sheet tabbed Excel spreadsheets.
- **Cabinet Grotesk Typography**: Premium headline & brand font loaded via Fontshare.
- **Browser LocalStorage Auto-Save**: Save client details, checked features, custom unit rates, and checklist states directly in the browser.
- **Custom Proposal Builder**: Create client proposals with automatic tax (GST 18%), discount, platform multiplier, and milestone payment schedules.
- **Multi-Format Content Exports**: One-click extraction as PDF, Word (.docx), Excel (.xlsx), or JSON Project File.
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
