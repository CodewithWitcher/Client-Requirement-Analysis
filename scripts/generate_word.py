#!/usr/bin/env python3
"""
Generate Word (.docx) Client Proposal templates for Website and Application projects.
Run: python3 scripts/generate_word.py
"""

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml


# ─── Style Constants ───────────────────────────────────────────────

DARK_BLUE = RGBColor(0x1B, 0x2A, 0x4A)
MED_BLUE = RGBColor(0x2E, 0x75, 0xB6)
ACCENT_GREEN = RGBColor(0x54, 0x82, 0x35)
ACCENT_ORANGE = RGBColor(0xED, 0x7D, 0x31)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
BLACK = RGBColor(0x00, 0x00, 0x00)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)


def set_cell_shading(cell, color_hex):
    """Set background color of a table cell."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_border(cell, **kwargs):
    """Set cell border. Usage: set_cell_border(cell, top={"sz": 6, "color": "1B2A4A"})"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}></w:tcBorders>')
        tcPr.append(tcBorders)

    for edge, attrs in kwargs.items():
        element = tcBorders.find(qn(f'w:{edge}'))
        if element is None:
            element = parse_xml(
                f'<w:{edge} {nsdecls("w")} w:val="single" '
                f'w:sz="{attrs.get("sz", 4)}" w:space="0" '
                f'w:color="{attrs.get("color", "000000")}"/>'
            )
            tcBorders.append(element)


def add_styled_table(doc, headers, rows, col_widths=None):
    """Add a professionally styled table to the document."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    # Header row
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE
        set_cell_shading(cell, "1B2A4A")

    # Data rows
    for r, row_data in enumerate(rows):
        for c, value in enumerate(row_data):
            cell = table.rows[r + 1].cells[c]
            cell.text = str(value)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if p.runs:
                p.runs[0].font.size = Pt(9)
            if r % 2 == 0:
                set_cell_shading(cell, "F2F2F2")

    # Column widths
    if col_widths:
        for i, width in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(width)

    return table


def add_heading_styled(doc, text, level=1):
    """Add a heading with custom styling."""
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.color.rgb = DARK_BLUE
    return heading


def add_cover_page(doc, title, subtitle):
    """Add a professional cover page."""
    # Add spacing before title
    for _ in range(6):
        doc.add_paragraph("")

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.size = Pt(32)
    run.font.bold = True
    run.font.color.rgb = DARK_BLUE

    # Divider line
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("━" * 40)
    run.font.size = Pt(14)
    run.font.color.rgb = MED_BLUE

    # Subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle)
    run.font.size = Pt(16)
    run.font.color.rgb = DARK_GRAY

    # Spacer
    doc.add_paragraph("")
    doc.add_paragraph("")

    # Info fields
    info_items = [
        ("Prepared For:", "[Client Name]"),
        ("Prepared By:", "[Your Name / Company]"),
        ("Date:", "[DD/MM/YYYY]"),
        ("Version:", "1.0"),
        ("Confidential:", "Yes"),
    ]
    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"{label} ")
        run.font.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = DARK_BLUE
        run = p.add_run(value)
        run.font.size = Pt(11)
        run.font.color.rgb = DARK_GRAY

    doc.add_page_break()


def add_toc_placeholder(doc):
    """Add a Table of Contents placeholder."""
    add_heading_styled(doc, "Table of Contents", level=1)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run("[Table of Contents — auto-generated in Word: References > Table of Contents]")
    run.font.italic = True
    run.font.color.rgb = DARK_GRAY
    run.font.size = Pt(10)
    doc.add_page_break()


# ════════════════════════════════════════════════════════════════════
# WEBSITE CLIENT PROPOSAL
# ════════════════════════════════════════════════════════════════════

def create_website_proposal(path):
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Cover Page
    add_cover_page(
        doc,
        "Website Development\nProposal",
        "Professional Web Solutions"
    )

    # Table of Contents
    add_toc_placeholder(doc)

    # ── Section 1: Executive Summary ───────────────────────────────
    add_heading_styled(doc, "1. Executive Summary", level=1)
    doc.add_paragraph(
        "Thank you for considering us for your website development project. "
        "This proposal outlines our understanding of your requirements, the scope of work, "
        "technology stack, timeline, pricing, and terms of engagement.\n\n"
        "We are committed to delivering a high-quality, modern, and performant website "
        "that meets your business objectives and exceeds your expectations."
    )

    # Key highlights table
    add_styled_table(doc, ["Parameter", "Details"], [
        ("Project Name", "[Project Name]"),
        ("Client", "[Client Name / Company]"),
        ("Project Type", "[Business Website / E-Commerce / Web Application / Landing Page]"),
        ("Platform", "Web (Desktop + Mobile Responsive)"),
        ("Estimated Duration", "[X weeks/months]"),
        ("Estimated Budget", "[₹XX,XXX — ₹XX,XXX]"),
    ], col_widths=[2.5, 4.0])

    doc.add_page_break()

    # ── Section 2: Project Understanding ───────────────────────────
    add_heading_styled(doc, "2. Project Understanding", level=1)
    doc.add_paragraph(
        "[Describe your understanding of the client's business, their goals for the website, "
        "target audience, and key problems the website will solve. This section should show "
        "the client that you understand their needs.]"
    )

    doc.add_heading("2.1 Business Overview", level=2)
    doc.add_paragraph("[Client's business description, industry, and target market.]")

    doc.add_heading("2.2 Project Goals", level=2)
    doc.add_paragraph(
        "• [Goal 1 — e.g., Establish online presence]\n"
        "• [Goal 2 — e.g., Generate leads through the website]\n"
        "• [Goal 3 — e.g., Enable online sales]\n"
        "• [Goal 4 — e.g., Improve brand visibility]"
    )

    doc.add_heading("2.3 Target Audience", level=2)
    doc.add_paragraph("[Describe the target users — age, location, behavior, pain points.]")

    doc.add_page_break()

    # ── Section 3: Scope of Work ───────────────────────────────────
    add_heading_styled(doc, "3. Scope of Work", level=1)

    doc.add_heading("3.1 Domain & Hosting", level=2)
    add_styled_table(doc, ["Item", "Details", "Provided By"], [
        ("Domain Registration", "[.com / .in / .org / etc.]", "[Client / Developer]"),
        ("Domain Privacy Protection", "[Yes / No]", "—"),
        ("SSL Certificate", "[Free (Let's Encrypt) / Paid]", "[Developer]"),
        ("Hosting Type", "[Shared / VPS / Cloud / Managed]", "[Client / Developer]"),
        ("Hosting Provider", "[AWS / DigitalOcean / Hostinger / etc.]", "[Client / Developer]"),
        ("Server Location", "[India / US / Europe]", "—"),
        ("Email Hosting", "[Yes / No] — [Google Workspace / Zoho / cPanel]", "[Developer]"),
        ("CDN Setup", "[Yes / No] — [Cloudflare / AWS CloudFront]", "[Developer]"),
        ("Staging Environment", "[Yes / No]", "[Developer]"),
    ], col_widths=[2.0, 3.0, 1.5])

    doc.add_heading("3.2 Technology Stack", level=2)
    add_styled_table(doc, ["Component", "Technology", "Reason"], [
        ("Frontend", "[React / Next.js / Vue / HTML-CSS-JS]", "[Why this choice]"),
        ("Backend", "[Node.js / Python-Django / PHP-Laravel / None]", "[Why this choice]"),
        ("Database", "[MySQL / PostgreSQL / MongoDB / Firebase]", "[Why this choice]"),
        ("CMS", "[WordPress / Strapi / Custom Admin / None]", "[Why this choice]"),
        ("Styling", "[Tailwind CSS / Bootstrap / Custom CSS / Material UI]", "[Why this choice]"),
        ("Deployment", "[Vercel / Netlify / AWS / DigitalOcean / cPanel]", "[Why this choice]"),
        ("Version Control", "Git (GitHub / GitLab / Bitbucket)", "Industry standard"),
    ], col_widths=[1.8, 2.5, 2.2])

    doc.add_heading("3.3 Database Design", level=2)
    add_styled_table(doc, ["Item", "Details"], [
        ("Database Type", "[Relational (SQL) / NoSQL / Both]"),
        ("Database Service", "[MySQL / PostgreSQL / MongoDB Atlas / Firebase Firestore / Supabase]"),
        ("Schema Complexity", "[Simple / Medium / Complex]"),
        ("Data Migration", "[Yes / No] — [From: ___]"),
        ("Backup Strategy", "[Daily / Weekly] — [Automated / Manual]"),
        ("Estimated Records", "[< 1K / 1K–10K / 10K–100K / 100K+]"),
    ], col_widths=[2.0, 4.5])

    doc.add_page_break()

    doc.add_heading("3.4 Pages & Site Structure", level=2)
    doc.add_paragraph(
        "The following pages will be developed as part of this project:"
    )
    add_styled_table(doc, ["#", "Page", "Type", "Description"], [
        ("1", "Home Page", "Dynamic", "[Hero section, services overview, testimonials, CTA]"),
        ("2", "About Us", "Static/Dynamic", "[Company story, team, mission, vision]"),
        ("3", "Services", "Dynamic", "[Service listings with details]"),
        ("4", "Contact Us", "Dynamic", "[Contact form, Google Maps, company info]"),
        ("5", "Blog Listing", "Dynamic", "[Blog posts with pagination, categories]"),
        ("6", "Blog Detail", "Dynamic", "[Full article, author, related posts]"),
        ("7", "Portfolio / Gallery", "Dynamic", "[Projects showcase with filters]"),
        ("8", "FAQ", "Dynamic", "[Accordion-style FAQ section]"),
        ("9", "Privacy Policy", "Static", "[Legal privacy policy page]"),
        ("10", "Terms & Conditions", "Static", "[Legal terms page]"),
        ("—", "[Additional pages]", "—", "[Add as needed]"),
    ], col_widths=[0.5, 1.8, 1.2, 3.0])

    doc.add_heading("3.5 Features & Functionality", level=2)
    add_styled_table(doc, ["#", "Feature", "Included", "Priority", "Notes"], [
        ("1", "Responsive Design (Mobile + Tablet)", "✓", "High", "All pages"),
        ("2", "Contact Form with Email Notification", "✓", "High", "SendGrid / Nodemailer"),
        ("3", "User Registration & Login", "[✓/✗]", "[High/Low]", "[If applicable]"),
        ("4", "Admin Panel / CMS", "[✓/✗]", "[High/Low]", "[Content management]"),
        ("5", "Search with Filters", "[✓/✗]", "[High/Low]", "[Site-wide search]"),
        ("6", "Newsletter Subscription", "[✓/✗]", "[Medium]", "[Mailchimp / custom]"),
        ("7", "Live Chat Integration", "[✓/✗]", "[Low]", "[Chatbot / Intercom / Tawk.to]"),
        ("8", "Multi-language Support", "[✓/✗]", "[Low]", "[i18n setup]"),
        ("9", "Dark Mode Toggle", "[✓/✗]", "[Low]", "[Theme switcher]"),
        ("10", "Social Media Integration", "[✓/✗]", "[Medium]", "[Share, follow buttons]"),
        ("11", "Google Maps Integration", "[✓/✗]", "[Medium]", "[Contact page]"),
        ("12", "Image Gallery / Lightbox", "[✓/✗]", "[Medium]", "[Portfolio]"),
        ("13", "Booking / Appointment System", "[✓/✗]", "[High/Low]", "[Calendar integration]"),
        ("14", "User Dashboard", "[✓/✗]", "[High/Low]", "[Logged-in user area]"),
        ("15", "Push Notifications (Web)", "[✓/✗]", "[Low]", "[FCM / OneSignal]"),
    ], col_widths=[0.4, 2.5, 0.8, 0.8, 2.0])

    doc.add_page_break()

    doc.add_heading("3.6 E-Commerce Features (if applicable)", level=2)
    add_styled_table(doc, ["#", "Feature", "Included", "Notes"], [
        ("1", "Product Catalog with Categories", "[✓/✗]", ""),
        ("2", "Product Variants (Size, Color, etc.)", "[✓/✗]", ""),
        ("3", "Shopping Cart", "[✓/✗]", ""),
        ("4", "Checkout Flow (Guest + Registered)", "[✓/✗]", ""),
        ("5", "Order Management System", "[✓/✗]", ""),
        ("6", "Inventory Management", "[✓/✗]", ""),
        ("7", "Coupons / Discount Codes", "[✓/✗]", ""),
        ("8", "Wishlist Feature", "[✓/✗]", ""),
        ("9", "Product Reviews & Ratings", "[✓/✗]", ""),
        ("10", "Shipping Calculator", "[✓/✗]", ""),
        ("11", "Tax Calculation (GST)", "[✓/✗]", ""),
        ("12", "Invoice Generation (PDF)", "[✓/✗]", ""),
        ("13", "Return / Refund System", "[✓/✗]", ""),
    ], col_widths=[0.4, 2.8, 0.8, 2.5])

    doc.add_heading("3.7 Payment Integration", level=2)
    add_styled_table(doc, ["Gateway", "Included", "Features", "Transaction Fees"], [
        ("Razorpay", "[✓/✗]", "UPI, Cards, Wallets, Net Banking", "2% per transaction"),
        ("Stripe", "[✓/✗]", "Cards, Apple Pay, Google Pay", "2.9% + 30¢"),
        ("PayPal", "[✓/✗]", "International payments", "3.49% + ₹3"),
        ("UPI Direct", "[✓/✗]", "PhonePe, GPay, Paytm", "0% (up to ₹2,000)"),
        ("Cash on Delivery", "[✓/✗]", "Manual order processing", "N/A"),
    ], col_widths=[1.5, 0.8, 2.5, 1.7])

    doc.add_heading("3.8 SEO & Analytics", level=2)
    add_styled_table(doc, ["#", "Item", "Included"], [
        ("1", "On-Page SEO (Meta tags, headings, alt text)", "✓"),
        ("2", "Sitemap.xml Generation", "✓"),
        ("3", "Robots.txt Configuration", "✓"),
        ("4", "Google Analytics 4 Setup", "✓"),
        ("5", "Google Search Console Setup", "✓"),
        ("6", "Schema Markup (Structured Data)", "[✓/✗]"),
        ("7", "Google Tag Manager Setup", "[✓/✗]"),
        ("8", "Facebook Pixel Setup", "[✓/✗]"),
        ("9", "Page Speed Optimization", "✓"),
        ("10", "Open Graph Tags for Social Sharing", "✓"),
    ], col_widths=[0.4, 3.5, 2.6])

    doc.add_heading("3.9 Security Measures", level=2)
    add_styled_table(doc, ["#", "Measure", "Included"], [
        ("1", "SSL/TLS Encryption (HTTPS)", "✓"),
        ("2", "Security Headers (CSP, HSTS, X-Frame)", "✓"),
        ("3", "Input Validation & Sanitization", "✓"),
        ("4", "SQL Injection Prevention", "✓"),
        ("5", "XSS Protection", "✓"),
        ("6", "CSRF Protection", "✓"),
        ("7", "Rate Limiting", "[✓/✗]"),
        ("8", "CAPTCHA (reCAPTCHA)", "[✓/✗]"),
        ("9", "Firewall (WAF)", "[✓/✗]"),
        ("10", "DDoS Protection", "[✓/✗]"),
        ("11", "GDPR Compliance", "[✓/✗]"),
        ("12", "Two-Factor Authentication", "[✓/✗]"),
    ], col_widths=[0.4, 3.5, 2.6])

    doc.add_page_break()

    # ── Section 4: Design Approach ─────────────────────────────────
    add_heading_styled(doc, "4. Design Approach", level=1)

    add_styled_table(doc, ["Parameter", "Details"], [
        ("Design Style", "[Minimalist / Modern / Corporate / Playful / Luxury]"),
        ("Design Tool", "[Figma / Adobe XD / Sketch]"),
        ("Wireframes", "[Yes / No] — [Low-fidelity / High-fidelity]"),
        ("UI Mockups", "[Yes / No] — [Number of pages]"),
        ("Responsive Design", "Desktop + Tablet + Mobile"),
        ("Dark Mode", "[Yes / No]"),
        ("Animations", "[None / Basic / Advanced (GSAP/Lottie)]"),
        ("Design Revisions", "[2 / 3 / 5] rounds of revisions"),
        ("Design Handoff", "Figma link with assets and specs"),
    ], col_widths=[2.0, 4.5])

    doc.add_page_break()

    # ── Section 5: Project Timeline ────────────────────────────────
    add_heading_styled(doc, "5. Project Timeline", level=1)
    doc.add_paragraph(
        "The project will follow an agile approach with defined milestones. "
        "Timelines are estimates and depend on timely client feedback."
    )

    add_styled_table(doc, ["Phase", "Tasks", "Duration", "Deliverable"], [
        ("Phase 1: Discovery & Planning", "Requirements gathering, sitemap, wireframes", "Week 1–2", "Scope document, wireframes"),
        ("Phase 2: Design", "UI/UX design, mockups, revisions", "Week 3–4", "Approved Figma designs"),
        ("Phase 3: Frontend Development", "HTML/CSS/JS or framework implementation", "Week 5–7", "Functional frontend"),
        ("Phase 4: Backend Development", "API, database, business logic, CMS", "Week 6–8", "Working backend + admin"),
        ("Phase 5: Integration", "Frontend-backend integration, APIs", "Week 8–9", "Integrated application"),
        ("Phase 6: Testing & QA", "Cross-browser, mobile, performance, security", "Week 9–10", "QA report, bug fixes"),
        ("Phase 7: Content & SEO", "Content upload, SEO setup, analytics", "Week 10–11", "SEO-ready site"),
        ("Phase 8: Launch", "Server setup, DNS, SSL, go-live", "Week 11–12", "Live website"),
        ("Phase 9: Post-Launch", "Monitoring, fixes, training, handover", "Week 12–13", "Complete handover"),
    ], col_widths=[1.8, 2.0, 1.2, 1.5])

    p = doc.add_paragraph()
    run = p.add_run("\nNote: ")
    run.font.bold = True
    p.add_run("Timelines may vary based on project complexity and client response times. "
              "Delays in feedback may shift subsequent milestones.")

    doc.add_page_break()

    # ── Section 6: Pricing ─────────────────────────────────────────
    add_heading_styled(doc, "6. Pricing Breakdown", level=1)
    doc.add_paragraph(
        "The following is a detailed cost breakdown for the project. "
        "All prices are in Indian Rupees (₹). USD equivalents are provided for reference."
    )

    add_styled_table(doc, ["#", "Category", "Description", "Cost (₹)", "Cost ($)"], [
        ("1", "Domain & SSL", "Domain registration + SSL setup", "[₹X,XXX]", "[$XX]"),
        ("2", "Hosting (Annual)", "Server setup + configuration", "[₹X,XXX]", "[$XX]"),
        ("3", "Design & UI/UX", "Wireframes + mockups + revisions", "[₹XX,XXX]", "[$XXX]"),
        ("4", "Frontend Development", "All pages + responsive design", "[₹XX,XXX]", "[$XXX]"),
        ("5", "Backend Development", "API + database + business logic", "[₹XX,XXX]", "[$XXX]"),
        ("6", "CMS / Admin Panel", "Content management system", "[₹XX,XXX]", "[$XXX]"),
        ("7", "Features & Integrations", "All listed features", "[₹XX,XXX]", "[$XXX]"),
        ("8", "E-Commerce (if applicable)", "Cart, checkout, orders", "[₹XX,XXX]", "[$XXX]"),
        ("9", "Payment Integration", "Gateway setup + testing", "[₹X,XXX]", "[$XX]"),
        ("10", "SEO & Analytics Setup", "On-page SEO, GA4, GSC", "[₹X,XXX]", "[$XX]"),
        ("11", "Security Setup", "SSL, headers, firewall", "[₹X,XXX]", "[$XX]"),
        ("12", "Testing & QA", "Cross-browser, performance, security", "[₹X,XXX]", "[$XX]"),
        ("13", "Content Upload", "Pages, images, data entry", "[₹X,XXX]", "[$XX]"),
        ("14", "Deployment & Launch", "Server, domain, go-live", "[₹X,XXX]", "[$XX]"),
        ("", "", "", "", ""),
        ("", "SUBTOTAL", "", "[₹X,XX,XXX]", "[$X,XXX]"),
        ("", "Complexity Multiplier", "[1.0x / 1.5x / 2.0x]", "—", "—"),
        ("", "Discount", "[X%]", "[−₹X,XXX]", "[−$XX]"),
        ("", "GST (18%)", "", "[₹XX,XXX]", "[$XXX]"),
        ("", "GRAND TOTAL", "", "[₹X,XX,XXX]", "[$X,XXX]"),
    ], col_widths=[0.4, 1.8, 2.0, 1.1, 1.1])

    doc.add_page_break()

    # ── Section 7: Payment Terms ───────────────────────────────────
    add_heading_styled(doc, "7. Payment Terms", level=1)

    add_styled_table(doc, ["Milestone", "Percentage", "Amount (₹)", "Due Date"], [
        ("Advance (Before project starts)", "40%", "[₹XX,XXX]", "[Date]"),
        ("After Design Approval", "25%", "[₹XX,XXX]", "[Date]"),
        ("After Development Completion", "25%", "[₹XX,XXX]", "[Date]"),
        ("After Launch & Handover", "10%", "[₹XX,XXX]", "[Date]"),
        ("TOTAL", "100%", "[₹X,XX,XXX]", "—"),
    ], col_widths=[2.5, 1.2, 1.5, 1.3])

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Payment Methods Accepted: ")
    run.font.bold = True
    p.add_run("Bank Transfer (NEFT/RTGS/IMPS), UPI, PayPal, Razorpay")

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Important Notes:")
    run.font.bold = True
    doc.add_paragraph("• Work begins only after receipt of advance payment.", style='List Bullet')
    doc.add_paragraph("• Invoices will be raised at each milestone.", style='List Bullet')
    doc.add_paragraph("• Late payments may delay project timeline.", style='List Bullet')
    doc.add_paragraph("• Additional features/changes outside scope will be quoted separately.", style='List Bullet')

    doc.add_page_break()

    # ── Section 8: Maintenance & Support ───────────────────────────
    add_heading_styled(doc, "8. Maintenance & Support Plans", level=1)
    doc.add_paragraph(
        "Post-launch maintenance ensures your website remains secure, updated, and performant. "
        "Choose a plan that fits your needs."
    )

    add_styled_table(doc, ["Feature", "Basic\n₹3K/mo", "Standard\n₹8K/mo", "Professional\n₹15K/mo"], [
        ("Uptime Monitoring", "✓", "✓", "✓"),
        ("Monthly Backups", "✓", "✓", "✓ (Daily)"),
        ("Security Updates", "Quarterly", "Monthly", "Weekly"),
        ("Bug Fixes", "Critical only", "All bugs", "Priority fixes"),
        ("Content Updates", "2/month", "5/month", "10/month"),
        ("Performance Monitoring", "✗", "Basic", "Advanced"),
        ("SEO Monitoring", "✗", "Basic", "Full reports"),
        ("Support Response Time", "48 hours", "24 hours", "12 hours"),
        ("Support Channels", "Email", "Email + Chat", "Email + Chat + Call"),
        ("Feature Enhancements", "✗", "1 small/mo", "2 small/mo"),
    ], col_widths=[2.0, 1.3, 1.5, 1.7])

    doc.add_page_break()

    # ── Section 9: What We Need From You ───────────────────────────
    add_heading_styled(doc, "9. What We Need From You", level=1)
    doc.add_paragraph(
        "To ensure smooth project execution, we'll need the following from your side:"
    )

    items = [
        "Logo and brand assets (if available)",
        "Brand guidelines — colors, fonts, style preferences",
        "Content — text, images, videos for each page",
        "Domain and hosting credentials (if already owned)",
        "Reference websites you like (for design direction)",
        "Product data / catalog (for e-commerce projects)",
        "Payment gateway merchant credentials",
        "Timely feedback on designs and deliverables (within 2–3 business days)",
        "A single point of contact from your team",
        "Any legal content — privacy policy, terms, etc.",
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_page_break()

    # ── Section 10: Terms & Conditions ─────────────────────────────
    add_heading_styled(doc, "10. Terms & Conditions", level=1)

    terms = [
        ("Scope", "This proposal covers only the items listed in the Scope of Work. Any additional features or changes will be quoted separately."),
        ("Intellectual Property", "Upon full payment, all custom code, designs, and content created for this project will be transferred to the client. Third-party licenses (themes, plugins, fonts) remain under their respective licenses."),
        ("Confidentiality", "Both parties agree to keep all project information confidential. An NDA can be signed upon request."),
        ("Timeline", "Delays caused by late client feedback, content delivery, or scope changes may shift the project timeline. Developer is not responsible for delays outside their control."),
        ("Revisions", "Design revisions are limited to the number specified in this proposal. Additional revisions will be charged at [₹X,XXX] per round."),
        ("Cancellation", "If the project is cancelled after commencement, all payments made up to that point are non-refundable. Work completed will be delivered."),
        ("Warranty", "A [30/60/90]-day warranty period is included after launch for bug fixes. This does not cover new features, content changes, or third-party issues."),
        ("Support", "Post-warranty support is available through maintenance plans (see Section 8) or hourly billing at [₹X,XXX/hr]."),
        ("Third-Party Services", "Recurring costs for hosting, domain, email, APIs, and third-party services are the client's responsibility after handover."),
        ("Liability", "Developer is not liable for losses arising from hosting failures, third-party service outages, or client-side mismanagement."),
    ]
    for title, desc in terms:
        p = doc.add_paragraph()
        run = p.add_run(f"{title}: ")
        run.font.bold = True
        p.add_run(desc)

    doc.add_page_break()

    # ── Section 11: Why Choose Us ──────────────────────────────────
    add_heading_styled(doc, "11. Why Choose Us", level=1)
    doc.add_paragraph(
        "[Customize this section with your strengths, experience, and unique selling points.]"
    )

    points = [
        "✓ [X]+ years of experience in web development",
        "✓ [X]+ projects delivered successfully",
        "✓ Expertise in modern technologies (React, Next.js, Node.js, etc.)",
        "✓ End-to-end service — design, development, deployment, maintenance",
        "✓ Focus on performance, security, and scalability",
        "✓ Transparent communication and regular updates",
        "✓ Post-launch support and maintenance",
        "✓ Competitive pricing with no hidden costs",
    ]
    for point in points:
        doc.add_paragraph(point)

    doc.add_page_break()

    # ── Section 12: Acceptance ─────────────────────────────────────
    add_heading_styled(doc, "12. Proposal Acceptance", level=1)
    doc.add_paragraph(
        "By signing below, you accept this proposal and agree to the scope, pricing, "
        "timeline, and terms outlined in this document."
    )

    doc.add_paragraph("")

    # Signature table
    table = doc.add_table(rows=5, cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ["Client", "Developer"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = WHITE
        set_cell_shading(cell, "1B2A4A")

    labels = ["Name:", "Company:", "Signature:", "Date:"]
    for r, label in enumerate(labels, 1):
        for c in range(2):
            cell = table.rows[r].cells[c]
            cell.text = label
            cell.paragraphs[0].runs[0].font.size = Pt(10)

    doc.add_paragraph("")
    doc.add_paragraph("")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("This proposal is valid for 30 days from the date of issue.")
    run.font.italic = True
    run.font.color.rgb = DARK_GRAY

    doc.save(path)
    print(f"✅ Created: {path}")


# ════════════════════════════════════════════════════════════════════
# APPLICATION CLIENT PROPOSAL
# ════════════════════════════════════════════════════════════════════

def create_application_proposal(path):
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Cover Page
    add_cover_page(
        doc,
        "Mobile Application\nDevelopment Proposal",
        "iOS & Android App Solutions"
    )

    # Table of Contents
    add_toc_placeholder(doc)

    # ── Section 1: Executive Summary ───────────────────────────────
    add_heading_styled(doc, "1. Executive Summary", level=1)
    doc.add_paragraph(
        "Thank you for considering us for your mobile application development project. "
        "This proposal outlines our understanding of your requirements, development approach, "
        "technology stack, timeline, pricing, and terms of engagement.\n\n"
        "We are committed to building a high-quality, performant, and user-friendly mobile application "
        "that delivers real value to your users and meets your business goals."
    )

    add_styled_table(doc, ["Parameter", "Details"], [
        ("Project Name", "[App Name]"),
        ("Client", "[Client Name / Company]"),
        ("App Type", "[E-Commerce / Social / On-Demand / Education / Finance / Health / Other]"),
        ("Platforms", "[Android only / iOS only / Both (Android + iOS)]"),
        ("Development Approach", "[Native (Swift + Kotlin) / Cross-Platform (Flutter / React Native)]"),
        ("Estimated Duration", "[X months]"),
        ("Estimated Budget", "[₹X,XX,XXX — ₹X,XX,XXX]"),
    ], col_widths=[2.5, 4.0])

    doc.add_page_break()

    # ── Section 2: Project Understanding ───────────────────────────
    add_heading_styled(doc, "2. Project Understanding", level=1)
    doc.add_paragraph(
        "[Describe your understanding of the client's business, the app's purpose, "
        "target audience, and key problems the app will solve.]"
    )

    doc.add_heading("2.1 Business Overview", level=2)
    doc.add_paragraph("[Client's business description, current digital presence, and app motivation.]")

    doc.add_heading("2.2 App Purpose & Goals", level=2)
    doc.add_paragraph(
        "• [Goal 1 — e.g., Enable users to order food from local restaurants]\n"
        "• [Goal 2 — e.g., Provide real-time tracking of deliveries]\n"
        "• [Goal 3 — e.g., Build a loyal customer base through rewards]\n"
        "• [Goal 4 — e.g., Generate revenue through commissions and ads]"
    )

    doc.add_heading("2.3 Target Audience", level=2)
    doc.add_paragraph("[Describe users — age, location, behavior, devices, pain points.]")

    doc.add_heading("2.4 Competitors", level=2)
    doc.add_paragraph("[List competitor apps organized by name and unique advantages they have.]")

    doc.add_page_break()

    # ── Section 3: Scope of Work ───────────────────────────────────
    add_heading_styled(doc, "3. Scope of Work", level=1)

    doc.add_heading("3.1 Platform & Technology", level=2)
    add_styled_table(doc, ["Component", "Choice", "Rationale"], [
        ("Target Platforms", "[Android + iOS]", "[Market coverage]"),
        ("Development Approach", "[Flutter / React Native / Native]", "[Why this framework]"),
        ("iOS Language", "[Dart (Flutter) / Swift (Native)]", "—"),
        ("Android Language", "[Dart (Flutter) / Kotlin (Native)]", "—"),
        ("Min iOS Version", "[iOS 14+ / iOS 15+]", "[Device coverage]"),
        ("Min Android Version", "[Android 8+ (API 26) / Android 10+]", "[Device coverage]"),
        ("Architecture", "[Clean Architecture / MVVM / BLoC]", "[Maintainability]"),
        ("State Management", "[BLoC / Riverpod / Redux / Provider]", "[For chosen framework]"),
        ("Tablet Support", "[Yes / No]", "[User need]"),
    ], col_widths=[2.0, 2.5, 2.0])

    doc.add_heading("3.2 App Store & Deployment", level=2)
    add_styled_table(doc, ["Item", "Details", "Cost"], [
        ("Google Play Developer Account", "[Client has / Need to create]", "₹2,100 ($25) one-time"),
        ("Apple Developer Account", "[Client has / Need to create]", "₹8,300 ($99) per year"),
        ("App Store Listing — Android", "[Developer handles]", "₹3,000–5,000"),
        ("App Store Listing — iOS", "[Developer handles]", "₹5,000–8,000"),
        ("App Store Screenshots Design", "[Per platform]", "₹5,000–10,000"),
        ("App Store Optimization (ASO)", "[Initial setup]", "₹5,000–15,000"),
        ("Beta Testing Setup", "[TestFlight + Play Console]", "₹3,000–5,000"),
        ("CI/CD Pipeline", "[GitHub Actions / Fastlane / Codemagic]", "₹8,000–20,000"),
    ], col_widths=[2.5, 2.0, 2.0])

    doc.add_heading("3.3 Backend & API", level=2)
    add_styled_table(doc, ["Component", "Choice", "Notes"], [
        ("Backend Type", "[Custom (Node.js/Python/Go) / Firebase / Supabase]", "[Why]"),
        ("API Style", "[REST / GraphQL]", "[Standard]"),
        ("Database", "[PostgreSQL / MongoDB / Firestore / MySQL]", "[Why]"),
        ("Cloud Storage", "[AWS S3 / Firebase Storage / GCS]", "[For media files]"),
        ("Authentication", "[Firebase Auth / Custom JWT / Auth0]", "[Why]"),
        ("Real-time", "[WebSocket / Firebase Realtime / Supabase Realtime]", "[If needed]"),
        ("Cloud Functions", "[Firebase Functions / AWS Lambda / Custom]", "[Background tasks]"),
        ("Admin Dashboard", "[Web-based admin panel]", "[For content/user management]"),
        ("Hosting", "[AWS / GCP / Firebase / DigitalOcean / Railway]", "[Why]"),
    ], col_widths=[1.8, 2.5, 2.2])

    doc.add_page_break()

    doc.add_heading("3.4 App Screens & Navigation", level=2)
    doc.add_paragraph("The following screens will be designed and developed:")

    add_styled_table(doc, ["#", "Screen", "Complexity", "Description"], [
        ("1", "Splash Screen", "Simple", "App logo + loading animation"),
        ("2", "Onboarding (3–5 screens)", "Simple", "App introduction walkthrough"),
        ("3", "Login / Register", "Medium", "Email, phone, social login"),
        ("4", "Home / Main Screen", "Complex", "Primary content, navigation hub"),
        ("5", "Profile Screen", "Medium", "User info, settings, photo"),
        ("6", "Settings", "Simple", "App configuration, preferences"),
        ("7", "Search + Filters", "Complex", "Dynamic search with filters"),
        ("8", "Detail Screen", "Medium", "Item/product/content details"),
        ("9", "List / Feed Screen", "Medium", "Scrollable content with pagination"),
        ("10", "Notification Center", "Medium", "Push notification history"),
        ("11", "Chat / Messages", "Complex", "[If applicable]"),
        ("12", "Cart + Checkout", "Complex", "[If e-commerce]"),
        ("13", "Order History / Tracking", "Medium", "[If applicable]"),
        ("14", "Help / Support", "Simple", "FAQ, contact support"),
        ("—", "[Additional Screens]", "—", "[Add as needed]"),
    ], col_widths=[0.4, 2.0, 1.0, 3.1])

    doc.add_heading("3.5 Features & Functionality", level=2)
    add_styled_table(doc, ["#", "Feature", "Included", "Priority"], [
        ("1", "Email/Password Authentication", "[✓/✗]", "High"),
        ("2", "Phone/OTP Authentication", "[✓/✗]", "High"),
        ("3", "Google Sign-In", "[✓/✗]", "Medium"),
        ("4", "Apple Sign-In (Required by Apple if social login exists)", "[✓/✗]", "High"),
        ("5", "Biometric Auth (Fingerprint / Face ID)", "[✓/✗]", "Medium"),
        ("6", "Push Notifications", "[✓/✗]", "High"),
        ("7", "In-App Messaging / Chat", "[✓/✗]", "[High/Low]"),
        ("8", "GPS / Location Services", "[✓/✗]", "[High/Low]"),
        ("9", "Google Maps / Navigation", "[✓/✗]", "[High/Low]"),
        ("10", "Camera / Gallery Integration", "[✓/✗]", "Medium"),
        ("11", "QR/Barcode Scanner", "[✓/✗]", "[High/Low]"),
        ("12", "File Upload / Download", "[✓/✗]", "Medium"),
        ("13", "Offline Mode & Data Sync", "[✓/✗]", "[High/Low]"),
        ("14", "Multi-language Support (i18n)", "[✓/✗]", "Low"),
        ("15", "Dark Mode", "[✓/✗]", "Low"),
        ("16", "Social Sharing", "[✓/✗]", "Low"),
        ("17", "Deep Linking / Universal Links", "[✓/✗]", "Medium"),
        ("18", "Accessibility Support", "[✓/✗]", "Medium"),
        ("19", "Background Location Tracking", "[✓/✗]", "[High/Low]"),
        ("20", "Audio / Video Player", "[✓/✗]", "[High/Low]"),
    ], col_widths=[0.4, 3.5, 0.8, 1.0])

    doc.add_page_break()

    doc.add_heading("3.6 Payment Integration (if applicable)", level=2)
    add_styled_table(doc, ["Gateway / Method", "Included", "Notes"], [
        ("Razorpay (UPI, Cards, Wallets)", "[✓/✗]", "India-focused, 2% fee"),
        ("Stripe (Cards, Apple Pay, Google Pay)", "[✓/✗]", "International, 2.9% + 30¢"),
        ("PayPal", "[✓/✗]", "International payments"),
        ("Google Pay / Apple Pay (Native)", "[✓/✗]", "One-tap payment"),
        ("In-App Purchases (IAP)", "[✓/✗]", "Required for digital goods, 15–30% commission"),
        ("Subscription (Auto-renewing)", "[✓/✗]", "Monthly/annual plans"),
        ("Wallet / Credits System", "[✓/✗]", "In-app currency"),
        ("Cash on Delivery", "[✓/✗]", "For physical goods"),
    ], col_widths=[2.5, 0.8, 3.2])

    doc.add_heading("3.7 Security Measures", level=2)
    add_styled_table(doc, ["#", "Security Feature", "Included"], [
        ("1", "Data Encryption (at rest + in transit — TLS 1.3)", "✓"),
        ("2", "Secure Token Storage (Keychain / Keystore)", "✓"),
        ("3", "Certificate Pinning", "[✓/✗]"),
        ("4", "Jailbreak / Root Detection", "[✓/✗]"),
        ("5", "Code Obfuscation (ProGuard / R8)", "✓"),
        ("6", "Biometric Authentication", "[✓/✗]"),
        ("7", "Two-Factor Authentication", "[✓/✗]"),
        ("8", "API Key Protection", "✓"),
        ("9", "Input Validation", "✓"),
        ("10", "Session Management & Auto-logout", "✓"),
        ("11", "GDPR Compliance", "[✓/✗]"),
        ("12", "Account Deletion Feature (Apple requirement)", "✓"),
    ], col_widths=[0.4, 3.5, 2.6])

    doc.add_heading("3.8 Testing & Quality Assurance", level=2)
    add_styled_table(doc, ["Testing Type", "Included", "Details"], [
        ("Unit Testing", "✓", "Core business logic tests"),
        ("Widget/UI Testing", "[✓/✗]", "Component-level tests"),
        ("Integration Testing", "✓", "API + feature flow tests"),
        ("Manual Testing", "✓", "Complete user flow testing"),
        ("Beta Testing", "[✓/✗]", "TestFlight + Play Console internal testing"),
        ("Device Compatibility", "✓", "Top 10–15 device models"),
        ("Performance Testing", "✓", "Load time, memory, battery"),
        ("Security Testing", "[✓/✗]", "OWASP mobile checklist"),
        ("Crash Reporting Setup", "✓", "Crashlytics / Sentry"),
    ], col_widths=[1.8, 0.8, 3.9])

    doc.add_page_break()

    # ── Section 4: Design Approach ─────────────────────────────────
    add_heading_styled(doc, "4. Design Approach", level=1)

    add_styled_table(doc, ["Parameter", "Details"], [
        ("Design Style", "[Material Design / iOS HIG / Custom / Minimalist / Modern]"),
        ("Design Tool", "Figma"),
        ("User Flow Diagrams", "✓ — All major user journeys"),
        ("Wireframes", "[Yes / No]"),
        ("High-Fidelity Mockups", "✓ — All screens"),
        ("Interactive Prototype", "[Yes / No]"),
        ("Dark Mode", "[Yes / No]"),
        ("Animations", "[Basic transitions / Custom Lottie / Advanced]"),
        ("Design Revisions", "[2 / 3 / 5] rounds"),
        ("Tablet Layout", "[Responsive / Dedicated / Not included]"),
        ("App Icon Design", "✓ — All platform sizes"),
        ("Splash Screen Design", "✓"),
        ("Onboarding Screens", "✓ — [3–5 screens]"),
        ("Design System", "[Yes — component library / No]"),
    ], col_widths=[2.0, 4.5])

    doc.add_page_break()

    # ── Section 5: Project Timeline ────────────────────────────────
    add_heading_styled(doc, "5. Project Timeline", level=1)
    doc.add_paragraph(
        "The project follows an agile methodology with 2-week sprints. "
        "Timelines depend on timely feedback and scope stability."
    )

    add_styled_table(doc, ["Phase", "Tasks", "Duration", "Deliverable"], [
        ("Phase 1: Discovery", "Requirements, user stories, user flows", "Week 1–2", "PRD, user flows"),
        ("Phase 2: Design", "Wireframes, UI design, prototype", "Week 3–5", "Approved Figma designs"),
        ("Phase 3: Backend Setup", "API, database, auth, cloud services", "Week 4–6", "Working API + docs"),
        ("Phase 4: App Development", "Core screens, navigation, features", "Week 6–12", "Working app (alpha)"),
        ("Phase 5: Integration", "API integration, state management", "Week 10–13", "Integrated app (beta)"),
        ("Phase 6: Testing", "QA, bug fixes, device testing", "Week 13–15", "QA report, stable build"),
        ("Phase 7: Beta Release", "Internal + external beta testing", "Week 15–16", "Beta feedback"),
        ("Phase 8: Polish & Fix", "Final fixes, performance, polish", "Week 16–17", "Release candidate"),
        ("Phase 9: Launch", "App store submission, monitoring", "Week 17–18", "Live on stores"),
        ("Phase 10: Post-Launch", "Crash monitoring, fixes, handover", "Week 18–20", "Complete handover"),
    ], col_widths=[1.5, 2.2, 1.2, 1.6])

    p = doc.add_paragraph()
    run = p.add_run("\nNote: ")
    run.font.bold = True
    p.add_run("App store review typically takes 1–7 days for iOS and 1–3 days for Android. "
              "Rejection requires resubmission which adds to timeline.")

    doc.add_page_break()

    # ── Section 6: Pricing ─────────────────────────────────────────
    add_heading_styled(doc, "6. Pricing Breakdown", level=1)
    doc.add_paragraph(
        "Detailed cost breakdown for the mobile application project. "
        "All prices in Indian Rupees (₹) with USD equivalents."
    )

    add_styled_table(doc, ["#", "Category", "Description", "Cost (₹)", "Cost ($)"], [
        ("1", "App Store Accounts", "Google Play + Apple Developer", "[₹10,100]", "[$124]"),
        ("2", "UI/UX Design", "All screens + prototype + revisions", "[₹XX,XXX]", "[$XXX]"),
        ("3", "App Development", "All screens + features (both platforms)", "[₹X,XX,XXX]", "[$X,XXX]"),
        ("4", "Authentication System", "Login, register, social, biometric", "[₹XX,XXX]", "[$XXX]"),
        ("5", "Backend & API", "Server, API, database, cloud functions", "[₹XX,XXX]", "[$XXX]"),
        ("6", "Admin Dashboard", "Web-based management panel", "[₹XX,XXX]", "[$XXX]"),
        ("7", "Push Notifications", "FCM / APNs setup + backend", "[₹X,XXX]", "[$XX]"),
        ("8", "Payment Integration", "Gateway setup + testing", "[₹XX,XXX]", "[$XXX]"),
        ("9", "Third-Party Integrations", "Maps, SMS, email, analytics", "[₹XX,XXX]", "[$XXX]"),
        ("10", "Testing & QA", "Unit, integration, device, beta", "[₹XX,XXX]", "[$XXX]"),
        ("11", "App Store Submission", "Both platforms + ASO", "[₹X,XXX]", "[$XX]"),
        ("12", "Deployment & DevOps", "CI/CD, server setup, monitoring", "[₹XX,XXX]", "[$XXX]"),
        ("", "", "", "", ""),
        ("", "SUBTOTAL", "", "[₹X,XX,XXX]", "[$X,XXX]"),
        ("", "Platform Multiplier", "[1.0x / 1.3x / 1.5x / 2.0x]", "—", "—"),
        ("", "Complexity Multiplier", "[1.0x / 1.5x / 2.0x]", "—", "—"),
        ("", "Discount", "[X%]", "[−₹X,XXX]", "[−$XX]"),
        ("", "GST (18%)", "", "[₹XX,XXX]", "[$XXX]"),
        ("", "GRAND TOTAL", "", "[₹X,XX,XXX]", "[$X,XXX]"),
    ], col_widths=[0.4, 1.8, 2.0, 1.1, 1.1])

    doc.add_page_break()

    # ── Section 7: Payment Terms ───────────────────────────────────
    add_heading_styled(doc, "7. Payment Terms", level=1)

    add_styled_table(doc, ["Milestone", "Percentage", "Amount (₹)", "Due Date"], [
        ("Advance (Before project starts)", "35%", "[₹XX,XXX]", "[Date]"),
        ("After Design Approval", "20%", "[₹XX,XXX]", "[Date]"),
        ("After App Development", "25%", "[₹XX,XXX]", "[Date]"),
        ("After Testing & Store Submission", "10%", "[₹XX,XXX]", "[Date]"),
        ("After Launch & Handover", "10%", "[₹XX,XXX]", "[Date]"),
        ("TOTAL", "100%", "[₹X,XX,XXX]", "—"),
    ], col_widths=[2.5, 1.2, 1.5, 1.3])

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Payment Methods Accepted: ")
    run.font.bold = True
    p.add_run("Bank Transfer (NEFT/RTGS/IMPS), UPI, PayPal, Razorpay")

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Important Notes:")
    run.font.bold = True
    doc.add_paragraph("• Work begins only after receipt of advance payment.", style='List Bullet')
    doc.add_paragraph("• App store account costs are separate and billed at actuals.", style='List Bullet')
    doc.add_paragraph("• Third-party service costs (hosting, APIs, SMS) are billed monthly at actuals.", style='List Bullet')
    doc.add_paragraph("• Additional features outside scope will be quoted separately.", style='List Bullet')

    doc.add_page_break()

    # ── Section 8: Maintenance & Support ───────────────────────────
    add_heading_styled(doc, "8. Maintenance & Support Plans", level=1)
    doc.add_paragraph(
        "Mobile apps require ongoing maintenance for OS updates, security patches, "
        "bug fixes, and feature updates. Choose a plan that fits your needs."
    )

    add_styled_table(doc, ["Feature", "Basic\n₹5K/mo", "Standard\n₹12K/mo", "Professional\n₹25K/mo"], [
        ("Crash Monitoring", "✓", "✓", "✓"),
        ("Bug Fixes", "Critical only", "All bugs", "All + Priority"),
        ("OS Compatibility Updates", "Yearly", "6 months", "Quarterly"),
        ("Library/SDK Updates", "✗", "Quarterly", "Monthly"),
        ("App Store Compliance", "✗", "✓", "✓"),
        ("Performance Monitoring", "Basic", "Standard", "Advanced"),
        ("Server/API Monitoring", "✗", "Basic", "Full"),
        ("Database Backups", "Weekly", "Daily", "Daily"),
        ("Security Patches", "Quarterly", "Monthly", "Bi-weekly"),
        ("Small Feature Updates", "✗", "1/month", "2/month"),
        ("App Store Updates", "2/year", "4/year", "Monthly"),
        ("Support Response Time", "48 hours", "24 hours", "12 hours"),
        ("Support Channels", "Email", "Email + Chat", "All channels"),
    ], col_widths=[2.0, 1.3, 1.5, 1.7])

    doc.add_page_break()

    # ── Section 9: What We Need From You ───────────────────────────
    add_heading_styled(doc, "9. What We Need From You", level=1)
    doc.add_paragraph(
        "To ensure smooth project execution, we'll need the following:"
    )

    items = [
        "App concept and feature list (we'll help refine this)",
        "Logo and brand assets (if available)",
        "Brand guidelines — colors, fonts, style preferences",
        "Content — text, images, product data",
        "Apple Developer account credentials (or we create one)",
        "Google Play Console access",
        "Payment gateway merchant credentials (if applicable)",
        "API documentation (if integrating with existing systems)",
        "Test device access (if targeting specific devices)",
        "Timely feedback on designs and builds (within 2–3 business days)",
        "A single point of contact from your team",
        "Legal content — privacy policy, terms of service",
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_page_break()

    # ── Section 10: Terms & Conditions ─────────────────────────────
    add_heading_styled(doc, "10. Terms & Conditions", level=1)

    terms = [
        ("Scope", "This proposal covers only the items listed. Any additional features, screens, or changes will be quoted separately."),
        ("Intellectual Property", "Upon full payment, all custom code and designs are transferred to the client. Third-party libraries remain under their respective open-source licenses."),
        ("Confidentiality", "Both parties agree to keep project details confidential. NDA available upon request."),
        ("App Store Fees", "Apple charges 15–30% commission on in-app purchases and subscriptions. Google charges 15% for the first $1M, then 30%. These are not developer fees."),
        ("App Store Review", "App store review processes are controlled by Apple and Google. Rejections require fixes and resubmission. Developer will handle this at no extra cost during the project period."),
        ("Timeline", "Delays from late feedback, scope changes, or content delivery may shift milestones. Developer is not responsible for delays outside their control."),
        ("Revisions", "Design revisions are limited as specified. Additional revisions at [₹X,XXX] per round."),
        ("Cancellation", "Payments made are non-refundable after work begins. Completed work will be delivered."),
        ("Warranty", "[30/60/90]-day warranty for bug fixes after launch. Does not cover new features, content changes, or third-party issues."),
        ("Ongoing Costs", "Hosting, domain, APIs, SMS, push notification services, and app store accounts are recurring costs — client's responsibility after handover."),
        ("Liability", "Developer is not liable for app store rejections due to client requirements, third-party service outages, or business losses."),
    ]
    for title, desc in terms:
        p = doc.add_paragraph()
        run = p.add_run(f"{title}: ")
        run.font.bold = True
        p.add_run(desc)

    doc.add_page_break()

    # ── Section 11: Why Choose Us ──────────────────────────────────
    add_heading_styled(doc, "11. Why Choose Us", level=1)
    doc.add_paragraph(
        "[Customize this section with your app development expertise and unique selling points.]"
    )

    points = [
        "✓ [X]+ years of mobile app development experience",
        "✓ [X]+ apps published on Play Store and App Store",
        "✓ Expertise in Flutter / React Native / Native development",
        "✓ End-to-end development — design, development, backend, deployment, maintenance",
        "✓ Focus on performance, security, and user experience",
        "✓ Experience with app store guidelines and approval processes",
        "✓ Post-launch monitoring, crash reporting, and support",
        "✓ Transparent communication with regular build deliveries",
        "✓ Competitive pricing with detailed breakdowns",
    ]
    for point in points:
        doc.add_paragraph(point)

    doc.add_page_break()

    # ── Section 12: Acceptance ─────────────────────────────────────
    add_heading_styled(doc, "12. Proposal Acceptance", level=1)
    doc.add_paragraph(
        "By signing below, you accept this proposal and agree to the scope, pricing, "
        "timeline, and terms outlined in this document."
    )

    doc.add_paragraph("")

    # Signature table
    table = doc.add_table(rows=5, cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ["Client", "Developer"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = WHITE
        set_cell_shading(cell, "1B2A4A")

    labels = ["Name:", "Company:", "Signature:", "Date:"]
    for r, label in enumerate(labels, 1):
        for c in range(2):
            cell = table.rows[r].cells[c]
            cell.text = label
            cell.paragraphs[0].runs[0].font.size = Pt(10)

    doc.add_paragraph("")
    doc.add_paragraph("")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("This proposal is valid for 30 days from the date of issue.")
    run.font.italic = True
    run.font.color.rgb = DARK_GRAY

    doc.save(path)
    print(f"✅ Created: {path}")


# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    word_dir = os.path.join(base, "word")
    os.makedirs(word_dir, exist_ok=True)

    create_website_proposal(os.path.join(word_dir, "Website-Client-Proposal.docx"))
    create_application_proposal(os.path.join(word_dir, "Application-Client-Proposal.docx"))

    print("\n🎉 All Word documents generated successfully!")
