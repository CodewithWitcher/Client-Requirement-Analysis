# Requirements Complete Guide

> Master reference guide documenting all technical requirement categories for both Website and Mobile Application projects — ideal for comprehensive scoping, proposal writing, and technical specification.

> **Covers:** 🌐 Website / Web App &nbsp;|&nbsp; 📱 Mobile Application

---

## Table of Contents

1. [Domain](#1-domain)
2. [Hosting](#2-hosting)
3. [SSL Certificate & Security](#3-ssl-certificate--security)
4. [Database](#4-database)
5. [Tech Stack](#5-tech-stack)
6. [Design & User Experience](#6-design--user-experience)
7. [Pages & Site Structure](#7-pages--site-structure)
8. [Features & Functionality](#8-features--functionality)
9. [E-Commerce](#9-e-commerce)
10. [Payment Integration](#10-payment-integration)
11. [Content Management](#11-content-management)
12. [SEO & Analytics](#12-seo--analytics)
13. [Performance & Traffic](#13-performance--traffic)
14. [Security & Compliance](#14-security--compliance)
15. [Third-Party Integrations](#15-third-party-integrations)
16. [Maintenance & Support](#16-maintenance--support)
17. [Timeline, Milestones & Release](#17-timeline-milestones--release)
18. [Legal & Compliance](#18-legal--compliance)
19. [Branding & Assets](#19-branding--assets)
20. [Communication & Project Management](#20-communication--project-management)

---

**📱 Application Additional:**

1. [Platform & Technology](#1-platform--technology)
2. [App Store & Deployment](#2-app-store--deployment)
3. [Design & User Experience](#3-design--user-experience)
4. [Authentication & User Management](#4-authentication--user-management)
5. [Features & Functionality](#5-features--functionality)
6. [Backend & API](#6-backend--api)
7. [Database & Storage](#7-database--storage)
8. [Push Notifications](#8-push-notifications)
9. [Payment & Monetization](#9-payment--monetization)
10. [Media & Content](#10-media--content)
11. [Device Features & Hardware](#11-device-features--hardware)
12. [Offline Capability](#12-offline-capability)
13. [Security](#13-security)
14. [Testing & Quality Assurance](#14-testing--quality-assurance)
15. [Performance Optimization](#15-performance-optimization)
16. [Analytics & Monitoring](#16-analytics--monitoring)
17. [Third-Party Integrations](#17-third-party-integrations)
18. [Maintenance & Support](#18-maintenance--support)
19. [Legal, Compliance & App Store Policies](#19-legal-compliance--app-store-policies)
20. [Timeline, Milestones & Release](#20-timeline-milestones--release)
21. [Communication & Project Management](#21-communication--project-management)

---

## 🌐 1. Domain

The domain is the web address (URL) of the website. Clarify who owns, registers, and manages it.

### Key Questions to Ask:
- Does the client already have a domain? If yes, what is it?
- Who is the current registrar? (GoDaddy, Namecheap, Google Domains, etc.)
- Does the client want a new domain? What name and extension?
- Will there be multiple domains (redirects)?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Domain Registration** | Client provides / Developer registers | If developer registers — include cost ($10–$50/year) |
| **Domain Extension** | .com, .in, .org, .io, .co, .net, .tech, .store, .app | Premium extensions cost more (.io = $30–$60/year) |
| **Domain Privacy Protection** | Enabled / Disabled | WHOIS privacy ($5–$15/year) |
| **Domain Transfer** | Required / Not required | Transfer fees and DNS migration time |
| **Subdomain Setup** | blog.site.com, shop.site.com, app.site.com | Additional DNS configuration |
| **Custom Email** | info@domain.com, support@domain.com | Google Workspace / Zoho Mail ($6–$12/user/month) |
| **Domain Renewal** | Annual / Multi-year | Long-term registration discounts |
| **DNS Management** | Developer-managed / Client-managed | Ongoing management responsibility |

### Pricing Considerations:
- If you handle domain registration, charge the domain cost + a setup fee ($20–$50).
- If the client provides the domain, ensure you get DNS access or nameserver delegation.
- Custom email setup is a separate line item.

---

---

## 🌐 2. Hosting

Hosting is where the website files, database, and media live. This is one of the most critical pricing factors.

### Key Questions to Ask:
- Does the client have existing hosting? If yes, what provider?
- What type of hosting does the project require?
- What is the expected traffic volume?
- Are there geographic requirements for the server?
- Does the client need email hosting as well?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Hosting Type** | Shared / VPS / Dedicated / Cloud / Managed | Shared = $3–$15/mo, VPS = $20–$100/mo, Cloud = $50–$500+/mo |
| **Hosting Provider** | AWS, DigitalOcean, Hostinger, Bluehost, GoDaddy, Vercel, Netlify, Railway, Render | Provider choice affects cost and features |
| **Server OS** | Linux (Ubuntu/CentOS) / Windows Server | Linux is standard; Windows for .NET |
| **Storage** | 5GB / 10GB / 50GB / 100GB / Unlimited | Based on media files, database size |
| **Bandwidth** | 100GB / 500GB / 1TB / Unlimited | Based on expected traffic |
| **RAM** | 512MB / 1GB / 2GB / 4GB / 8GB+ | Higher for dynamic applications |
| **CPU** | 1 Core / 2 Cores / 4 Cores / 8 Cores | Higher for compute-heavy applications |
| **Server Location** | US / Europe / India / Asia-Pacific / Multi-region | Affects latency for target audience |
| **Uptime SLA** | 99.9% / 99.95% / 99.99% | Higher SLA = higher cost |
| **Backup Frequency** | Daily / Weekly / Monthly / None | Automated backups add cost |
| **Managed vs Unmanaged** | Managed (provider handles updates) / Unmanaged (you handle) | Managed = higher monthly cost |
| **Email Hosting** | Included / Separate (Google Workspace, Zoho) | $5–$12/user/month if separate |
| **Staging Environment** | Yes / No | Separate staging server adds cost |
| **CDN Included** | Yes / No / Separate (Cloudflare, AWS CloudFront) | Free tier available, premium = $20+/mo |
| **Auto-Scaling** | Yes / No | Cloud hosting with auto-scaling for traffic spikes |
| **Containerization** | Docker / Kubernetes / None | Adds complexity and cost |
| **CI/CD Pipeline** | Yes / No | GitHub Actions, GitLab CI, Jenkins setup |

### Hosting Type Comparison:

| Type | Best For | Monthly Cost | Performance |
|------|----------|-------------|-------------|
| **Shared Hosting** | Small sites, blogs, portfolios | $3–$15 | Low |
| **VPS (Virtual Private Server)** | Medium businesses, moderate traffic | $20–$100 | Medium |
| **Cloud Hosting (AWS/GCP/Azure)** | Scalable applications, high traffic | $50–$500+ | High |
| **Dedicated Server** | Enterprise applications, maximum control | $100–$500+ | Very High |
| **Managed WordPress** | WordPress sites (WP Engine, Kinsta) | $25–$100 | Medium-High |
| **Static Hosting (Vercel/Netlify)** | Static sites, JAMstack, Next.js | Free–$20 | High |
| **Serverless (AWS Lambda, Vercel)** | API-driven, microservices | Pay-per-use | Variable |

### Pricing Considerations:
- Always clarify who pays the ongoing hosting bill — client or you.
- If you manage hosting, charge a monthly management fee ($50–$200/month).
- Setup fee for server configuration ($100–$500 one-time).
- Include hosting cost in the first year and quote renewals separately.

---

---

## 🌐 3. SSL Certificate & Security

SSL secures data transmission between the browser and server.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **SSL Type** | Free (Let's Encrypt) / Domain Validated / Organization Validated / Extended Validation | Free–$300/year |
| **Wildcard SSL** | Yes (covers subdomains) / No | $50–$200/year |
| **SSL Provider** | Let's Encrypt, Cloudflare, Comodo, DigiCert, GeoTrust | Varies significantly |
| **Auto-Renewal** | Enabled / Manual | Setup for auto-renewal |
| **HTTPS Redirect** | Forced HTTPS / Mixed content | Configuration effort |

---

---

## 🌐 4. Database

The database stores all dynamic content, user data, orders, and application state.

### Key Questions to Ask:
- What type of data will be stored?
- How much data is expected over 1 year? 5 years?
- Is real-time data access needed?
- Are there existing databases to migrate from?
- What are the data backup and recovery requirements?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Database Type** | Relational (SQL) / Non-Relational (NoSQL) / Both | Architecture choice |
| **Database Engine** | MySQL / PostgreSQL / MongoDB / Firebase / Supabase / DynamoDB / SQLite | Engine affects hosting options |
| **Database Size** | Small (<1GB) / Medium (1–10GB) / Large (10–100GB) / Enterprise (100GB+) | Storage costs scale |
| **Number of Tables/Collections** | <10 / 10–50 / 50–100 / 100+ | Complexity indicator |
| **Read/Write Ratio** | Read-heavy / Write-heavy / Balanced | Affects optimization strategy |
| **Backup Strategy** | Daily automated / Weekly / On-demand / None | $10–$100/month for managed backups |
| **Backup Retention** | 7 days / 30 days / 90 days / 1 year | Longer retention = higher cost |
| **Replication** | Single instance / Read replicas / Multi-region | High availability adds cost |
| **Data Migration** | No migration / Simple import / Complex ETL | $200–$2,000 based on complexity |
| **Database Hosting** | Same server / Managed service (RDS, Atlas, PlanetScale) | Managed services = $15–$200+/month |
| **Connection Pooling** | Yes / No | For high-concurrency apps |
| **Caching Layer** | None / Redis / Memcached | Performance boost, $15–$50/month |
| **Search Engine** | None / Elasticsearch / Algolia / Meilisearch | Full-text search capability $0–$100+/month |

### Database Engine Comparison:

| Engine | Type | Best For | Managed Service Cost |
|--------|------|----------|---------------------|
| **MySQL** | SQL | Traditional web apps, WordPress, PHP | $15–$100/mo |
| **PostgreSQL** | SQL | Complex queries, data integrity, analytics | $15–$100/mo |
| **MongoDB** | NoSQL | Flexible schema, real-time, JSON-heavy | $57+/mo (Atlas) |
| **Firebase Firestore** | NoSQL | Real-time apps, mobile backends | Free–$100+/mo |
| **Supabase** | SQL (Postgres) | Open-source Firebase alternative | Free–$25+/mo |
| **SQLite** | SQL | Small apps, prototypes, embedded | Free |
| **DynamoDB** | NoSQL | Serverless, AWS ecosystem | Pay-per-use |
| **Redis** | In-memory | Caching, sessions, real-time leaderboards | $15–$50/mo |

### Pricing Considerations:
- Database design and schema creation: $200–$1,000
- Data migration from existing system: $300–$2,000
- Database optimization and indexing: $100–$500
- Ongoing database management: $50–$200/month

---

---

## 🌐 5. Tech Stack

The technology stack determines the tools, languages, and frameworks used to build the website.

### Key Questions to Ask:
- Is there a preferred technology? (Often tied to existing systems)
- Does the team have in-house developers for maintenance?
- What is the expected lifespan of the website?
- Any requirement for a specific CMS?
- Are there SEO requirements that affect framework choice?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Frontend Framework** | HTML/CSS/JS (Vanilla) / React / Next.js / Vue.js / Angular / Svelte / Astro | Framework complexity affects dev time |
| **CSS Framework** | Tailwind CSS / Bootstrap / Material UI / Custom CSS / Shadcn UI | $0–$500 for custom styling |
| **Backend Language** | Node.js / Python / PHP / Java / C# / Ruby / Go | Language choice affects hosting |
| **Backend Framework** | Express.js / Django / Laravel / Spring Boot / ASP.NET / Rails / FastAPI | Framework affects development speed |
| **CMS** | None (Custom) / WordPress / Strapi / Contentful / Sanity / Ghost / Drupal | CMS licensing and customization costs |
| **Static Site Generator** | Next.js / Gatsby / Hugo / Astro / 11ty | Good for blogs, portfolios, docs |
| **API Architecture** | REST / GraphQL / tRPC / None | GraphQL adds 20–30% dev time |
| **Authentication** | Custom / Firebase Auth / Auth0 / Clerk / NextAuth / Supabase Auth | Auth service = $0–$100+/month |
| **State Management** | None / Redux / Zustand / Jotai / Context API | Complexity for frontend |
| **Package Manager** | npm / yarn / pnpm / bun | Developer preference |
| **Build Tool** | Vite / Webpack / Turbopack / esbuild | Modern tools improve DX |
| **Testing** | None / Jest / Playwright / Cypress / Vitest | Testing adds 15–25% dev time |
| **Version Control** | Git (GitHub / GitLab / Bitbucket) | Standard for all projects |
| **TypeScript** | Yes / No | Adds 10–15% dev time, better quality |

### Tech Stack Comparison (Common Combinations):

| Stack | Components | Best For | Dev Time Multiplier |
|-------|-----------|----------|-------------------|
| **WordPress** | PHP + MySQL + Themes | Blogs, small businesses, content sites | 1x (fastest) |
| **MERN** | MongoDB + Express + React + Node.js | Full-stack web apps | 1.5x |
| **MEAN** | MongoDB + Express + Angular + Node.js | Enterprise web apps | 1.7x |
| **Next.js Full-Stack** | Next.js + PostgreSQL + Prisma | Modern web apps, SEO-critical | 1.3x |
| **LAMP** | Linux + Apache + MySQL + PHP | Traditional web apps | 1x |
| **Django** | Python + Django + PostgreSQL | Data-heavy apps, dashboards | 1.4x |
| **Laravel** | PHP + Laravel + MySQL | E-commerce, SaaS, CRM | 1.3x |
| **JAMstack** | Static (Astro/Hugo) + Headless CMS + CDN | Static sites, blogs, portfolios | 0.8x |

### Pricing Considerations:
- WordPress site (theme-based): $500–$3,000
- WordPress (custom theme): $2,000–$10,000
- Custom-coded site (React/Next.js): $3,000–$25,000+
- Full-stack application: $10,000–$100,000+
- Technology consulting fee (stack recommendation): $200–$500

---

---

## 6. Design & User Experience

### 🌐 Website

Design is one of the highest-value components and often the first thing clients care about.

### Key Questions to Ask:
- Does the client have existing branding (logo, colors, fonts)?
- Is there any design inspiration or reference websites?
- Do they want custom design or are they okay with a template?
- How many design revisions are expected?
- Is a mobile-first approach needed?
- Do they need prototyping or wireframing?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Design Approach** | Custom Design / Template/Theme-based / Hybrid | Custom = 3–5x more expensive |
| **Wireframing** | Yes (Low-fidelity) / Yes (High-fidelity) / No | $300–$2,000 |
| **Prototyping** | Interactive prototype in Figma/Adobe XD / No | $500–$3,000 |
| **UI Design Tool** | Figma / Adobe XD / Sketch / Canva | Figma is industry standard |
| **Responsive Design** | Desktop only / Desktop + Tablet / Desktop + Tablet + Mobile | Mobile-responsive is standard |
| **Number of Unique Page Designs** | 3–5 / 5–10 / 10–20 / 20+ | Each unique page = $200–$1,000 |
| **Design Revisions** | 2 rounds / 3 rounds / Unlimited | Unlimited revisions = higher cost |
| **Dark Mode** | Yes / No | +10–15% design/dev effort |
| **Animations & Micro-interactions** | None / Subtle / Heavy (parallax, scroll effects) | Heavy = +20–40% dev time |
| **Accessibility (WCAG)** | Level A / Level AA / Level AAA / None | AA is recommended, AAA is rare |
| **Icon Set** | Free (Heroicons, Lucide) / Premium (FontAwesome Pro) / Custom | Custom icons = $500–$2,000 |
| **Typography** | Google Fonts (free) / Adobe Fonts / Custom fonts | Custom fonts = licensing fee |
| **Image Style** | Stock photos / Custom photography / Illustrations / AI-generated | Custom photography = $500–$5,000 |
| **Design System** | None / Basic style guide / Full design system | Full design system = $2,000–$10,000 |

### Pricing Tiers for Design:

| Tier | Includes | Price Range |
|------|----------|-------------|
| **Basic** | Template-based, minor color/font changes, responsive | $200–$800 |
| **Standard** | Semi-custom, wireframes, 5–8 unique pages, 2 revisions | $1,000–$3,000 |
| **Premium** | Fully custom, prototyping, animations, 10+ pages, 3 revisions | $3,000–$10,000 |
| **Enterprise** | Full design system, user research, A/B testing, unlimited revisions | $10,000–$50,000+ |

---

### 📱 Mobile Application

Mobile design has unique requirements compared to web design.

### Key Questions to Ask:
- Do you have existing branding (logo, colors, fonts)?
- Any reference apps for design inspiration?
- Custom design or standard platform look?
- How important are animations and transitions?
- Accessibility requirements?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Design Approach** | Custom UI / Platform-native (Material/Cupertino) / Hybrid | Custom = 2–3x more expensive |
| **Wireframing** | No / Low-fidelity / High-fidelity | $300–$2,000 |
| **Interactive Prototype** | No / Figma prototype / Principle / After Effects | $500–$3,000 |
| **Design Tool** | Figma / Sketch / Adobe XD | Figma is industry standard |
| **Number of Screens** | 5–10 / 10–25 / 25–50 / 50+ | Each screen = $100–$500 in design |
| **Platform-Specific Design** | Unified / Separate iOS & Android designs | Separate = +30% design cost |
| **Design System** | None / Basic components / Full design system | Full system = $2,000–$10,000 |
| **Material Design (Android)** | Standard compliance / Custom Material theme | Google guidelines compliance |
| **Human Interface (iOS)** | Standard compliance / Custom styling | Apple guidelines compliance |
| **Dark Mode** | No / Yes (system-controlled) / Yes (in-app toggle) | +15–25% design & dev effort |
| **Theming** | Single theme / Light + Dark / Custom themes | Multiple themes = +20% effort |
| **Animations** | None / Subtle (standard transitions) / Heavy (custom, complex) | Heavy = +25–40% dev time |
| **Micro-interactions** | None / Basic (button feedback, pulls) / Advanced | Advanced = +15–25% dev time |
| **Onboarding Flow** | None / Simple (3–5 slides) / Interactive walkthrough | $300–$2,000 |
| **Splash Screen** | Default / Animated / Branded | $100–$500 |
| **Design Revisions** | 2 rounds / 3 rounds / Unlimited | Define in contract |
| **Icon Set** | Platform default / Custom icon pack | Custom = $500–$2,000 |
| **Illustration Style** | None / Stock / Custom | Custom = $500–$3,000 |
| **Typography** | System fonts / Google Fonts / Custom fonts | Custom font licensing |
| **Accessibility** | None / Basic (font scaling, contrast) / Full (VoiceOver, TalkBack) | Full = +15–20% dev time |
| **Landscape Support** | Portrait only / Both orientations | Both = +10–15% development |
| **Adaptive Layout** | Phones only / Phones + Tablets / All screen sizes | Tablet support = +30% |

### Screen Design Pricing:

| Screen Type | Complexity | Price Range (Design) |
|-------------|-----------|---------------------|
| Splash/Launch | Simple | $50–$150 |
| Onboarding (per slide) | Simple | $50–$150 |
| Login/Signup | Medium | $150–$400 |
| Home/Dashboard | High | $300–$800 |
| List/Feed Screen | Medium | $150–$400 |
| Detail Screen | Medium | $150–$400 |
| Profile Screen | Medium | $150–$400 |
| Settings Screen | Low | $100–$250 |
| Search Screen | Medium–High | $200–$500 |
| Map Screen | High | $300–$600 |
| Chat Screen | High | $300–$700 |
| Cart/Checkout | High | $300–$800 |
| Notification Center | Medium | $150–$400 |
| Modal/Bottom Sheet | Low | $50–$200 |
| Error/Empty States | Low | $50–$150 each |

---

---

## 🌐 7. Pages & Site Structure

Understanding the site map is critical for accurate pricing.

### Key Questions to Ask:
- How many pages does the website need?
- Which pages are static and which are dynamic?
- Is there a blog or news section?
- Is there a user dashboard or admin panel?
- Do they need multi-language support?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Total Pages** | 1–5 / 5–10 / 10–25 / 25–50 / 50+ | Each page = $100–$500 |
| **Static Pages** | Home, About, Contact, Services, Portfolio | Simpler to build |
| **Dynamic Pages** | Product listings, blog posts, user profiles | Require database integration |
| **Landing Pages** | 0 / 1–3 / 3–5 / 5+ | Marketing-optimized pages |
| **Blog Section** | No / Basic (posts only) / Advanced (categories, tags, search, comments) | $300–$2,000 |
| **Admin Dashboard** | No / Basic / Advanced (analytics, user management) | $1,000–$10,000 |
| **User Dashboard** | No / Profile only / Full dashboard (orders, settings, notifications) | $1,000–$8,000 |
| **Multi-Language** | No / 2 languages / 3–5 languages / 10+ languages | Each language adds 30–50% content cost |
| **Sitemap** | Auto-generated / Custom | Usually auto-generated |
| **URL Structure** | Simple / SEO-optimized / Custom | SEO-optimized URLs are standard |
| **Breadcrumbs** | Yes / No | Minor effort |
| **404 Custom Page** | Yes / No | Custom branded 404 page |
| **Search Functionality** | No / Basic search / Advanced (filters, faceted search) | $200–$2,000 |

### Common Page Types & Pricing:

| Page Type | Complexity | Price Range |
|-----------|-----------|-------------|
| Home Page | High (hero, features, testimonials, CTA) | $300–$1,500 |
| About Us | Low–Medium | $100–$400 |
| Contact Page (with form) | Low–Medium | $100–$400 |
| Services/Products Page | Medium | $200–$600 |
| Individual Service Page | Medium | $150–$500 |
| Blog Listing Page | Medium | $200–$600 |
| Blog Post Template | Medium | $200–$500 |
| Portfolio/Gallery | Medium–High | $300–$800 |
| FAQ Page | Low | $100–$300 |
| Pricing Page | Medium | $200–$500 |
| Testimonials Page | Low–Medium | $150–$400 |
| Team/Staff Page | Low–Medium | $150–$400 |
| Login/Register Page | Medium–High | $300–$800 |
| User Dashboard | High | $1,000–$5,000 |
| Admin Panel | Very High | $2,000–$10,000 |
| Product Detail Page | Medium–High | $300–$1,000 |
| Cart & Checkout | Very High | $1,000–$5,000 |
| Order Tracking | High | $500–$2,000 |
| Terms & Privacy | Low | $50–$200 |

---

---

## 8. Features & Functionality

### 🌐 Website

This is where the scope can balloon quickly. Be very specific about what's included.

### Parameters:

| Feature | Options | Complexity | Price Range |
|---------|---------|-----------|-------------|
| **Contact Form** | Basic / Advanced (file upload, conditional fields) | Low–Medium | $100–$500 |
| **User Registration** | Email/Password / Social login / Phone OTP | Medium–High | $500–$2,000 |
| **User Authentication** | Session-based / JWT / OAuth 2.0 | Medium | $300–$1,000 |
| **Role-Based Access** | None / 2 roles / Multiple roles | Medium–High | $500–$2,500 |
| **Email Notifications** | None / Transactional / Marketing | Medium | $200–$1,000 |
| **SMS Notifications** | None / OTP only / Full SMS | Medium | $300–$1,500 |
| **Push Notifications (Web)** | None / Basic / Advanced | Medium | $300–$1,000 |
| **Live Chat** | None / Third-party (Crisp, Tawk.to) / Custom | Low–High | $0–$3,000 |
| **Chatbot** | None / Rule-based / AI-powered | Medium–Very High | $500–$10,000+ |
| **Newsletter Subscription** | None / Basic / Integration (Mailchimp, SendGrid) | Low–Medium | $100–$500 |
| **Social Media Sharing** | None / Share buttons / Auto-post | Low | $50–$300 |
| **Social Media Feed** | None / Instagram / Twitter / Facebook | Low–Medium | $100–$500 |
| **Review & Ratings** | None / Basic / Advanced (verified, photos) | Medium | $300–$1,500 |
| **Booking/Appointment** | None / Calendar-based / Full booking system | Medium–High | $500–$5,000 |
| **File Upload** | None / Images only / Multi-file / Large files | Medium | $200–$1,000 |
| **PDF Generation** | None / Invoices / Reports / Certificates | Medium | $300–$1,500 |
| **Maps Integration** | None / Google Maps embed / Interactive maps | Low–Medium | $100–$500 |
| **Video Player** | None / YouTube/Vimeo embed / Custom player | Low–Medium | $100–$800 |
| **Image Gallery** | None / Basic grid / Lightbox / Masonry | Low–Medium | $100–$600 |
| **Drag & Drop** | None / Kanban board / Page builder / File upload | Medium–High | $500–$3,000 |
| **Real-Time Features** | None / Chat / Notifications / Collaboration | High | $1,000–$5,000 |
| **Data Export** | None / CSV / Excel / PDF | Medium | $200–$800 |
| **Data Import** | None / CSV upload / API sync / Bulk import | Medium–High | $300–$1,500 |
| **Multi-Tenant** | No / Yes | Very High | $5,000–$20,000+ |
| **Cron Jobs / Scheduled Tasks** | None / Email digests / Report generation / Data cleanup | Medium | $200–$1,000 |
| **Wishlist/Favorites** | None / Basic / With notifications | Low–Medium | $200–$600 |
| **Comparison Feature** | None / Side-by-side / Table view | Medium | $300–$1,000 |
| **Referral System** | None / Basic codes / Full affiliate | Medium–High | $500–$3,000 |
| **Notification Center** | None / In-app / In-app + Email + SMS | Medium–High | $500–$2,000 |

---

### 📱 Mobile Application

The core functionality that defines the app's purpose and value.

### Parameters:

| Feature | Options | Complexity | Price Range |
|---------|---------|-----------|-------------|
| **User Feed/Timeline** | None / Chronological / Algorithmic | Medium–High | $1,000–$5,000 |
| **Search** | None / Basic (local) / Advanced (server-side + filters) | Medium–High | $500–$3,000 |
| **Chat/Messaging** | None / 1-to-1 / Group / Multimedia (images, files) | High–Very High | $2,000–$15,000 |
| **Voice/Video Call** | None / Voice only / Video only / Both | Very High | $5,000–$25,000 |
| **Social Features** | None / Like / Like + Comment / Full social (follow, share, report) | Medium–High | $1,000–$8,000 |
| **Content Posting** | None / Text / Text + Images / Text + Images + Video | Medium–High | $1,000–$5,000 |
| **Stories/Status** | None / Image stories / Video stories (24-hr disappearing) | High | $3,000–$10,000 |
| **Maps & Geolocation** | None / Show location on map / Real-time tracking / Navigation | Medium–Very High | $500–$10,000 |
| **QR Code** | None / Scanner / Generator / Both | Low–Medium | $200–$800 |
| **Barcode Scanner** | None / 1D barcodes / 2D barcodes / Both | Low–Medium | $200–$1,000 |
| **Calendar/Events** | None / View only / Create + RSVP / Full calendar management | Medium–High | $500–$5,000 |
| **Booking/Scheduling** | None / Time slot booking / Calendar-based / Service booking | High | $2,000–$8,000 |
| **File Management** | None / Upload / Upload + Download + View / Full document management | Medium–High | $500–$3,000 |
| **Order Management** | None / Basic (status tracking) / Full (history, reorder, returns) | Medium–High | $1,000–$5,000 |
| **Reviews & Ratings** | None / Star rating / Rating + Review / Verified + Photos | Medium | $500–$2,000 |
| **Wishlist/Favorites** | None / Simple save / Organized collections | Low–Medium | $200–$800 |
| **Referral System** | None / Share code / Full affiliate with rewards | Medium–High | $500–$3,000 |
| **Gamification** | None / Points/XP / Badges / Leaderboard / Levels | Medium–High | $1,000–$5,000 |
| **Subscription/Membership** | None / Tiers / Paywalled content | Medium–High | $1,000–$5,000 |
| **Multi-Language (i18n)** | Single language / 2–3 / 5–10 / 10+ | Low–Medium | $200–$500/language |
| **Accessibility** | None / Basic / Full (screen readers, haptics) | Medium | $500–$3,000 |
| **Deep Linking** | None / Basic / Universal/App links / Deferred deep links | Low–Medium | $200–$1,000 |
| **Share Functionality** | None / System share sheet / Custom share cards | Low | $100–$400 |
| **In-App Browser** | None / WebView / Chrome Custom Tabs / SafariVC | Low | $100–$300 |
| **Data Export** | None / PDF / CSV / Both | Medium | $300–$1,000 |
| **Surveys/Polls** | None / Simple polls / Full survey forms | Medium | $500–$2,000 |
| **Task/Todo Management** | None / Basic list / Full (categories, priorities, reminders) | Medium–High | $1,000–$4,000 |
| **Dashboard/Analytics** | None / Basic charts / Full analytics dashboard | Medium–High | $1,000–$5,000 |
| **Admin Panel (Web)** | None / Basic / Full admin dashboard (web-based) | High | $3,000–$15,000 |

---

---

## 🌐 9. E-Commerce

If the website is an online store, this section is critical.

### Key Questions to Ask:
- How many products will be listed (now and in the future)?
- Are products physical, digital, or both?
- Is there a subscription model?
- Shipping — domestic, international, or both?
- Tax calculation requirements?
- Inventory management needs?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **E-Commerce Type** | None / Simple (few products) / Full store / Marketplace | Marketplace = highest complexity |
| **Product Count** | 1–10 / 10–100 / 100–1,000 / 1,000+ | Affects catalog design |
| **Product Type** | Physical / Digital / Service / Subscription / Mixed | Each type has different logic |
| **Product Variants** | None / Size/Color / Multiple attributes | Variant management adds complexity |
| **Product Reviews** | None / Basic / Verified purchase / With photos | $200–$1,000 |
| **Inventory Management** | None / Basic stock tracking / Advanced (warehouse, multi-location) | $500–$5,000 |
| **Shopping Cart** | Simple / Persistent / Multi-vendor | $300–$2,000 |
| **Wishlist** | Yes / No | $200–$500 |
| **Checkout Process** | Single page / Multi-step / Guest checkout | Multi-step = $500–$2,000 |
| **Order Management** | Basic / Advanced (status tracking, notifications) | $500–$3,000 |
| **Shipping Calculation** | Free / Flat rate / Weight-based / API-based (FedEx, UPS) | API integration = $500–$2,000 |
| **Tax Calculation** | None / Manual / Automated (tax API) | Automated = $200–$1,000 |
| **Coupon/Discount System** | None / Basic codes / Advanced (rules, tiers, auto-apply) | $300–$1,500 |
| **Invoice Generation** | None / Basic / Branded / Tax-compliant | $200–$1,000 |
| **Return/Refund Management** | None / Basic / Full (RMA process) | $300–$2,000 |
| **Vendor/Seller Management** | None / Single vendor / Multi-vendor marketplace | Marketplace = $10,000–$50,000+ |
| **Product Comparison** | None / Yes | $300–$1,000 |
| **Recently Viewed** | None / Yes | $100–$300 |
| **Product Recommendations** | None / Manual / AI-powered | $200–$5,000 |
| **Abandoned Cart Recovery** | None / Email reminders / Full flow | $300–$1,500 |

### E-Commerce Platform Comparison:

| Platform | Best For | Cost | Customization |
|----------|----------|------|---------------|
| **WooCommerce** | WordPress stores | Free (+ plugins) | High |
| **Shopify** | All-in-one stores | $29–$399/mo | Medium |
| **Custom (Next.js + DB)** | Unique requirements | Dev cost only | Full |
| **Medusa.js** | Headless e-commerce | Free (open-source) | Very High |
| **Saleor** | Enterprise headless | Free–$2,000/mo | Very High |
| **BigCommerce** | Large catalogs | $29–$299/mo | Medium |

---

---

## 🌐 10. Payment Integration

Payment processing is where money flows — get this right.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Payment Gateway** | Stripe / Razorpay / PayPal / Square / Braintree / PayU / CCAvenue | Each gateway = $300–$1,000 to integrate |
| **Number of Gateways** | 1 / 2 / 3+ | Each additional = +$300–$500 |
| **Payment Methods** | Credit/Debit cards / UPI / Net Banking / Wallets / EMI / BNPL | Each method within gateway |
| **Multi-Currency** | No / Yes (2–5 currencies) / Yes (global) | $200–$1,000 |
| **Recurring Payments** | No / Monthly subscriptions / Annual / Custom intervals | $500–$2,000 |
| **Invoice Payments** | No / Yes (pay via link) | $200–$800 |
| **Split Payments** | No / Yes (marketplace commission) | $500–$2,000 |
| **Refund Handling** | Manual / Automated / Partial refunds | $200–$800 |
| **Payment Security** | PCI DSS compliant / 3D Secure / Tokenization | Usually handled by gateway |
| **Webhook Integration** | Yes / No | Payment status callbacks $200–$500 |
| **Test Environment** | Sandbox / Test mode | Standard for all integrations |
| **Payment Analytics** | Basic / Advanced dashboard | $200–$1,000 |

### Payment Gateway Comparison:

| Gateway | Best For | Transaction Fee | Regions |
|---------|----------|----------------|---------|
| **Stripe** | Global, developers | 2.9% + $0.30 | Global |
| **Razorpay** | India | 2% | India |
| **PayPal** | International payments | 3.49% + $0.49 | Global |
| **Square** | In-person + online | 2.6% + $0.10 | US, UK, CA, AU, JP |
| **Braintree** | PayPal-owned, enterprise | 2.59% + $0.49 | Global |
| **PayU** | India, emerging markets | 2% | India, LatAm, EMEA |
| **CCAvenue** | India | 2–3% | India |

---

---

## 🌐 11. Content Management

Content is what makes the website valuable. Clarify who creates and manages it.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Content Provider** | Client provides all / Developer creates / Mix | Content writing = $50–$200/page |
| **CMS Needed** | No (static) / Yes (client can edit) | CMS adds $500–$3,000 to project |
| **CMS Type** | WordPress / Strapi / Contentful / Sanity / Custom admin | See CMS comparison |
| **Content Types** | Text / Images / Videos / Documents / Audio | Rich content types need more setup |
| **Content Volume** | <10 pages / 10–50 / 50–200 / 200+ | Affects content entry time |
| **Content Migration** | No / From old website / From documents / From database | $300–$5,000 |
| **Media Management** | Basic upload / DAM (Digital Asset Management) | DAM = $1,000–$5,000 |
| **Content Workflow** | Direct publish / Draft → Review → Publish | Approval workflow = $500–$2,000 |
| **Content Versioning** | No / Yes | Built into most CMS |
| **Multi-Language Content** | No / 2 languages / 5+ languages | Translation management system |
| **SEO Content Fields** | None / Meta titles/descriptions / Full schema | Usually included in CMS |
| **Content Scheduling** | No / Yes (publish at future date) | $200–$500 |

---

---

## 🌐 12. SEO & Analytics

Search visibility and data tracking are critical for business websites.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **On-Page SEO** | None / Basic (meta tags, headings) / Advanced (schema, structured data) | $300–$2,000 |
| **Technical SEO** | None / Sitemap + robots.txt / Full (speed, crawlability, Core Web Vitals) | $500–$3,000 |
| **Google Analytics** | Not needed / GA4 setup / GA4 + Custom events + Conversions | $100–$1,000 |
| **Google Search Console** | Not needed / Setup + Configuration | $100–$300 |
| **Google Tag Manager** | Not needed / Setup | $200–$500 |
| **Heatmaps & Session Recording** | None / Hotjar / Microsoft Clarity / FullStory | $0–$100/mo |
| **A/B Testing** | None / Google Optimize / VWO / Custom | $0–$500/mo |
| **Page Speed Optimization** | Basic / Advanced (lazy loading, code splitting, image optimization) | $300–$1,500 |
| **Sitemap** | Auto-generated / Custom | Standard |
| **Schema Markup** | None / Basic / Advanced (product, FAQ, article, breadcrumb) | $200–$1,000 |
| **Open Graph Tags** | None / Basic / Full (with images) | $100–$300 |
| **Canonical URLs** | Yes / No | Standard |
| **Redirect Management** | None / 301 redirects from old site | $100–$500 |
| **Local SEO** | None / Google Business Profile / Full local setup | $200–$1,000 |

---

---

## 🌐 13. Performance & Traffic

Understanding expected traffic helps determine infrastructure requirements.

### Key Questions to Ask:
- How many visitors do you expect per month?
- Are there seasonal traffic spikes?
- Where is the target audience located?
- What should the page load time target be?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Expected Monthly Traffic** | <1,000 / 1,000–10,000 / 10,000–100,000 / 100,000+ | Determines hosting tier |
| **Traffic Spikes** | No / Occasional (sales, events) / Regular (media coverage) | Auto-scaling needed |
| **CDN (Content Delivery Network)** | None / Cloudflare Free / Cloudflare Pro / AWS CloudFront | $0–$200+/month |
| **Image Optimization** | None / Compression / WebP/AVIF conversion / Responsive images | $200–$800 |
| **Code Optimization** | None / Minification / Tree-shaking / Code splitting | Standard good practice |
| **Caching Strategy** | None / Browser caching / Server caching / Full-page caching / Redis | $200–$1,000 |
| **Lazy Loading** | None / Images / Images + Components | Standard practice |
| **Load Balancing** | None / Application load balancer / Multi-server | $50–$300/month |
| **Database Optimization** | None / Indexing / Query optimization / Read replicas | $200–$1,000 |
| **Performance Monitoring** | None / Lighthouse / New Relic / Datadog | $0–$500/month |
| **Target Load Time** | <5 seconds / <3 seconds / <1 second (LCP) | Faster = more optimization effort |
| **Core Web Vitals** | Not prioritized / Passing scores / Excellent scores | $300–$1,500 |
| **Compression** | None / Gzip / Brotli | Server configuration |
| **HTTP/2 or HTTP/3** | HTTP/1.1 / HTTP/2 / HTTP/3 | Modern hosting includes this |

### Traffic & Hosting Recommendations:

| Monthly Visitors | Recommended Hosting | Est. Monthly Cost |
|-----------------|-------------------|-------------------|
| <1,000 | Shared hosting / Static hosting | $3–$15 |
| 1,000–10,000 | VPS / Managed hosting | $20–$50 |
| 10,000–50,000 | Cloud VPS / Managed cloud | $50–$150 |
| 50,000–200,000 | Cloud hosting with CDN | $150–$500 |
| 200,000–1,000,000 | Auto-scaling cloud + Load balancer | $500–$2,000 |
| 1,000,000+ | Multi-region cloud, dedicated infrastructure | $2,000+ |

---

---

## 🌐 14. Security & Compliance

Security is non-negotiable, especially for sites handling user data or payments.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **SSL Certificate** | Free (Let's Encrypt) / Paid (OV/EV) | $0–$300/year |
| **Web Application Firewall (WAF)** | None / Cloudflare / AWS WAF / Sucuri | $20–$200/month |
| **DDoS Protection** | None / Basic (Cloudflare Free) / Advanced | $0–$200/month |
| **Rate Limiting** | None / API rate limiting / Login attempt limiting | $100–$500 |
| **Input Validation** | Basic / Advanced (XSS, SQL injection prevention) | Standard practice |
| **Content Security Policy (CSP)** | None / Basic / Strict | $100–$300 |
| **Two-Factor Authentication** | None / Email / SMS / Authenticator app | $200–$800 |
| **Password Policy** | Basic / Advanced (complexity, expiry, breached check) | $100–$400 |
| **Activity Logging** | None / Login logs / Full audit trail | $200–$1,000 |
| **Data Encryption** | At rest / In transit / Both | Standard for sensitive data |
| **Security Headers** | None / Basic / Full (HSTS, X-Frame, X-Content-Type) | $100–$300 |
| **Vulnerability Scanning** | None / Monthly / Continuous | $50–$500/month |
| **Backup & Disaster Recovery** | None / Daily backups / Full DR plan | $50–$500/month |
| **CAPTCHA** | None / reCAPTCHA / hCaptcha | $0–$100 |
| **IP Blocking** | None / Geo-blocking / Rate-based | $100–$300 |

---

---

## 15. Third-Party Integrations

### 🌐 Website

External services that the website needs to connect with.

### Parameters:

| Integration | Options | Pricing Impact |
|-------------|---------|---------------|
| **Email Service** | None / SMTP / SendGrid / Mailchimp / Amazon SES | $100–$500 + service costs |
| **CRM** | None / HubSpot / Salesforce / Zoho / Custom | $500–$5,000 |
| **ERP** | None / SAP / Tally / Custom | $2,000–$15,000 |
| **Social Media Login** | None / Google / Facebook / Apple / GitHub | $200–$500 per provider |
| **Google Maps** | None / Embed / Interactive / Route planning | $100–$1,000 |
| **Shipping Provider** | None / FedEx / UPS / DHL / Shiprocket / Delhivery | $500–$2,000 per provider |
| **SMS Provider** | None / Twilio / MSG91 / AWS SNS | $200–$800 |
| **Cloud Storage** | None / AWS S3 / Google Cloud Storage / Cloudinary | $100–$500 + storage costs |
| **Video Conferencing** | None / Zoom / Google Meet / Custom (WebRTC) | $500–$5,000 |
| **Calendar Integration** | None / Google Calendar / Calendly / Custom | $200–$1,000 |
| **Accounting Software** | None / QuickBooks / Xero / Tally | $500–$3,000 |
| **Marketing Automation** | None / Mailchimp / ActiveCampaign / HubSpot | $300–$2,000 |
| **Webhook/API Integration** | None / 1–3 APIs / 3–10 APIs / 10+ APIs | Each API = $200–$1,000 |
| **AI/ML Services** | None / OpenAI / Google AI / Custom model | $500–$10,000+ |
| **WhatsApp Business** | None / Chat button / Full API integration | $200–$2,000 |

---

### 📱 Mobile Application

External services the mobile app needs to integrate with.

### Parameters:

| Integration | Options | Pricing Impact |
|-------------|---------|---------------|
| **Maps** | None / Google Maps / Apple Maps / Mapbox / OpenStreetMap | $200–$1,500 + API cost |
| **Social Media Sharing** | None / System share / Deep link sharing | $100–$500 |
| **Social Media Login** | None / Google / Apple / Facebook / Multiple | $100–$300 per provider |
| **SMS/OTP** | None / Firebase Phone Auth / Twilio / MSG91 | $200–$500 + per-SMS cost |
| **Email Service** | None / SendGrid / Mailchimp / Amazon SES | $200–$500 + service cost |
| **Cloud Storage** | None / AWS S3 / Firebase Storage / Cloudinary | $100–$500 + storage cost |
| **CDN** | None / Cloudflare / CloudFront / Fastly | $0–$200+/month |
| **Machine Learning** | None / Firebase ML / TensorFlow Lite / Core ML / OpenAI API | $500–$10,000+ |
| **AR SDK** | None / ARKit (iOS) / ARCore (Android) / Vuforia | $2,000–$15,000 |
| **Payment SDK** | None / Stripe / Razorpay / PayPal / Apple Pay / Google Pay | $500–$2,000 per gateway |
| **Chat SDK** | None / Firebase / SendBird / Stream / GetStream | $0–$500+/month |
| **Video SDK** | None / Agora / Twilio Video / Jitsi / Vonage | $0–$500+/month |
| **CRM Integration** | None / Salesforce / HubSpot / Zoho | $500–$3,000 |
| **ERP Integration** | None / SAP / Oracle / Custom | $2,000–$15,000 |
| **IoT/Hardware** | None / BLE devices / Smart home / Wearables | $2,000–$20,000 |
| **WhatsApp Business** | None / Share button / Full API | $200–$2,000 |
| **Crash/Error Tracking** | None / Sentry / Crashlytics / Bugsnag | $0–$100+/month |
| **Deep Linking** | None / Firebase Dynamic Links / Branch / Adjust | $0–$500+/month |
| **Attribution** | None / Adjust / AppsFlyer / Branch | $0–$500+/month |

---

---

## 16. Maintenance & Support

Post-launch maintenance is a significant recurring revenue opportunity.

### Key Questions to Ask:
- Does the client need ongoing maintenance?
- Who will handle content updates?
- What is the expected response time for issues?
- Is 24/7 support required?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Maintenance Contract** | None / Monthly / Quarterly / Annual | Monthly = $100–$1,000 |
| **Bug Fixes** | Warranty period only / Ongoing | Warranty = 30–90 days free |
| **Content Updates** | Client self-service / Developer handles | $50–$200/month |
| **Plugin/Dependency Updates** | No / Monthly / Weekly | $100–$300/month |
| **Security Patches** | No / Monthly / As needed | $100–$300/month |
| **Uptime Monitoring** | No / Basic / Advanced (with alerts) | $10–$50/month |
| **Performance Monitoring** | No / Monthly report / Real-time | $50–$200/month |
| **Backup Management** | No / Automated + Verified | $30–$100/month |
| **Support Hours** | Business hours / Extended / 24/7 | 24/7 = premium pricing |
| **Response Time SLA** | 48 hours / 24 hours / 4 hours / 1 hour | Faster SLA = higher cost |
| **Support Channels** | Email / Phone / Chat / Ticket system | Multi-channel = higher cost |
| **Feature Enhancements** | Not included / Minor updates / Major updates | Separate quote or hourly rate |
| **Hosting Management** | Not included / Included | $50–$200/month |
| **Training** | None / Documentation / Video / Live sessions | $200–$1,000 |

### Maintenance Plan Tiers:

| Plan | Includes | Monthly Price Range |
|------|---------|-------------------|
| **Basic** | Bug fixes, security updates, backups | $100–$300 |
| **Standard** | Basic + content updates, monthly report, email support | $300–$600 |
| **Premium** | Standard + performance monitoring, priority support, minor enhancements | $600–$1,500 |
| **Enterprise** | Premium + 24/7 support, SLA, dedicated account manager | $1,500–$5,000+ |

---

**📱 Application Additional:**

Post-launch maintenance is crucial for mobile apps (more so than websites).
- Who will submit app updates to the stores?
- How quickly should critical bugs be fixed?
- Are OS update compatibility fixes expected?
- Is crash monitoring needed?
| **Maintenance Contract** | None / Monthly / Quarterly / Annual | Monthly = $200–$2,000 |
| **Bug Fixes** | Warranty only (30–90 days) / Ongoing | Warranty = included |
| **OS Updates** | Not covered / Annual compatibility check / Proactive | Annual = $1,000–$5,000 |
| **App Store Updates** | Not covered / Quarterly / Monthly / As needed | $200–$500/update |
| **Framework/Library Updates** | Not covered / Quarterly / As needed | $200–$800/quarter |
| **Security Patches** | Not covered / Monthly / As needed | $100–$500/patch |
| **Performance Monitoring** | Not included / Monthly report / Real-time | $100–$500/month |
| **Crash Monitoring** | Not included / Alert on new crashes / Full analysis | $50–$300/month |
| **Feature Enhancements** | Not included / Minor updates / Major features | Separate quote/hourly |
| **Support Hours** | Business hours / Extended / 24/7 | Premium = 2–3x cost |
| **Response Time SLA** | 48 hours / 24 hours / 4 hours / 1 hour | Faster = premium |
| **Support Channels** | Email / Chat / Phone / Ticket | Multi-channel = higher |
| **Backup Management** | Not included / Database backups / Full backup | $50–$200/month |
| **Hosting Management** | Not included / Server maintenance / Full DevOps | $100–$500/month |
| **Analytics Reporting** | Not included / Monthly / Weekly | $100–$300/month |
| **App Store Optimization (ongoing)** | Not included / Quarterly review / Monthly optimization | $200–$1,000/month |
| **Basic** | Bug fixes, crash monitoring, security patches | $200–$500 |
| **Standard** | Basic + OS updates, monthly report, email support | $500–$1,000 |
| **Premium** | Standard + performance monitoring, priority support, minor enhancements | $1,000–$2,500 |
| **Enterprise** | Premium + 24/7 support, SLA, dedicated account manager, analytics | $2,500–$8,000+ |

---

## 17. Timeline, Milestones & Release

### 🌐 Website

Setting clear timelines prevents scope creep and manages expectations.

### Parameters:

| Parameter | Options | Notes |
|-----------|---------|-------|
| **Project Timeline** | 2–4 weeks / 1–2 months / 2–4 months / 4–6 months / 6+ months | Based on scope |
| **Discovery Phase** | 1–2 weeks / Not needed | Requirements gathering |
| **Design Phase** | 1–3 weeks / 2–6 weeks | Wireframes + Mockups + Revisions |
| **Development Phase** | 2–8 weeks / 2–4 months | Core development |
| **Testing Phase** | 1–2 weeks / 2–4 weeks | QA and bug fixing |
| **Content Entry** | Client handles / Developer handles (1–2 weeks) | Content population |
| **Launch Preparation** | 3–5 days | DNS, SSL, final checks |
| **Release Strategy** | Big bang (all at once) / Phased / Soft launch → Full launch | Phased reduces risk |
| **Milestones** | 3–5 key milestones / Weekly deliverables | Payment tied to milestones |
| **Payment Schedule** | 50/50 / 30/30/40 / Monthly / Milestone-based | Milestone-based recommended |
| **Change Request Process** | Formal (written + approval) / Informal | Formal process prevents disputes |
| **Revision Policy** | 2 rounds / 3 rounds / Unlimited / Per revision cost | Define clearly in contract |
| **Post-Launch Support** | 15 days / 30 days / 60 days / 90 days | Free bug fix period |

### Recommended Milestone Structure:

| Milestone | Deliverable | Payment % |
|-----------|------------|----------|
| **Project Kickoff** | Requirements document, sitemap, wireframes | 20% |
| **Design Approval** | UI/UX mockups (all pages) | 20% |
| **Development Complete** | Functional website on staging | 30% |
| **Testing & Revisions** | Bug-free, client-approved | 20% |
| **Launch & Handover** | Live website + documentation | 10% |

---

### 📱 Mobile Application

Mobile app timelines are typically longer than website timelines.

### Parameters:

| Parameter | Options | Notes |
|-----------|---------|-------|
| **Project Timeline** | 1–2 months / 2–4 months / 4–6 months / 6–12 months / 12+ months | Based on scope |
| **Discovery & Planning** | 1–2 weeks / 2–4 weeks | Requirements, architecture |
| **UI/UX Design** | 2–4 weeks / 4–8 weeks | Wireframes + Mockups + Prototype |
| **Development (MVP)** | 4–8 weeks / 8–16 weeks | Core features |
| **Development (Full)** | 8–16 weeks / 16–32 weeks | All features |
| **Backend Development** | 2–8 weeks / 8–16 weeks | API, database, admin panel |
| **Testing & QA** | 2–4 weeks / 4–8 weeks | All testing types |
| **Beta Testing** | 1–2 weeks / 2–4 weeks | TestFlight / Internal track |
| **App Store Submission** | 1–2 weeks | Review + potential rejections |
| **Post-Launch Monitoring** | 2–4 weeks | Bug fixes, performance tuning |
| **Release Strategy** | MVP → Full / Soft launch → Full / Big bang | MVP recommended |
| **MVP Scope** | Core 3–5 features | Launch fast, iterate |
| **Feature Releases** | Monthly / Bi-weekly / Sprint-based | Agile approach |
| **Payment Schedule** | 40/30/30 / 30/30/20/20 / Milestone-based | Milestone-based recommended |

### Recommended Milestone Structure:

| Milestone | Deliverable | Payment % | Timeline |
|-----------|------------|----------|----------|
| **Project Kickoff** | Requirements doc, architecture, tech stack decision | 15% | Week 1–2 |
| **Design Complete** | All screens designed in Figma, prototype approved | 20% | Week 3–6 |
| **Backend API Ready** | API endpoints, database, authentication | 15% | Week 4–8 |
| **App v1 (Alpha)** | Core features working on staging | 20% | Week 6–12 |
| **App v2 (Beta)** | All features, bug fixes, beta testing | 15% | Week 10–16 |
| **Store Submission** | App approved and live on stores | 10% | Week 14–18 |
| **Post-Launch Support** | 30-day monitoring, bug fixes, optimization | 5% | Week 18–22 |

---

---

## 🌐 18. Legal & Compliance

Never ignore legal requirements — they can have serious consequences.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Privacy Policy** | Not needed / Template / Custom (lawyer-reviewed) | $100–$500 |
| **Terms of Service** | Not needed / Template / Custom | $100–$500 |
| **Cookie Consent** | Not needed / Basic banner / GDPR-compliant with preferences | $100–$500 |
| **GDPR Compliance** | Not applicable / Basic / Full (DPO, data mapping) | $500–$5,000 |
| **CCPA Compliance** | Not applicable / Basic / Full | $500–$3,000 |
| **ADA/WCAG Accessibility** | Not required / Level A / Level AA / Level AAA | $500–$5,000 |
| **Data Retention Policy** | Not needed / Basic / Custom | $200–$1,000 |
| **Copyright Notices** | Yes / No | Standard |
| **Intellectual Property** | Client owns all / Developer retains license / Shared | Define in contract |
| **NDA (Non-Disclosure Agreement)** | Not needed / Mutual NDA | Standard practice |
| **Disclaimer Pages** | Not needed / Yes | $100–$300 |
| **Age Verification** | Not needed / Yes | $200–$500 |
| **Data Processing Agreement** | Not needed / Yes | For GDPR compliance |

---

---

## 🌐 19. Branding & Assets

Understand what branding materials the client has or needs.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Logo** | Client provides / Need new logo / Redesign existing | New logo = $200–$2,000 |
| **Brand Colors** | Defined / Needs creation | Color palette creation = $100–$500 |
| **Typography** | Defined / Needs selection | Font selection + licensing |
| **Brand Guidelines** | Existing / Need creation | Brand guide = $500–$2,000 |
| **Photography** | Client provides / Stock photos / Custom shoot | Custom = $500–$5,000 |
| **Video Content** | Not needed / Client provides / Need production | Production = $1,000–$10,000+ |
| **Illustrations** | Not needed / Stock / Custom | Custom = $500–$3,000 |
| **Favicon** | Client provides / Create from logo | $50–$100 |
| **Social Media Assets** | Not needed / Cover images + Profile pictures | $100–$500 |
| **Print Materials** | Not needed / Business cards / Brochures / Flyers | $200–$1,000 per item |

---

---

## 20. Communication & Project Management

**🌐 Website**

How the project will be managed and how client communication will work.

### Parameters:

| Parameter | Options | Notes |
|-----------|---------|-------|
| **Project Management Tool** | None / Trello / Jira / Asana / Notion / ClickUp | Choose one and share with client |
| **Communication Channel** | Email / WhatsApp / Slack / Microsoft Teams / Phone | Define primary channel |
| **Status Updates** | Weekly / Bi-weekly / Daily standups | Weekly is standard |
| **Demo/Review Meetings** | Per milestone / Weekly / Bi-weekly | Schedule in advance |
| **Staging Access** | Shared URL / Password-protected / VPN | Client should review on staging |
| **Documentation** | None / User manual / Technical docs / Video tutorials | $300–$2,000 |
| **Source Code Access** | Not provided / GitHub repository / Full handover | Define in contract |
| **Training Sessions** | None / 1 hour / 3 hours / Full training program | $100–$500/hour |
| **Point of Contact** | Single / Multiple stakeholders | Multiple = longer review cycles |
| **Feedback Format** | Written (email/document) / Annotated screenshots / Loom videos | Define expectations early |

---

---

**📱 Application**

Managing client communication throughout access development.

### Parameters:

| Parameter | Options | Notes |
|-----------|---------|-------|
| **Project Management Tool** | Trello / Jira / Asana / Notion / Linear / ClickUp | Choose one |
| **Sprint Duration** | 1 week / 2 weeks / 3 weeks | 2 weeks is standard |
| **Communication Channel** | Email / Slack / WhatsApp / Microsoft Teams | Define primary |
| **Status Updates** | Daily / Weekly / Per sprint | Weekly minimum |
| **Demo/Review Meetings** | Per milestone / Per sprint / Weekly | Sprint demos recommended |
| **Build Sharing** | TestFlight / Firebase App Distribution / Direct APK | Regular test builds |
| **Bug Reporting Tool** | Email / Jira / Linear / Notion / Custom form | Structured reporting |
| **Design Review** | Figma comments / Meetings / Annotated screenshots | Define process |
| **Code Repository Access** | No access / Read-only / Full access | Depends on contract |
| **Documentation** | None / API docs / User manual / Technical architecture | $300–$2,000 |
| **Handover** | Source code only / Code + docs + training / Full handover | Define scope |
| **Training** | None / 1–2 hours / Full training program | $100–$500/hour |
| **Point of Contact** | Single / Multiple stakeholders | Single preferred |

---

---

## 📊 Quick Price Estimation Formula

### 🌐 Website

```
Total Website Price = 
    Domain & Hosting Setup Fee
  + Design Cost (based on pages × complexity)
  + Development Cost (hourly rate × estimated hours)
  + Feature Cost (sum of individual features)
  + Integration Cost (per integration)
  + Content Cost (per page if developer handles)
  + Testing & QA (10–15% of dev cost)
  + Project Management (5–10% of total)
  + Contingency Buffer (10–20% of total)
```

### Hourly Rate Reference:

| Developer Level | Hourly Rate (USD) | Hourly Rate (INR) |
|----------------|-------------------|-------------------|
| Junior | $15–$30 | ₹500–₹1,000 |
| Mid-Level | $30–$60 | ₹1,000–₹2,500 |
| Senior | $60–$120 | ₹2,500–₹5,000 |
| Expert/Agency | $120–$250+ | ₹5,000–₹15,000+ |

---

*This guide should be updated as new technologies and pricing standards emerge. Last updated: March 2026.*

### 📱 Mobile Application

```
Total App Price = 
    Platform Cost Multiplier
  × (Design Cost + Development Cost + Backend Cost)
  + App Store Setup Fee
  + Testing & QA (15–25% of dev cost)
  + Third-Party Service Setup
  + Project Management (5–10% of total)
  + Contingency Buffer (15–25% of total)
```

### Platform Cost Multipliers:

| Platform | Multiplier |
|----------|-----------|
| Single platform (iOS or Android) | 1.0x |
| Cross-platform (Flutter/React Native) | 1.3–1.5x |
| Both native (Swift + Kotlin) | 1.8–2.0x |
| Native + Web app | 2.2–2.5x |

### App Complexity & Pricing Guide:

| Complexity | Screens | Features | Timeline | Price Range |
|-----------|---------|----------|----------|-------------|
| **Simple** | 5–10 | Auth, list/detail, basic CRUD | 1–2 months | $3,000–$15,000 |
| **Medium** | 10–25 | Social features, payments, notifications | 2–4 months | $15,000–$50,000 |
| **Complex** | 25–50 | Real-time, maps, chat, admin panel | 4–8 months | $50,000–$150,000 |
| **Enterprise** | 50+ | Multi-tenant, offline, integrations, security | 8–18 months | $150,000–$500,000+ |

### Hourly Rate Reference:

| Developer Level | Hourly Rate (USD) | Hourly Rate (INR) |
|----------------|-------------------|-------------------|
| Junior | $15–$30 | ₹500–₹1,000 |
| Mid-Level | $30–$60 | ₹1,000–₹2,500 |
| Senior | $60–$120 | ₹2,500–₹5,000 |
| Expert/Agency | $120–$250+ | ₹5,000–₹15,000+ |

---

*This guide should be updated as new technologies and pricing standards emerge. Last updated: March 2026.*

---

## 📱 1. Platform & Technology

The most fundamental decision — which platforms and technology to use.

### Key Questions to Ask:
- Do you need an iOS app, Android app, or both?
- Is a web app (PWA) acceptable, or must it be a native app?
- Does the client have any technology preferences?
- Are there performance-critical features (AR, real-time, gaming)?
- Will the team maintain the app in-house after delivery?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Target Platform** | iOS only / Android only / Both (iOS + Android) / Web (PWA) | Both = 1.5–1.8x single platform cost |
| **Development Approach** | Native (Swift/Kotlin) / Cross-Platform (Flutter/React Native) / Hybrid (Ionic/Capacitor) / PWA | See comparison below |
| **iOS Language** | Swift / Objective-C (legacy) | Swift is standard |
| **Android Language** | Kotlin / Java (legacy) | Kotlin is standard |
| **Cross-Platform Framework** | Flutter / React Native / .NET MAUI / KMM (Kotlin Multiplatform) | Framework choice affects dev time |
| **Minimum iOS Version** | iOS 14 / iOS 15 / iOS 16 / iOS 17 / Latest only | Older support = more testing effort |
| **Minimum Android Version** | Android 8 (API 26) / Android 10 / Android 12 / Android 13+ | Older support = more compatibility work |
| **Tablet Support** | No / Yes (responsive) / Yes (dedicated tablet UI) | Dedicated tablet UI = +30–50% design |
| **Wearable Support** | No / Apple Watch / Wear OS / Both | Each wearable = +$5,000–$20,000 |
| **TV App** | No / Apple TV / Android TV / Both | Each TV app = +$10,000–$30,000 |
| **Architecture** | MVC / MVVM / Clean Architecture / Redux | Affects maintainability and cost |
| **State Management** | Provider / Bloc / Riverpod (Flutter) / Redux / MobX (React Native) | Standard for framework |
| **Package Manager** | CocoaPods/SPM (iOS) / Gradle (Android) / pub (Flutter) / npm (RN) | Standard for framework |

### Development Approach Comparison:

| Approach | Platforms | Performance | Dev Time | Cost Multiplier | Best For |
|----------|----------|-------------|----------|----------------|----------|
| **Native (Swift + Kotlin)** | Separate codebases | Excellent | 2x (parallel dev) | 2x | Performance-critical, AR/VR, complex animations |
| **Flutter** | Single codebase | Very Good | 1x | 1x | Most apps, beautiful UI, fast development |
| **React Native** | Single codebase | Good | 1.1x | 1.1x | Web dev teams, shared logic with web |
| **Ionic/Capacitor** | Single codebase | Moderate | 0.9x | 0.9x | Simple apps, web-first approach |
| **PWA** | Web browser | Moderate | 0.7x | 0.7x | Content apps, low device feature needs |
| **KMM** | Shared logic, native UI | Excellent | 1.3x | 1.3x | Shared business logic, platform-specific UI |

### Technology Cost Comparison:

| Project Type | Native (per platform) | Flutter/React Native (both platforms) |
|-------------|----------------------|--------------------------------------|
| Simple app (5–10 screens) | $5,000–$15,000 | $3,000–$10,000 |
| Medium app (10–25 screens) | $15,000–$50,000 | $10,000–$35,000 |
| Complex app (25–50 screens) | $50,000–$150,000 | $35,000–$100,000 |
| Enterprise app (50+ screens) | $150,000–$500,000+ | $100,000–$350,000+ |

---

---

## 📱 2. App Store & Deployment

Deploying to app stores has specific requirements and costs.

### Key Questions to Ask:
- Does the client have Apple Developer and Google Play accounts?
- Who will manage the app store listings?
- Is internal distribution needed (enterprise apps)?
- Is beta testing required before launch?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Apple Developer Account** | Client has / Developer creates / Client creates | $99/year (required for iOS) |
| **Google Play Console** | Client has / Developer creates / Client creates | $25 one-time (required for Android) |
| **App Store Listing Setup** | Developer handles / Client handles | $200–$500 per platform |
| **App Name & Keywords** | Client provides / Developer researches (ASO) | ASO = $200–$1,000 |
| **App Description** | Client writes / Developer writes | $100–$300 per platform |
| **Screenshots & Previews** | Client provides / Developer creates | $200–$800 (5–8 screenshots per platform) |
| **App Preview Video** | None / Yes | $500–$3,000 |
| **App Icon Design** | Client provides / Developer designs | $100–$500 |
| **Feature Graphic (Android)** | Client provides / Developer designs | $50–$200 |
| **Privacy Policy URL** | Client provides / Developer creates | Required for both stores |
| **App Category** | Client decides / Developer recommends | Strategy discussion |
| **Age Rating** | Client provides info / Developer handles questionnaire | Required for submission |
| **App Review Handling** | Developer handles / Client handles | First submission can take 1–7 days |
| **Distribution Type** | Public / TestFlight (iOS) / Internal Testing (Android) / Enterprise | Enterprise = Apple Enterprise Program ($299/year) |
| **Beta Testing** | None / TestFlight (iOS) / Firebase App Distribution / Both | $200–$500 setup |
| **CI/CD Pipeline** | None / Fastlane / Codemagic / Bitrise / GitHub Actions | $300–$2,000 setup |
| **Automated Builds** | None / On push / On PR / Scheduled | CI/CD service = $0–$100/month |
| **Code Signing** | Developer manages / Client manages | Certificates and provisioning profiles |
| **App Updates** | Developer pushes / Client pushes (with training) | Ongoing responsibility |
| **OTA Updates** | None / CodePush (React Native) / Shorebird (Flutter) | $0–$500/month |

### App Store Submission Checklist:

| Requirement | Apple App Store | Google Play Store |
|-------------|-----------------|-------------------|
| **Account** | Apple Developer ($99/year) | Play Console ($25 one-time) |
| **App Icon** | 1024×1024 px | 512×512 px |
| **Screenshots** | Min 3 per device type | Min 2 per device type |
| **Description** | Up to 4,000 chars | Up to 4,000 chars |
| **Privacy Policy** | Required | Required |
| **Review Time** | 1–7 days (avg 24–48 hrs) | Few hours to 7 days |
| **Content Rating** | Required questionnaire | Required questionnaire |
| **Data Safety** | App Privacy labels | Data safety form |
| **In-App Purchases** | 30% commission (15% small business) | 30% commission (15% small business) |

---

---

## 📱 4. Authentication & User Management

User login and profile management is needed for most apps.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Registration Method** | Email + Password / Phone (OTP) / Social Login / All | Each method = $200–$500 |
| **Social Login Providers** | Google / Apple / Facebook / Twitter/X / GitHub / LinkedIn | Each = $100–$300 |
| **Phone OTP** | None / SMS / WhatsApp | SMS service cost + $300–$800 dev |
| **Email Verification** | None / Email link / Email code | $200–$500 |
| **Forgot Password** | None / Email reset / Phone reset | $200–$400 |
| **Biometric Login** | None / Fingerprint / Face ID / Both | $200–$500 |
| **Two-Factor Auth (2FA)** | None / SMS / Authenticator app / Both | $300–$1,000 |
| **Session Management** | Auto logout / Remember me / Multi-device | $200–$600 |
| **Role-Based Access** | None / 2 roles / Multiple roles / Custom permissions | $500–$3,000 |
| **Profile Management** | Basic (name, email) / Advanced (avatar, bio, preferences) | $300–$1,000 |
| **Account Deletion** | Not needed / Required (App Store policy) | Required for iOS apps |
| **Guest Mode** | No / Limited access / Full trial | $200–$500 |
| **Auth Service** | Custom / Firebase Auth / Auth0 / Supabase Auth / Clerk | See comparison below |
| **Token Management** | JWT / Session / OAuth 2.0 tokens | Standard implementation |
| **SSO (Single Sign-On)** | None / SAML / OAuth / OpenID Connect | Enterprise feature = $1,000–$5,000 |

### Authentication Service Comparison:

| Service | Free Tier | Paid Starting | Social Logins | Phone Auth |
|---------|-----------|--------------|---------------|------------|
| **Firebase Auth** | 10K verifications/mo | Pay-per-use | Yes | Yes |
| **Auth0** | 7,500 MAU | $23/mo | Yes | Yes |
| **Supabase Auth** | 50K MAU | $25/mo (includes DB) | Yes | Yes |
| **Clerk** | 10K MAU | $25/mo | Yes | Yes |
| **AWS Cognito** | 50K MAU | Pay-per-use | Yes | Yes |
| **Custom** | N/A | Dev cost only | Manual integration | Manual |

---

---

## 📱 6. Backend & API

The server-side infrastructure that powers the app.

### Key Questions to Ask:
- Is there an existing backend/API?
- What is the expected user base (now and future)?
- Are real-time features needed?
- Is a web admin panel needed alongside the mobile app?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Backend Type** | Custom Backend / BaaS (Firebase, Supabase) / Serverless | Custom = highest cost |
| **Backend Language** | Node.js / Python / Java / Go / Rust / PHP / C# | Language affects dev time |
| **Backend Framework** | Express.js / NestJS / Django / FastAPI / Spring Boot / Laravel / Gin | Framework affects speed |
| **API Type** | REST / GraphQL / gRPC / WebSocket | GraphQL = +20% dev time |
| **API Documentation** | None / Swagger/OpenAPI / Postman collection | $200–$500 |
| **Real-Time Communication** | None / WebSocket / Server-Sent Events / Firebase Realtime | $500–$3,000 |
| **File Upload/Storage** | None / Local server / AWS S3 / Firebase Storage / Cloudinary | $200–$1,000 + storage cost |
| **Image Processing** | None / Resize/Compress / Thumbnails / Filters | $200–$1,000 |
| **Video Processing** | None / Compression / Transcoding / Streaming | $1,000–$5,000 |
| **Background Jobs** | None / Email queue / Image processing / Report generation | $300–$1,500 |
| **Cron Jobs** | None / Data cleanup / Notifications / Reports | $200–$800 |
| **Rate Limiting** | None / Basic / Advanced (per user, per endpoint) | $200–$500 |
| **API Versioning** | None / URL versioning / Header versioning | $200–$400 |
| **Microservices** | Monolith / 2–3 services / Full microservices | Each service = +$5,000–$20,000 |
| **Message Queue** | None / RabbitMQ / Apache Kafka / AWS SQS | $500–$2,000 |
| **Containerization** | None / Docker / Kubernetes | Docker = $500, K8s = $2,000–$5,000 |
| **CI/CD** | None / GitHub Actions / GitLab CI / Jenkins | $300–$2,000 |
| **Hosting** | Shared / VPS / Cloud (AWS/GCP/Azure) / Serverless | $10–$1,000+/month |
| **Auto-Scaling** | None / Horizontal / Vertical | Cloud with auto-scaling |

### Backend Service Comparison:

| Service | Type | Best For | Monthly Cost | Dev Time Multiplier |
|---------|------|----------|-------------|-------------------|
| **Firebase** | BaaS | Quick launch, real-time, small-medium apps | Free–$100+ | 0.5x |
| **Supabase** | BaaS | Firebase alternative with SQL | Free–$25+ | 0.5x |
| **AWS Amplify** | BaaS | AWS ecosystem integration | Pay-per-use | 0.6x |
| **Custom (Node.js)** | Custom | Full control, complex logic | Server cost | 1x |
| **Custom (Django/Python)** | Custom | Data-heavy, ML integration | Server cost | 1.1x |
| **Serverless (Lambda)** | Serverless | Event-driven, variable traffic | Pay-per-use | 0.8x |
| **Appwrite** | BaaS | Self-hosted BaaS | Free (self-hosted) | 0.5x |

---

---

## 📱 7. Database & Storage

Data management strategy for the mobile application.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Cloud Database** | Firebase Firestore / Supabase (PostgreSQL) / MongoDB Atlas / AWS DynamoDB / PlanetScale | Service cost varies |
| **Local Database** | None / SQLite / Hive / ObjectBox / Realm / Room (Android) / Core Data (iOS) | Built into app |
| **Offline-First Database** | None / WatermelonDB / Realm / PouchDB + CouchDB | $1,000–$5,000 |
| **Data Sync** | None / One-way (cloud → device) / Two-way sync | Two-way = +$2,000–$5,000 |
| **Caching Strategy** | None / In-memory / Disk cache / Hybrid | $200–$800 |
| **File Storage** | None / App internal / AWS S3 / Firebase Storage / Cloudinary | $100–$500 + storage cost |
| **Media Storage Size** | <1GB / 1–10GB / 10–100GB / 100GB+ | Storage cost = $0.023–$0.2/GB/month |
| **Data Encryption** | None / At rest / In transit / Both | Standard practice |
| **Data Migration** | None / From existing system | $500–$3,000 |
| **Seed Data** | None / Static / Dynamic | Initial data population |
| **Data Backup** | None / Daily / Real-time | $10–$100/month |
| **Search (Full-Text)** | None / Local search / Algolia / Elasticsearch | $0–$100+/month |

### Storage Cost Comparison:

| Service | Free Tier | Cost per GB/month | Best For |
|---------|-----------|-------------------|----------|
| **Firebase Storage** | 5GB | $0.026/GB | Small-medium apps |
| **AWS S3** | 5GB (12 months) | $0.023/GB | Large-scale storage |
| **Supabase Storage** | 1GB | $0.021/GB | Supabase ecosystem |
| **Cloudinary** | 25GB bandwidth | $0.05/GB (bandwidth) | Image/video processing |
| **DigitalOcean Spaces** | N/A | $0.02/GB | Simple object storage |

---

---

## 📱 8. Push Notifications

Push notifications are critical for user engagement and retention.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Push Notification Service** | None / FCM (Firebase) / APNs + FCM / OneSignal / Pusher | $0–$100+/month |
| **Notification Types** | None / Basic (text) / Rich (images, actions, deep links) | Rich = +$500–$1,000 |
| **Targeting** | None / All users / Segments / Individual | Segment-based = +$300–$800 |
| **Scheduled Notifications** | None / One-time / Recurring | $200–$500 |
| **In-App Notifications** | None / Toast/Snackbar / Notification center / Badge counts | $300–$1,000 |
| **Email Notifications** | None / Transactional / Marketing | $200–$800 |
| **SMS Notifications** | None / OTP only / Full | SMS service cost + $300–$800 |
| **Notification Preferences** | None / Category-based opt-in/opt-out | $300–$800 |
| **Silent Notifications** | None / Data sync / Background updates | $200–$500 |
| **Geofence Notifications** | None / Location-based triggers | $500–$2,000 |
| **Time-Zone Aware** | No / Yes | $200–$400 |

### Notification Service Comparison:

| Service | Free Tier | Paid Starting | Rich Notifications | Analytics |
|---------|-----------|--------------|-------------------|-----------|
| **FCM (Firebase)** | Unlimited | Free | Yes | Basic |
| **OneSignal** | Unlimited | $9/mo | Yes | Advanced |
| **Pusher Beams** | 1K devices | $29/mo | Yes | Advanced |
| **Amazon SNS** | 1M publishes | Pay-per-use | Limited | Basic |

---

---

## 📱 9. Payment & Monetization

How the app makes money and processes payments.

### Key Questions to Ask:
- How will the app be monetized?
- Is it a paid app or free with in-app purchases?
- Are subscriptions needed?
- Will physical goods be sold (requiring external payment)?
- What regions will payments be accepted from?

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **App Pricing Model** | Free / Paid (one-time) / Freemium / Free with ads | Affects store listing |
| **In-App Purchases** | None / Consumable / Non-consumable / Both | $1,000–$5,000 per type |
| **Subscriptions** | None / Monthly / Annual / Multiple tiers | $2,000–$8,000 |
| **Subscription Management** | Custom / RevenueCat / Adapty / Glassfy | Service = $0–$100+/month |
| **Payment Gateway (for physical goods)** | None / Stripe / Razorpay / PayPal / Braintree | $500–$2,000 per gateway |
| **Wallet System** | None / Simple balance / Full wallet (add money, withdraw) | $2,000–$8,000 |
| **Ad Integration** | None / Banner / Interstitial / Rewarded video / Native ads | $500–$2,000 |
| **Ad Network** | None / Google AdMob / Facebook Audience / Unity Ads / IronSource | Usually Google AdMob |
| **Tipping/Donations** | None / Fixed amounts / Custom amounts | $500–$2,000 |
| **Multi-Currency** | No / Yes | $300–$1,000 |
| **Invoice Generation** | None / Basic / Tax-compliant | $300–$1,500 |
| **Payout to Sellers/Drivers** | None / Manual / Automated (Stripe Connect) | $2,000–$8,000 |
| **Promo Codes/Coupons** | None / Basic codes / Advanced (rules, limits, expiry) | $300–$1,500 |
| **Free Trial** | None / Time-limited / Feature-limited | Built into subscriptions |

### Important Apple/Google Payment Rules:

| Rule | Apple App Store | Google Play Store |
|------|----------------|-------------------|
| **Digital goods must use** | Apple In-App Purchase | Google Play Billing |
| **Commission** | 30% (15% for Small Business Program <$1M/yr) | 30% (15% for first $1M/yr) |
| **Physical goods** | Can use external payment (Stripe, etc.) | Can use external payment |
| **Services (ride, food delivery)** | Can use external payment | Can use external payment |
| **Subscriptions commission** | 30% first year → 15% after | 30% first year → 15% after |

### Subscription Integration Cost:

| Approach | Setup Cost | Monthly Cost | Revenue Optimized |
|----------|-----------|-------------|-------------------|
| **Native (StoreKit + Google Billing)** | $2,000–$5,000 | None | Manual |
| **RevenueCat** | $1,000–$3,000 | $0–$120/mo | Yes (paywalls, A/B testing) |
| **Adapty** | $1,000–$3,000 | $0–$99/mo | Yes (analytics, paywalls) |
| **Custom server** | $3,000–$8,000 | Server cost | Custom |

---

---

## 📱 10. Media & Content

How media files (images, videos, audio) are handled in the app.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Image Handling** | None / Display only / Upload + Display / Full (crop, filter, edit) | $200–$2,000 |
| **Image Source** | App assets only / Camera / Gallery / Both + Camera crop | $200–$800 |
| **Image Compression** | None / Client-side / Server-side / Both | $200–$500 |
| **Video Handling** | None / Playback only / Record + Upload + Stream | $500–$5,000 |
| **Video Player** | None / Basic / Custom controls / PiP (Picture-in-Picture) | $200–$2,000 |
| **Video Streaming** | None / Progressive download / HLS/DASH adaptive streaming | $1,000–$5,000 |
| **Audio Handling** | None / Playback / Record / Both | $300–$2,000 |
| **Audio Player** | None / Basic / Background playback / Lock screen controls | $300–$1,500 |
| **PDF Viewer** | None / Basic / Annotate + Sign | $200–$1,500 |
| **Document Scanner** | None / Camera-based / OCR text extraction | $500–$2,000 |
| **AR Content** | None / Face filters / 3D object placement / AR navigation | $5,000–$30,000+ |
| **Image CDN** | None / Cloudinary / Imgix / Cloudflare Images | $0–$100+/month |

---

---

## 📱 11. Device Features & Hardware

Mobile apps can leverage device hardware that websites cannot.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Camera** | None / Photo capture / Video recording / Barcode/QR scan | $200–$1,000 |
| **GPS/Location** | None / One-time location / Continuous tracking / Geofencing | $300–$3,000 |
| **Contacts Access** | None / Read contacts / Sync contacts | $200–$500 |
| **Calendar Access** | None / Read / Read + Write | $200–$500 |
| **Bluetooth** | None / BLE scanning / BLE communication / Classic Bluetooth | $1,000–$5,000 |
| **NFC** | None / Read tags / Read + Write | $500–$2,000 |
| **Biometrics** | None / Fingerprint / Face recognition / Both | $200–$500 |
| **Accelerometer/Gyroscope** | None / Motion detection / Step counter / Gesture recognition | $300–$2,000 |
| **Haptic Feedback** | None / Basic vibration / Custom haptic patterns | $100–$500 |
| **Clipboard** | None / Copy / Copy + Paste | $50–$200 |
| **Share Sheet** | None / System share / Custom share targets | $100–$300 |
| **File System Access** | None / Read / Read + Write | $200–$500 |
| **Microphone** | None / Voice recording / Voice recognition / Voice commands | $300–$3,000 |
| **Phone Calls** | None / Dial number / In-app VoIP | VoIP = $3,000–$10,000 |
| **SMS** | None / Send SMS / Read SMS (OTP auto-fill) | $100–$500 |
| **Health/Fitness Data** | None / HealthKit (iOS) / Google Fit / Both | $1,000–$5,000 per platform |
| **Background Location** | None / While in use / Always (requires justification) | +$500–$1,000 (strict review) |
| **Local Authentication** | None / Passcode / Biometric / Both | $200–$500 |
| **Widget Support** | None / iOS Widget / Android Widget / Both | $1,000–$3,000 per platform |
| **App Clips (iOS) / Instant Apps (Android)** | None / Basic / Full | $2,000–$5,000 |
| **Siri/Google Assistant Integration** | None / Basic shortcuts / Custom intents | $1,000–$3,000 |

---

---

## 📱 12. Offline Capability

Many apps need to work without internet connectivity.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Offline Mode** | None (online only) / Read-only offline / Full offline + sync | Full = $2,000–$10,000 |
| **Offline Data** | None / Cache last loaded / Configurable download | $500–$3,000 |
| **Sync Strategy** | None / Sync on connection / Manual sync / Real-time + offline fallback | $500–$3,000 |
| **Conflict Resolution** | None / Last write wins / Manual resolution / Custom merge | $500–$2,000 |
| **Offline Media** | None / Cached images / Downloaded media / Streaming cache | $500–$2,000 |
| **Queue Actions** | None / Queue form submissions / Queue all mutations | $500–$2,000 |
| **Connectivity Status** | None / Basic indicator / Detailed (WiFi/cellular/offline) | $100–$300 |

---

---

## 📱 13. Security

Mobile apps have unique security considerations.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Data Encryption (at rest)** | None / SQLCipher / Platform encryption | $300–$1,000 |
| **Data Encryption (in transit)** | HTTP (insecure) / HTTPS (TLS) / Certificate pinning | Pinning = $300–$800 |
| **Certificate Pinning** | None / Public key pinning / Certificate pinning | $300–$800 |
| **Secure Storage** | SharedPreferences / Keychain (iOS) + Keystore (Android) / Encrypted storage | $200–$500 |
| **Jailbreak/Root Detection** | None / Detect and warn / Block app on rooted devices | $200–$800 |
| **Code Obfuscation** | None / ProGuard (Android) / Basic / Advanced (DexGuard, iXGuard) | $200–$2,000 |
| **Tamper Detection** | None / Basic / Advanced | $500–$2,000 |
| **Biometric Security** | None / App unlock / Transaction auth | $200–$500 |
| **Session Security** | Basic tokens / Rotating tokens / Encrypted tokens + session management | $200–$800 |
| **API Security** | API key / OAuth 2.0 / JWT + refresh tokens | $200–$800 |
| **Data Masking** | None / Sensitive fields masked | $100–$400 |
| **Screenshot Prevention** | None / Yes (for sensitive screens) | $100–$300 |
| **Clipboard Security** | None / Clear clipboard after paste | $100–$200 |
| **Penetration Testing** | None / Single test / Ongoing | $2,000–$10,000 per test |
| **OWASP Mobile Top 10** | Not addressed / Partially / Fully compliant | Full = +15–20% security dev |

---

---

## 📱 14. Testing & Quality Assurance

Testing for mobile is more complex than web due to device fragmentation.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Unit Testing** | None / Critical paths / Comprehensive (>80% coverage) | +10–20% dev time |
| **Widget/Component Testing** | None / Key components / Comprehensive | +10–15% dev time |
| **Integration Testing** | None / API tests / Full flow tests | +10–20% dev time |
| **E2E Testing** | None / Happy paths / Comprehensive | +15–25% dev time |
| **E2E Testing Tool** | None / Appium / Detox / Maestro / Patrol (Flutter) | Tool setup + test writing |
| **Manual Testing** | Basic / Detailed test cases / Full regression suite | $500–$3,000 |
| **Device Testing** | Emulator only / 3–5 real devices / 10+ devices / Cloud device lab | Cloud lab = $50–$500/month |
| **Cloud Device Lab** | None / BrowserStack / AWS Device Farm / Firebase Test Lab | $0 (limited free) – $500/month |
| **Performance Testing** | None / Basic profiling / Load testing | $500–$2,000 |
| **Crash Reporting** | None / Firebase Crashlytics / Sentry / Bugsnag | $0–$100+/month |
| **Beta Testing** | None / Internal (TestFlight/Internal track) / External beta | $200–$500 setup |
| **Accessibility Testing** | None / Automated scan / Manual audit | $300–$2,000 |
| **Security Testing** | None / Automated scan (MobSF) / Manual pentest | $500–$10,000 |
| **User Acceptance Testing** | None / Client tests / Structured UAT | $300–$1,000 |
| **Regression Testing** | None / Manual / Automated | Automated = +$1,000–$3,000 |

### Testing Budget Rule:
- **Minimum:** 15–20% of development budget
- **Recommended:** 25–30% of development budget
- **Critical apps (fintech, health):** 30–40% of development budget

---

---

## 📱 15. Performance Optimization

Mobile users expect fast, smooth apps with minimal resource usage.

### Parameters:

| Parameter | Options | Impact |
|-----------|---------|--------|
| **App Size** | Unrestricted / <50MB / <25MB / <10MB | Smaller = better downloads |
| **Launch Time** | Unrestricted / <3 seconds / <2 seconds / <1 second | Cold start optimization |
| **Frame Rate** | 30fps / 60fps / 120fps (ProMotion) | 60fps is standard target |
| **Memory Management** | Basic / Optimized / Aggressive (low-memory devices) | $200–$1,000 |
| **Battery Optimization** | Basic / Location optimization / Full battery profiling | $200–$1,000 |
| **Network Optimization** | None / Request batching / Compression / Caching | $200–$1,000 |
| **Image Optimization** | None / Lazy loading / Progressive / WebP/AVIF | $200–$600 |
| **List/Scroll Performance** | Basic / Virtualized / Pagination (infinite scroll) | $200–$800 |
| **Build Size Optimization** | None / Tree-shaking / Code splitting / Asset optimization | $200–$800 |
| **Startup Optimization** | None / Deferred initialization / Splash screen preloading | $200–$500 |
| **ANR/Freeze Prevention** | Basic / Background threading / Isolate heavy computations | $200–$800 |

---

---

## 📱 16. Analytics & Monitoring

Understanding user behavior and app health is critical for success.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Analytics Platform** | None / Firebase Analytics / Mixpanel / Amplitude / CleverTap | $0–$500+/month |
| **Crash Reporting** | None / Firebase Crashlytics / Sentry / Bugsnag | $0–$100+/month |
| **Event Tracking** | None / Basic (screen views, clicks) / Advanced (funnels, user properties) | $300–$1,500 |
| **User Properties** | None / Basic demographics / Custom properties | $200–$500 |
| **Funnel Analysis** | None / Registration funnel / Purchase funnel / Custom | $200–$800 |
| **Retention Tracking** | None / D1/D7/D30 / Cohort analysis | $200–$500 |
| **A/B Testing** | None / Firebase Remote Config / Optimizely / LaunchDarkly | $0–$200+/month |
| **Feature Flags** | None / Basic toggles / Full feature management | $200–$1,000 |
| **Performance Monitoring** | None / Firebase Performance / New Relic / Datadog | $0–$300+/month |
| **User Session Recording** | None / Smartlook / LogRocket / UXCam | $0–$200+/month |
| **Heatmaps** | None / Touch heatmaps / Scroll maps | $0–$100+/month |
| **Revenue Analytics** | None / Basic / RevenueCat / Custom dashboard | $200–$1,000 |
| **Push Notification Analytics** | None / Open rate / Full funnel | Built into notification service |
| **Custom Dashboard** | None / Admin web dashboard / In-app analytics | $1,000–$5,000 |

### Analytics Service Comparison:

| Service | Free Tier | Paid Starting | Best For |
|---------|-----------|--------------|----------|
| **Firebase Analytics** | Unlimited | Free | Basic analytics, Google ecosystem |
| **Mixpanel** | 20M events/mo | $20/mo | Event-based analytics, funnels |
| **Amplitude** | 10M events/mo | $49/mo | Product analytics, retention |
| **CleverTap** | Limited | Custom pricing | Marketing automation + analytics |
| **PostHog** | 1M events/mo | $0 (self-hosted) | Open-source, feature flags |

---

---

## 📱 19. Legal, Compliance & App Store Policies

Mobile apps have strict store policies and legal requirements.

### Parameters:

| Parameter | Options | Pricing Impact |
|-----------|---------|---------------|
| **Privacy Policy** | Template / Custom / Lawyer-reviewed | $100–$1,000 |
| **Terms of Service** | Template / Custom / Lawyer-reviewed | $100–$1,000 |
| **GDPR Compliance** | Not applicable / Basic / Full | $500–$5,000 |
| **CCPA Compliance** | Not applicable / Basic / Full | $500–$3,000 |
| **COPPA (Children's data)** | Not applicable / Compliant | $500–$3,000 |
| **HIPAA (Health data)** | Not applicable / Compliant | $5,000–$20,000 |
| **App Tracking Transparency (iOS)** | Not needed / ATT prompt implementation | $200–$500 |
| **Data Safety (Google Play)** | Required form completion | $100–$300 |
| **App Privacy (Apple)** | Required privacy labels | $100–$300 |
| **Account Deletion** | Required (App Store policy since 2022) | Must be implemented |
| **Content Moderation** | Not needed / Manual review / Automated | $500–$5,000 |
| **User-Generated Content Policy** | Not applicable / Terms + reporting | $200–$1,000 |
| **Export Compliance** | Standard / Uses encryption (requires declaration) | Declaration in store |
| **Intellectual Property** | Client owns all / Shared / Developer retains framework | Define in contract |
| **NDA** | Not needed / Mutual NDA | Standard practice |
| **Source Code Escrow** | Not needed / Yes | $500–$2,000/year |
| **Open Source Licenses** | Audit required / Not important | License audit $200–$500 |

### Common App Store Rejection Reasons:

| Reason | How to Avoid |
|--------|-------------|
| **Bugs and crashes** | Thorough testing on real devices |
| **Broken links** | Test all URLs before submission |
| **Guideline 2.1 - Performance** | No placeholder content, all features must work |
| **Guideline 4.2 - Minimum Functionality** | App must provide sufficient value (no thin wrappers) |
| **Guideline 5.1.1 - Data Collection** | Proper privacy policy, data handling disclosure |
| **Guideline 3.1.1 - In-App Purchase** | Digital goods must use IAP (Apple/Google) |
| **Missing account deletion** | Implement account deletion feature |
| **Insufficient metadata** | Complete descriptions, screenshots, privacy info |

---

---
