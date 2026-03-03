#!/usr/bin/env python3
"""
Generate Excel Pricing Calculator sheets for Website and Application projects.
Run: python3 scripts/generate_excel.py
"""

import os
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter

# ─── Style Constants ───────────────────────────────────────────────

DARK_BLUE = "1B2A4A"
MED_BLUE = "2E75B6"
LIGHT_BLUE = "D6E4F0"
ACCENT_GREEN = "548235"
ACCENT_ORANGE = "ED7D31"
WHITE = "FFFFFF"
LIGHT_GRAY = "F2F2F2"
BORDER_COLOR = "B4C6E7"

thin_border = Border(
    left=Side(style="thin", color=BORDER_COLOR),
    right=Side(style="thin", color=BORDER_COLOR),
    top=Side(style="thin", color=BORDER_COLOR),
    bottom=Side(style="thin", color=BORDER_COLOR),
)

header_font = Font(name="Calibri", bold=True, color=WHITE, size=11)
header_fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")
subheader_font = Font(name="Calibri", bold=True, color=WHITE, size=10)
subheader_fill = PatternFill(start_color=MED_BLUE, end_color=MED_BLUE, fill_type="solid")
section_font = Font(name="Calibri", bold=True, color=DARK_BLUE, size=11)
section_fill = PatternFill(start_color=LIGHT_BLUE, end_color=LIGHT_BLUE, fill_type="solid")
normal_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", bold=True, size=10)
currency_format = '#,##0'
green_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
orange_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
alt_fill = PatternFill(start_color=LIGHT_GRAY, end_color=LIGHT_GRAY, fill_type="solid")
center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)


def style_header_row(ws, row, cols, font=header_font, fill=header_fill):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = font
        cell.fill = fill
        cell.alignment = center_align
        cell.border = thin_border


def style_row(ws, row, cols, font=normal_font, fill=None, align=None):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = font
        if fill:
            cell.fill = fill
        if align:
            cell.alignment = align
        else:
            cell.alignment = left_align
        cell.border = thin_border


def add_section_header(ws, row, text, cols):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=cols)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = section_font
    cell.fill = section_fill
    cell.alignment = left_align
    for c in range(1, cols + 1):
        ws.cell(row=row, column=c).border = thin_border
        ws.cell(row=row, column=c).fill = section_fill
    return row + 1


def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ════════════════════════════════════════════════════════════════════
# WEBSITE PRICING CALCULATOR
# ════════════════════════════════════════════════════════════════════

def create_website_excel(path):
    wb = Workbook()

    # ── Sheet 1: Pricing Calculator ─────────────────────────────────
    ws = wb.active
    ws.title = "Pricing Calculator"
    ws.sheet_properties.tabColor = "1B2A4A"
    set_col_widths(ws, [5, 35, 18, 15, 15, 18, 15, 20])

    COLS = 8
    headers = ["#", "Item / Parameter", "Category", "Unit Cost (₹)",
               "Quantity", "Total (₹)", "Required?", "Notes"]

    # Title
    ws.merge_cells("A1:H1")
    title_cell = ws.cell(row=1, column=1, value="WEBSITE PROJECT — PRICING CALCULATOR")
    title_cell.font = Font(name="Calibri", bold=True, color=WHITE, size=14)
    title_cell.fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")
    title_cell.alignment = center_align
    for c in range(1, COLS + 1):
        ws.cell(row=1, column=c).fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")

    # Client info
    ws.merge_cells("A2:H2")
    ws.cell(row=2, column=1, value="Client Name:").font = bold_font
    ws.merge_cells("A3:H3")
    ws.cell(row=3, column=1, value="Project Name:").font = bold_font
    ws.merge_cells("A4:H4")
    ws.cell(row=4, column=1, value="Date:").font = bold_font

    row = 6
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header_row(ws, row, COLS)
    row += 1

    # Data items
    items = [
        # Domain & SSL
        ("DOMAIN & SSL", None),
        (1, "Domain Registration (.com)", "Domain", 800, 1),
        (2, "Domain Privacy Protection", "Domain", 500, 1),
        (3, "SSL Certificate (Basic/Free)", "SSL", 0, 1),
        (4, "SSL Certificate (Wildcard/Premium)", "SSL", 5000, 1),
        # Hosting
        ("HOSTING", None),
        (5, "Shared Hosting (Annual)", "Hosting", 3000, 1),
        (6, "VPS Hosting (Annual)", "Hosting", 12000, 1),
        (7, "Cloud Hosting (Annual — AWS/GCP)", "Hosting", 24000, 1),
        (8, "Dedicated Server (Annual)", "Hosting", 60000, 1),
        (9, "Email Hosting (Annual)", "Hosting", 3600, 1),
        # Database
        ("DATABASE", None),
        (10, "MySQL / PostgreSQL Setup", "Database", 3000, 1),
        (11, "MongoDB Setup", "Database", 5000, 1),
        (12, "Firebase Setup", "Database", 3000, 1),
        (13, "Database Migration", "Database", 8000, 1),
        # Design
        ("DESIGN & UI/UX", None),
        (14, "Wireframes (per page)", "Design", 2000, 1),
        (15, "High-Fidelity Mockup (per page)", "Design", 4000, 1),
        (16, "Logo Design", "Design", 5000, 1),
        (17, "Brand Kit (Logo + Colors + Typography)", "Design", 15000, 1),
        (18, "Custom Illustrations (per set)", "Design", 8000, 1),
        (19, "Design Revisions (per round)", "Design", 2000, 1),
        # Pages
        ("PAGE DEVELOPMENT", None),
        (20, "Home Page", "Pages", 8000, 1),
        (21, "About Page", "Pages", 4000, 1),
        (22, "Services Page", "Pages", 5000, 1),
        (23, "Contact Page (with form)", "Pages", 4000, 1),
        (24, "Blog Listing Page", "Pages", 6000, 1),
        (25, "Blog Detail Page", "Pages", 5000, 1),
        (26, "Portfolio / Gallery Page", "Pages", 6000, 1),
        (27, "Team / About Team Page", "Pages", 4000, 1),
        (28, "FAQ Page", "Pages", 3000, 1),
        (29, "Testimonials Page", "Pages", 3000, 1),
        (30, "Terms & Privacy Pages", "Pages", 2000, 2),
        (31, "Custom Landing Page", "Pages", 8000, 1),
        (32, "Login / Register Pages", "Pages", 8000, 1),
        (33, "User Dashboard", "Pages", 12000, 1),
        (34, "Admin Panel", "Pages", 25000, 1),
        (35, "Search Results Page", "Pages", 5000, 1),
        (36, "404 Error Page", "Pages", 1500, 1),
        # Features
        ("FEATURES & FUNCTIONALITY", None),
        (37, "Responsive Design (Mobile + Tablet)", "Feature", 10000, 1),
        (38, "Contact Form with Email", "Feature", 3000, 1),
        (39, "Multi-step Form / Wizard", "Feature", 8000, 1),
        (40, "Newsletter Subscription", "Feature", 3000, 1),
        (41, "Live Chat Integration", "Feature", 5000, 1),
        (42, "Chatbot Integration (AI)", "Feature", 15000, 1),
        (43, "User Authentication (Email/Pass)", "Feature", 8000, 1),
        (44, "Social Login (Google/Facebook)", "Feature", 5000, 1),
        (45, "Booking / Appointment System", "Feature", 15000, 1),
        (46, "Event Calendar", "Feature", 8000, 1),
        (47, "Google Maps Integration", "Feature", 3000, 1),
        (48, "Image Gallery / Lightbox", "Feature", 3000, 1),
        (49, "Video Integration", "Feature", 2000, 1),
        (50, "File Upload System", "Feature", 5000, 1),
        (51, "Multi-language Support", "Feature", 15000, 1),
        (52, "Dark Mode Toggle", "Feature", 3000, 1),
        (53, "Push Notifications (Web)", "Feature", 5000, 1),
        (54, "Advanced Search with Filters", "Feature", 8000, 1),
        (55, "Comments / Reviews System", "Feature", 6000, 1),
        (56, "Ratings System", "Feature", 4000, 1),
        (57, "Social Sharing Buttons", "Feature", 1500, 1),
        (58, "PDF Generation", "Feature", 5000, 1),
        (59, "Email Template System", "Feature", 5000, 1),
        (60, "CRM Integration", "Feature", 10000, 1),
        # E-Commerce
        ("E-COMMERCE (if applicable)", None),
        (61, "Product Listing Page", "E-Commerce", 8000, 1),
        (62, "Product Detail Page", "E-Commerce", 8000, 1),
        (63, "Shopping Cart", "E-Commerce", 10000, 1),
        (64, "Checkout Flow", "E-Commerce", 12000, 1),
        (65, "Order Management System", "E-Commerce", 15000, 1),
        (66, "Inventory Management", "E-Commerce", 12000, 1),
        (67, "Coupon / Discount System", "E-Commerce", 6000, 1),
        (68, "Wishlist Feature", "E-Commerce", 4000, 1),
        (69, "Product Reviews", "E-Commerce", 5000, 1),
        (70, "Shipping Calculator", "E-Commerce", 5000, 1),
        (71, "Tax Calculation", "E-Commerce", 4000, 1),
        (72, "Invoice Generation", "E-Commerce", 5000, 1),
        (73, "Return / Refund System", "E-Commerce", 8000, 1),
        (74, "Vendor / Multi-seller System", "E-Commerce", 40000, 1),
        # Payment
        ("PAYMENT INTEGRATION", None),
        (75, "Razorpay Integration", "Payment", 5000, 1),
        (76, "Stripe Integration", "Payment", 6000, 1),
        (77, "PayPal Integration", "Payment", 5000, 1),
        (78, "UPI Integration", "Payment", 3000, 1),
        (79, "Subscription / Recurring Payments", "Payment", 10000, 1),
        # SEO & Analytics
        ("SEO & ANALYTICS", None),
        (80, "Basic On-Page SEO", "SEO", 5000, 1),
        (81, "Advanced SEO Setup", "SEO", 15000, 1),
        (82, "Google Analytics 4 Setup", "SEO", 2000, 1),
        (83, "Google Search Console Setup", "SEO", 1000, 1),
        (84, "Schema Markup", "SEO", 3000, 1),
        (85, "Sitemap & Robots.txt", "SEO", 1000, 1),
        (86, "Google Tag Manager Setup", "SEO", 2000, 1),
        (87, "Facebook Pixel Setup", "SEO", 1500, 1),
        # Security
        ("SECURITY", None),
        (88, "Security Headers Setup", "Security", 2000, 1),
        (89, "Firewall Setup (WAF)", "Security", 5000, 1),
        (90, "DDoS Protection", "Security", 5000, 1),
        (91, "CAPTCHA Integration", "Security", 2000, 1),
        (92, "Two-Factor Auth (2FA)", "Security", 5000, 1),
        (93, "GDPR Compliance Setup", "Security", 8000, 1),
        (94, "Security Audit", "Security", 10000, 1),
        # CMS
        ("CMS SETUP", None),
        (95, "WordPress Setup & Customization", "CMS", 15000, 1),
        (96, "Custom CMS / Admin Panel", "CMS", 30000, 1),
        (97, "Headless CMS (Strapi/Sanity)", "CMS", 20000, 1),
        # Content
        ("CONTENT SERVICES", None),
        (98, "Content Writing (per page)", "Content", 2000, 1),
        (99, "Copywriting (per page)", "Content", 3000, 1),
        (100, "Stock Images (per set of 10)", "Content", 2000, 1),
        # Performance
        ("PERFORMANCE OPTIMIZATION", None),
        (101, "Page Speed Optimization", "Performance", 5000, 1),
        (102, "CDN Setup", "Performance", 3000, 1),
        (103, "Image Optimization Pipeline", "Performance", 3000, 1),
        (104, "Caching Strategy", "Performance", 3000, 1),
        # Third-Party Integrations
        ("THIRD-PARTY INTEGRATIONS", None),
        (105, "Email Service (SendGrid/SES)", "Integration", 5000, 1),
        (106, "SMS Gateway Integration", "Integration", 5000, 1),
        (107, "Social Media API Integration", "Integration", 5000, 1),
        (108, "Google Calendar Integration", "Integration", 5000, 1),
        (109, "Zapier / Automation Integration", "Integration", 5000, 1),
        (110, "ERP / Accounting Integration", "Integration", 15000, 1),
        # Testing & QA
        ("TESTING & QA", None),
        (111, "Cross-Browser Testing", "Testing", 5000, 1),
        (112, "Mobile Responsiveness Testing", "Testing", 3000, 1),
        (113, "Load / Stress Testing", "Testing", 5000, 1),
        (114, "Security Testing", "Testing", 5000, 1),
        (115, "User Acceptance Testing", "Testing", 5000, 1),
    ]

    item_num = 0
    for item in items:
        if item[1] is None:
            # Section header
            row = add_section_header(ws, row, item[0], COLS)
            continue

        num, name, category, unit_cost, qty = item
        ws.cell(row=row, column=1, value=num)
        ws.cell(row=row, column=2, value=name)
        ws.cell(row=row, column=3, value=category)
        ws.cell(row=row, column=4, value=unit_cost)
        ws.cell(row=row, column=4).number_format = currency_format
        ws.cell(row=row, column=5, value=qty)
        # Total formula = Unit Cost × Quantity
        ws.cell(row=row, column=6).value = f"=D{row}*E{row}"
        ws.cell(row=row, column=6).number_format = currency_format
        ws.cell(row=row, column=7, value="Yes")

        fill = alt_fill if item_num % 2 == 0 else None
        style_row(ws, row, COLS, fill=fill)
        ws.cell(row=row, column=1).alignment = center_align
        ws.cell(row=row, column=5).alignment = center_align
        ws.cell(row=row, column=7).alignment = center_align
        item_num += 1
        row += 1

    # Grand Total
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    ws.cell(row=row, column=1, value="SUBTOTAL (All Items)")
    ws.cell(row=row, column=1).font = Font(name="Calibri", bold=True, size=12, color=DARK_BLUE)
    ws.cell(row=row, column=6).value = f"=SUMPRODUCT((G7:G{row-2}=\"Yes\")*F7:F{row-2})"
    ws.cell(row=row, column=6).font = Font(name="Calibri", bold=True, size=12, color=DARK_BLUE)
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border
        ws.cell(row=row, column=c).fill = green_fill

    row += 1
    ws.cell(row=row, column=2, value="Complexity Multiplier")
    ws.cell(row=row, column=5, value=1.0)
    ws.cell(row=row, column=5).alignment = center_align
    ws.cell(row=row, column=6).value = f"=F{row-1}*E{row}"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.cell(row=row, column=2, value="Discount (%)")
    ws.cell(row=row, column=5, value=0)
    ws.cell(row=row, column=5).alignment = center_align
    ws.cell(row=row, column=6).value = f"=F{row-1}*(1-E{row}/100)"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.cell(row=row, column=2, value="GST (18%)")
    ws.cell(row=row, column=6).value = f"=F{row-1}*0.18"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    total_label = ws.cell(row=row, column=1, value="GRAND TOTAL (incl. GST)")
    total_label.font = Font(name="Calibri", bold=True, size=14, color=WHITE)
    ws.cell(row=row, column=6).value = f"=F{row-2}+F{row-1}"
    ws.cell(row=row, column=6).font = Font(name="Calibri", bold=True, size=14, color=WHITE)
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).fill = PatternFill(start_color=ACCENT_GREEN, end_color=ACCENT_GREEN, fill_type="solid")
        ws.cell(row=row, column=c).border = thin_border

    # Payment schedule
    row += 2
    row = add_section_header(ws, row, "PAYMENT SCHEDULE", COLS)
    schedule = [
        ("Advance (Before Starting)", "30-50%", f"=F{row-3}*0.4"),
        ("After Design Approval", "20-30%", f"=F{row-3}*0.25"),
        ("After Development Completion", "20-30%", f"=F{row-3}*0.25"),
        ("After Launch & Handover", "10-20%", f"=F{row-3}*0.1"),
    ]
    for milestone, pct, formula in schedule:
        ws.cell(row=row, column=2, value=milestone)
        ws.cell(row=row, column=5, value=pct)
        ws.cell(row=row, column=5).alignment = center_align
        ws.cell(row=row, column=6).value = formula
        ws.cell(row=row, column=6).number_format = currency_format
        style_row(ws, row, COLS)
        row += 1

    # ── Sheet 2: Maintenance Plans ──────────────────────────────────
    ws2 = wb.create_sheet("Maintenance Plans")
    ws2.sheet_properties.tabColor = "2E75B6"
    set_col_widths(ws2, [5, 35, 15, 15, 15, 15, 15])
    COLS2 = 7

    ws2.merge_cells("A1:G1")
    ws2.cell(row=1, column=1, value="WEBSITE MAINTENANCE PLANS").font = Font(name="Calibri", bold=True, color=WHITE, size=14)
    ws2.cell(row=1, column=1).fill = header_fill
    ws2.cell(row=1, column=1).alignment = center_align
    for c in range(1, COLS2 + 1):
        ws2.cell(row=1, column=c).fill = header_fill

    maint_headers = ["#", "Service", "Basic\n₹3K/mo", "Standard\n₹8K/mo", "Professional\n₹15K/mo", "Enterprise\n₹30K/mo", "Premium\n₹50K/mo"]
    for c, h in enumerate(maint_headers, 1):
        ws2.cell(row=3, column=c, value=h)
    style_header_row(ws2, 3, COLS2, subheader_font, subheader_fill)

    maintenance_items = [
        (1, "Uptime Monitoring", "✓", "✓", "✓", "✓", "✓"),
        (2, "Monthly Backups", "✓", "✓", "✓", "✓", "✓"),
        (3, "Weekly Backups", "✗", "✓", "✓", "✓", "✓"),
        (4, "Daily Backups", "✗", "✗", "✓", "✓", "✓"),
        (5, "Security Updates", "Quarterly", "Monthly", "Weekly", "Weekly", "Daily"),
        (6, "Plugin / Library Updates", "✗", "Monthly", "Bi-weekly", "Weekly", "As needed"),
        (7, "Content Updates (per month)", "2", "5", "10", "Unlimited", "Unlimited"),
        (8, "Bug Fixes", "Critical", "All", "All+Priority", "All+Priority", "All+Priority"),
        (9, "Performance Monitoring", "✗", "Basic", "Advanced", "Advanced", "Real-time"),
        (10, "SSL Renewal Management", "✓", "✓", "✓", "✓", "✓"),
        (11, "SEO Monitoring", "✗", "Basic", "Full", "Full", "Full+Reports"),
        (12, "Analytics Reports", "✗", "Monthly", "Bi-weekly", "Weekly", "Daily"),
        (13, "Support Response Time", "48hrs", "24hrs", "12hrs", "6hrs", "2hrs"),
        (14, "Support Channels", "Email", "Email+Chat", "Email+Chat+Call", "All+Dedicated", "All+Dedicated"),
        (15, "Feature Enhancements", "✗", "1 small/mo", "2 small/mo", "4/mo", "Unlimited"),
        (16, "Server Management", "✗", "Basic", "Full", "Full", "Full+Scaling"),
        (17, "Disaster Recovery", "✗", "✗", "Basic", "Full", "Full+Testing"),
        (18, "Priority Support", "✗", "✗", "✓", "✓", "✓"),
    ]

    for r, item in enumerate(maintenance_items, 4):
        for c, val in enumerate(item, 1):
            ws2.cell(row=r, column=c, value=val)
        fill = alt_fill if r % 2 == 0 else None
        style_row(ws2, r, COLS2, fill=fill)
        ws2.cell(row=r, column=1).alignment = center_align
        for c in range(3, COLS2 + 1):
            ws2.cell(row=r, column=c).alignment = center_align

    # ── Sheet 3: Hourly Rates ──────────────────────────────────────
    ws3 = wb.create_sheet("Hourly Rates")
    ws3.sheet_properties.tabColor = "548235"
    set_col_widths(ws3, [5, 30, 18, 18, 18])
    COLS3 = 5

    ws3.merge_cells("A1:E1")
    ws3.cell(row=1, column=1, value="DEVELOPER HOURLY RATES REFERENCE").font = Font(name="Calibri", bold=True, color=WHITE, size=14)
    ws3.cell(row=1, column=1).fill = PatternFill(start_color=ACCENT_GREEN, end_color=ACCENT_GREEN, fill_type="solid")
    ws3.cell(row=1, column=1).alignment = center_align
    for c in range(1, COLS3 + 1):
        ws3.cell(row=1, column=c).fill = PatternFill(start_color=ACCENT_GREEN, end_color=ACCENT_GREEN, fill_type="solid")

    rate_headers = ["#", "Developer Level", "Rate (₹/hr)", "Rate ($/hr)", "Monthly (160 hrs)"]
    for c, h in enumerate(rate_headers, 1):
        ws3.cell(row=3, column=c, value=h)
    style_header_row(ws3, 3, COLS3, subheader_font, subheader_fill)

    rates = [
        (1, "Junior Developer (0-2 yrs)", 500, 8, "=C4*160"),
        (2, "Mid-Level Developer (2-5 yrs)", 1000, 15, "=C5*160"),
        (3, "Senior Developer (5-8 yrs)", 1800, 25, "=C6*160"),
        (4, "Lead Developer (8+ yrs)", 2500, 35, "=C7*160"),
        (5, "UI/UX Designer (Mid)", 1200, 18, "=C8*160"),
        (6, "UI/UX Designer (Senior)", 2000, 30, "=C9*160"),
        (7, "Full-Stack Developer (Mid)", 1200, 18, "=C10*160"),
        (8, "Full-Stack Developer (Senior)", 2200, 30, "=C11*160"),
        (9, "DevOps Engineer", 2000, 28, "=C12*160"),
        (10, "QA / Tester", 800, 12, "=C13*160"),
        (11, "Project Manager", 1500, 22, "=C14*160"),
        (12, "Technical Architect", 3000, 45, "=C15*160"),
    ]

    for r, (num, role, inr, usd, formula) in enumerate(rates, 4):
        ws3.cell(row=r, column=1, value=num)
        ws3.cell(row=r, column=2, value=role)
        ws3.cell(row=r, column=3, value=inr)
        ws3.cell(row=r, column=3).number_format = currency_format
        ws3.cell(row=r, column=4, value=usd)
        ws3.cell(row=r, column=4).number_format = '$#,##0'
        ws3.cell(row=r, column=5).value = formula
        ws3.cell(row=r, column=5).number_format = currency_format
        fill = alt_fill if r % 2 == 0 else None
        style_row(ws3, r, COLS3, fill=fill)
        ws3.cell(row=r, column=1).alignment = center_align

    # Freeze panes on sheet 1
    ws.freeze_panes = "A7"

    wb.save(path)
    print(f"✅ Created: {path}")


# ════════════════════════════════════════════════════════════════════
# APPLICATION PRICING CALCULATOR
# ════════════════════════════════════════════════════════════════════

def create_application_excel(path):
    wb = Workbook()

    ws = wb.active
    ws.title = "Pricing Calculator"
    ws.sheet_properties.tabColor = "1B2A4A"
    set_col_widths(ws, [5, 35, 18, 15, 15, 18, 15, 20])

    COLS = 8
    headers = ["#", "Item / Parameter", "Category", "Unit Cost (₹)",
               "Quantity", "Total (₹)", "Required?", "Notes"]

    # Title
    ws.merge_cells("A1:H1")
    title_cell = ws.cell(row=1, column=1, value="MOBILE APPLICATION — PRICING CALCULATOR")
    title_cell.font = Font(name="Calibri", bold=True, color=WHITE, size=14)
    title_cell.fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")
    title_cell.alignment = center_align
    for c in range(1, COLS + 1):
        ws.cell(row=1, column=c).fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")

    ws.merge_cells("A2:H2")
    ws.cell(row=2, column=1, value="Client Name:").font = bold_font
    ws.merge_cells("A3:H3")
    ws.cell(row=3, column=1, value="Project Name:").font = bold_font
    ws.merge_cells("A4:H4")
    ws.cell(row=4, column=1, value="Platform: Android / iOS / Both").font = bold_font

    row = 6
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header_row(ws, row, COLS)
    row += 1

    items = [
        # App Store & Deployment
        ("APP STORE & DEPLOYMENT", None),
        (1, "Google Play Developer Account ($25)", "Store", 2100, 1),
        (2, "Apple Developer Account ($99/yr)", "Store", 8300, 1),
        (3, "App Store Listing & ASO (per store)", "Store", 5000, 1),
        (4, "App Store Screenshots Design (per store)", "Store", 3000, 1),
        (5, "CI/CD Pipeline Setup", "DevOps", 10000, 1),
        # Design
        ("DESIGN & UI/UX", None),
        (6, "User Flow & Wireframes", "Design", 10000, 1),
        (7, "High-Fidelity Mockups (per screen)", "Design", 3000, 1),
        (8, "Interactive Prototype", "Design", 8000, 1),
        (9, "App Icon Design (all sizes)", "Design", 3000, 1),
        (10, "Splash Screen Design", "Design", 2000, 1),
        (11, "Onboarding Screen Design (3-5 screens)", "Design", 5000, 1),
        (12, "Custom Illustrations / Lottie Animations", "Design", 8000, 1),
        (13, "Dark Mode Design", "Design", 5000, 1),
        (14, "Tablet Layout Design", "Design", 8000, 1),
        (15, "Design System Documentation", "Design", 5000, 1),
        # Auth
        ("AUTHENTICATION", None),
        (16, "Email/Password Login", "Auth", 8000, 1),
        (17, "Phone/OTP Login", "Auth", 8000, 1),
        (18, "Google Sign-In", "Auth", 4000, 1),
        (19, "Apple Sign-In", "Auth", 5000, 1),
        (20, "Facebook Login", "Auth", 4000, 1),
        (21, "Biometric Auth (Fingerprint/Face)", "Auth", 5000, 1),
        (22, "Two-Factor Authentication", "Auth", 8000, 1),
        (23, "Session Management & Token Refresh", "Auth", 5000, 1),
        (24, "Account Deletion Feature", "Auth", 3000, 1),
        (25, "Role-Based Access Control", "Auth", 8000, 1),
        # Core Screens
        ("CORE SCREEN DEVELOPMENT", None),
        (26, "Splash Screen", "Screens", 3000, 1),
        (27, "Onboarding Flow (3-5 screens)", "Screens", 8000, 1),
        (28, "Home / Main Screen", "Screens", 10000, 1),
        (29, "Profile Screen", "Screens", 6000, 1),
        (30, "Settings Screen", "Screens", 5000, 1),
        (31, "Search Screen with Filters", "Screens", 10000, 1),
        (32, "Detail Screen", "Screens", 6000, 1),
        (33, "List / Feed Screen (with pagination)", "Screens", 8000, 1),
        (34, "Form / Input Screen", "Screens", 5000, 1),
        (35, "Notification Center", "Screens", 6000, 1),
        (36, "Help / FAQ / Support Screen", "Screens", 4000, 1),
        (37, "About / Legal Screens", "Screens", 2000, 1),
        # Features
        ("FEATURES & FUNCTIONALITY", None),
        (38, "Push Notifications (FCM/APNs)", "Feature", 8000, 1),
        (39, "In-App Messaging / Chat", "Feature", 25000, 1),
        (40, "Real-time Chat (WebSocket)", "Feature", 35000, 1),
        (41, "Voice / Video Calling", "Feature", 50000, 1),
        (42, "GPS / Location Services", "Feature", 8000, 1),
        (43, "Google Maps Integration", "Feature", 8000, 1),
        (44, "Route / Navigation", "Feature", 12000, 1),
        (45, "Geofencing", "Feature", 10000, 1),
        (46, "Camera Integration", "Feature", 5000, 1),
        (47, "Gallery / Image Picker", "Feature", 3000, 1),
        (48, "Image Cropping / Editing", "Feature", 5000, 1),
        (49, "Video Recording / Player", "Feature", 8000, 1),
        (50, "QR / Barcode Scanner", "Feature", 5000, 1),
        (51, "Document Scanner (OCR)", "Feature", 12000, 1),
        (52, "File Upload / Download", "Feature", 5000, 1),
        (53, "Offline Mode & Data Sync", "Feature", 15000, 1),
        (54, "Background Services / Tasks", "Feature", 8000, 1),
        (55, "Local Notifications / Reminders", "Feature", 5000, 1),
        (56, "Social Sharing", "Feature", 3000, 1),
        (57, "Deep Linking / Universal Links", "Feature", 5000, 1),
        (58, "Multi-language (i18n)", "Feature", 10000, 1),
        (59, "Dark Mode Toggle", "Feature", 3000, 1),
        (60, "Accessibility Support", "Feature", 8000, 1),
        # Advanced Features
        ("ADVANCED FEATURES", None),
        (61, "AR / Augmented Reality", "Advanced", 60000, 1),
        (62, "ML / AI Feature", "Advanced", 50000, 1),
        (63, "Face Detection / Recognition", "Advanced", 30000, 1),
        (64, "Object Detection", "Advanced", 40000, 1),
        (65, "Bluetooth / BLE Integration", "Advanced", 20000, 1),
        (66, "NFC Integration", "Advanced", 15000, 1),
        (67, "IoT Device Integration", "Advanced", 30000, 1),
        (68, "Wearable (Watch) Companion App", "Advanced", 40000, 1),
        (69, "Health Kit / Google Fit Integration", "Advanced", 15000, 1),
        # Backend
        ("BACKEND & API", None),
        (70, "Custom Backend Setup (Node/Python/Go)", "Backend", 15000, 1),
        (71, "Firebase Setup & Configuration", "Backend", 8000, 1),
        (72, "Supabase Setup & Configuration", "Backend", 8000, 1),
        (73, "REST API Development (per module)", "Backend", 10000, 1),
        (74, "GraphQL API Development", "Backend", 15000, 1),
        (75, "Real-time Database Setup", "Backend", 8000, 1),
        (76, "Cloud Storage Setup (S3/GCS)", "Backend", 5000, 1),
        (77, "Cloud Functions / Serverless", "Backend", 8000, 1),
        (78, "Admin Panel / Dashboard", "Backend", 30000, 1),
        (79, "API Documentation (Swagger)", "Backend", 5000, 1),
        # E-Commerce
        ("E-COMMERCE (if applicable)", None),
        (80, "Product Listing Screen", "E-Commerce", 10000, 1),
        (81, "Product Detail Screen", "E-Commerce", 8000, 1),
        (82, "Shopping Cart", "E-Commerce", 10000, 1),
        (83, "Checkout Flow", "E-Commerce", 12000, 1),
        (84, "Order Tracking", "E-Commerce", 10000, 1),
        (85, "Order History", "E-Commerce", 6000, 1),
        (86, "Wishlist / Favorites", "E-Commerce", 5000, 1),
        (87, "Product Reviews & Ratings", "E-Commerce", 6000, 1),
        (88, "Coupons / Discounts", "E-Commerce", 5000, 1),
        (89, "Inventory Management", "E-Commerce", 12000, 1),
        # Payment
        ("PAYMENT INTEGRATION", None),
        (90, "Razorpay Integration", "Payment", 8000, 1),
        (91, "Stripe Integration", "Payment", 8000, 1),
        (92, "PayPal Integration", "Payment", 6000, 1),
        (93, "Google Pay / Apple Pay", "Payment", 8000, 1),
        (94, "In-App Purchases (IAP)", "Payment", 12000, 1),
        (95, "Subscription System", "Payment", 15000, 1),
        (96, "Wallet System", "Payment", 12000, 1),
        # Security
        ("SECURITY", None),
        (97, "Data Encryption (at rest + in transit)", "Security", 5000, 1),
        (98, "Certificate Pinning", "Security", 5000, 1),
        (99, "Secure Local Storage", "Security", 3000, 1),
        (100, "Jailbreak / Root Detection", "Security", 5000, 1),
        (101, "Code Obfuscation", "Security", 3000, 1),
        (102, "HIPAA Compliance", "Security", 40000, 1),
        (103, "PCI-DSS Compliance", "Security", 30000, 1),
        # Testing
        ("TESTING & QA", None),
        (104, "Unit Testing Setup + Tests", "Testing", 10000, 1),
        (105, "Integration Testing", "Testing", 8000, 1),
        (106, "UI / Widget Testing", "Testing", 8000, 1),
        (107, "Beta Testing (TestFlight/Play Console)", "Testing", 5000, 1),
        (108, "Device Compatibility Testing", "Testing", 5000, 1),
        (109, "Performance Testing", "Testing", 5000, 1),
        (110, "Security Testing / Pen Test", "Testing", 10000, 1),
        # Analytics
        ("ANALYTICS & MONITORING", None),
        (111, "Firebase Analytics Setup", "Analytics", 3000, 1),
        (112, "Crashlytics / Sentry Setup", "Analytics", 3000, 1),
        (113, "Mixpanel / Amplitude Integration", "Analytics", 5000, 1),
        (114, "Custom Analytics Dashboard", "Analytics", 10000, 1),
        # Third-Party Integrations
        ("THIRD-PARTY INTEGRATIONS", None),
        (115, "Email Service (SendGrid/SES)", "Integration", 5000, 1),
        (116, "SMS / OTP Service (Twilio/MSG91)", "Integration", 5000, 1),
        (117, "Social Media API Integration", "Integration", 5000, 1),
        (118, "Calendar Integration", "Integration", 5000, 1),
        (119, "Cloud Messaging (FCM/OneSignal)", "Integration", 5000, 1),
        (120, "ERP / CRM Integration", "Integration", 15000, 1),
    ]

    item_num = 0
    for item in items:
        if item[1] is None:
            row = add_section_header(ws, row, item[0], COLS)
            continue

        num, name, category, unit_cost, qty = item
        ws.cell(row=row, column=1, value=num)
        ws.cell(row=row, column=2, value=name)
        ws.cell(row=row, column=3, value=category)
        ws.cell(row=row, column=4, value=unit_cost)
        ws.cell(row=row, column=4).number_format = currency_format
        ws.cell(row=row, column=5, value=qty)
        ws.cell(row=row, column=6).value = f"=D{row}*E{row}"
        ws.cell(row=row, column=6).number_format = currency_format
        ws.cell(row=row, column=7, value="Yes")

        fill = alt_fill if item_num % 2 == 0 else None
        style_row(ws, row, COLS, fill=fill)
        ws.cell(row=row, column=1).alignment = center_align
        ws.cell(row=row, column=5).alignment = center_align
        ws.cell(row=row, column=7).alignment = center_align
        item_num += 1
        row += 1

    # Platform multiplier
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    ws.cell(row=row, column=1, value="SUBTOTAL (All Items)")
    ws.cell(row=row, column=1).font = Font(name="Calibri", bold=True, size=12, color=DARK_BLUE)
    ws.cell(row=row, column=6).value = f"=SUMPRODUCT((G7:G{row-2}=\"Yes\")*F7:F{row-2})"
    ws.cell(row=row, column=6).font = Font(name="Calibri", bold=True, size=12, color=DARK_BLUE)
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border
        ws.cell(row=row, column=c).fill = green_fill

    row += 1
    ws.cell(row=row, column=2, value="Platform Multiplier (1.0=One, 1.3-1.5=Both Cross-Platform, 1.8-2.0=Both Native)")
    ws.cell(row=row, column=5, value=1.0)
    ws.cell(row=row, column=5).alignment = center_align
    ws.cell(row=row, column=6).value = f"=F{row-1}*E{row}"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.cell(row=row, column=2, value="Complexity Multiplier (1.0=Simple, 1.5=Medium, 2.0=Complex, 3.0=Enterprise)")
    ws.cell(row=row, column=5, value=1.0)
    ws.cell(row=row, column=5).alignment = center_align
    ws.cell(row=row, column=6).value = f"=F{row-1}*E{row}"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.cell(row=row, column=2, value="Discount (%)")
    ws.cell(row=row, column=5, value=0)
    ws.cell(row=row, column=5).alignment = center_align
    ws.cell(row=row, column=6).value = f"=F{row-1}*(1-E{row}/100)"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.cell(row=row, column=2, value="GST (18%)")
    ws.cell(row=row, column=6).value = f"=F{row-1}*0.18"
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).border = thin_border

    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    ws.cell(row=row, column=1, value="GRAND TOTAL (incl. GST)")
    ws.cell(row=row, column=1).font = Font(name="Calibri", bold=True, size=14, color=WHITE)
    ws.cell(row=row, column=6).value = f"=F{row-2}+F{row-1}"
    ws.cell(row=row, column=6).font = Font(name="Calibri", bold=True, size=14, color=WHITE)
    ws.cell(row=row, column=6).number_format = currency_format
    for c in range(1, COLS + 1):
        ws.cell(row=row, column=c).fill = PatternFill(start_color=ACCENT_GREEN, end_color=ACCENT_GREEN, fill_type="solid")
        ws.cell(row=row, column=c).border = thin_border

    # Payment schedule
    row += 2
    row = add_section_header(ws, row, "PAYMENT SCHEDULE", COLS)
    schedule = [
        ("Advance (Before Starting)", "30-40%", f"=F{row-3}*0.35"),
        ("After Design Approval", "20-25%", f"=F{row-3}*0.20"),
        ("After Development Completion", "25-30%", f"=F{row-3}*0.25"),
        ("After Testing & Store Submission", "10-15%", f"=F{row-3}*0.10"),
        ("After Launch & Handover", "5-10%", f"=F{row-3}*0.10"),
    ]
    for milestone, pct, formula in schedule:
        ws.cell(row=row, column=2, value=milestone)
        ws.cell(row=row, column=5, value=pct)
        ws.cell(row=row, column=5).alignment = center_align
        ws.cell(row=row, column=6).value = formula
        ws.cell(row=row, column=6).number_format = currency_format
        style_row(ws, row, COLS)
        row += 1

    # ── Sheet 2: App Maintenance Plans ──────────────────────────────
    ws2 = wb.create_sheet("Maintenance Plans")
    ws2.sheet_properties.tabColor = "2E75B6"
    set_col_widths(ws2, [5, 35, 15, 15, 15, 15, 15])
    COLS2 = 7

    ws2.merge_cells("A1:G1")
    ws2.cell(row=1, column=1, value="MOBILE APP MAINTENANCE PLANS").font = Font(name="Calibri", bold=True, color=WHITE, size=14)
    ws2.cell(row=1, column=1).fill = header_fill
    ws2.cell(row=1, column=1).alignment = center_align
    for c in range(1, COLS2 + 1):
        ws2.cell(row=1, column=c).fill = header_fill

    maint_headers = ["#", "Service", "Basic\n₹5K/mo", "Standard\n₹12K/mo", "Professional\n₹25K/mo", "Enterprise\n₹40K/mo", "Premium\n₹60K/mo"]
    for c, h in enumerate(maint_headers, 1):
        ws2.cell(row=3, column=c, value=h)
    style_header_row(ws2, 3, COLS2, subheader_font, subheader_fill)

    maintenance_items = [
        (1, "Crash Monitoring", "✓", "✓", "✓", "✓", "✓"),
        (2, "Bug Fixes", "Critical", "All", "All+Priority", "All+Priority", "All+Priority"),
        (3, "OS Compatibility Updates", "Yearly", "6 months", "Quarterly", "Monthly", "As Released"),
        (4, "Library/SDK Updates", "✗", "Quarterly", "Monthly", "Bi-weekly", "As needed"),
        (5, "App Store Policy Compliance", "✗", "✓", "✓", "✓", "✓"),
        (6, "Performance Monitoring", "Basic", "Standard", "Advanced", "Real-time", "Real-time"),
        (7, "Server/API Monitoring", "✗", "Basic", "Full", "Full", "Full+Alerts"),
        (8, "Database Backups", "Weekly", "Daily", "Daily", "Hourly", "Continuous"),
        (9, "Security Patches", "Quarterly", "Monthly", "Bi-weekly", "Weekly", "As needed"),
        (10, "Feature Updates (small)", "✗", "1/month", "2/month", "4/month", "Unlimited"),
        (11, "App Store Updates", "2/year", "4/year", "Monthly", "Bi-weekly", "As needed"),
        (12, "Analytics Reports", "✗", "Monthly", "Bi-weekly", "Weekly", "Daily"),
        (13, "User Feedback Management", "✗", "✗", "✓", "✓", "✓"),
        (14, "Support Response Time", "48hrs", "24hrs", "12hrs", "4hrs", "1hr"),
        (15, "Support Channels", "Email", "Email+Chat", "All", "All+Dedicated", "All+Dedicated"),
        (16, "Server Scaling Support", "✗", "✗", "Basic", "Full", "Full+Auto"),
        (17, "A/B Testing Support", "✗", "✗", "✓", "✓", "✓"),
        (18, "Priority Hotfix Deployment", "✗", "✗", "✓", "✓", "✓"),
    ]

    for r, item in enumerate(maintenance_items, 4):
        for c, val in enumerate(item, 1):
            ws2.cell(row=r, column=c, value=val)
        fill = alt_fill if r % 2 == 0 else None
        style_row(ws2, r, COLS2, fill=fill)
        ws2.cell(row=r, column=1).alignment = center_align
        for c in range(3, COLS2 + 1):
            ws2.cell(row=r, column=c).alignment = center_align

    # ── Sheet 3: App Complexity Guide ──────────────────────────────
    ws3 = wb.create_sheet("App Complexity Guide")
    ws3.sheet_properties.tabColor = "ED7D31"
    set_col_widths(ws3, [5, 25, 20, 20, 20])
    COLS3 = 5

    ws3.merge_cells("A1:E1")
    ws3.cell(row=1, column=1, value="APP COST BY TYPE & COMPLEXITY").font = Font(name="Calibri", bold=True, color=WHITE, size=14)
    ws3.cell(row=1, column=1).fill = PatternFill(start_color=ACCENT_ORANGE, end_color=ACCENT_ORANGE, fill_type="solid")
    ws3.cell(row=1, column=1).alignment = center_align
    for c in range(1, COLS3 + 1):
        ws3.cell(row=1, column=c).fill = PatternFill(start_color=ACCENT_ORANGE, end_color=ACCENT_ORANGE, fill_type="solid")

    app_headers = ["#", "App Type", "Simple (₹)", "Medium (₹)", "Complex (₹)"]
    for c, h in enumerate(app_headers, 1):
        ws3.cell(row=3, column=c, value=h)
    style_header_row(ws3, 3, COLS3, subheader_font, subheader_fill)

    app_types = [
        (1, "Business / Portfolio", "50K - 1L", "1L - 2.5L", "2.5L - 5L"),
        (2, "E-Commerce", "2L - 4L", "4L - 8L", "8L - 20L"),
        (3, "Social Networking", "3L - 6L", "6L - 15L", "15L - 40L"),
        (4, "On-Demand Service", "4L - 8L", "8L - 15L", "15L - 30L"),
        (5, "Food Delivery", "5L - 8L", "8L - 15L", "15L - 25L"),
        (6, "Ride Sharing", "6L - 10L", "10L - 20L", "20L - 40L"),
        (7, "FinTech / Banking", "5L - 10L", "10L - 20L", "20L - 50L"),
        (8, "Healthcare / Telemedicine", "4L - 8L", "8L - 18L", "18L - 35L"),
        (9, "Education / LMS", "3L - 6L", "6L - 12L", "12L - 25L"),
        (10, "Fitness / Wellness", "2L - 5L", "5L - 10L", "10L - 20L"),
        (11, "Chat / Messaging", "3L - 6L", "6L - 15L", "15L - 30L"),
        (12, "Streaming (Audio/Video)", "5L - 10L", "10L - 20L", "20L - 50L"),
        (13, "IoT / Smart Home", "4L - 8L", "8L - 18L", "18L - 35L"),
        (14, "AR / VR", "5L - 10L", "10L - 25L", "25L - 60L"),
    ]

    for r, item in enumerate(app_types, 4):
        for c, val in enumerate(item, 1):
            ws3.cell(row=r, column=c, value=val)
        fill = alt_fill if r % 2 == 0 else None
        style_row(ws3, r, COLS3, fill=fill)
        ws3.cell(row=r, column=1).alignment = center_align
        for c in range(3, COLS3 + 1):
            ws3.cell(row=r, column=c).alignment = center_align

    ws.freeze_panes = "A7"
    wb.save(path)
    print(f"✅ Created: {path}")


# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_dir = os.path.join(base, "excel")
    os.makedirs(excel_dir, exist_ok=True)

    create_website_excel(os.path.join(excel_dir, "Website-Pricing-Calculator.xlsx"))
    create_application_excel(os.path.join(excel_dir, "Application-Pricing-Calculator.xlsx"))

    print("\n🎉 All Excel files generated successfully!")
