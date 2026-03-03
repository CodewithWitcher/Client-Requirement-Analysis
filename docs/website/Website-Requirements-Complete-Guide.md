# 🌐 Website Requirements — Complete Guide

> This is the master reference document for every parameter you need to discuss, evaluate, and price when building a website for a client. Use this guide during discovery calls and proposal preparation.

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

## 1. Domain

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

## 2. Hosting

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

## 3. SSL Certificate & Security

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

## 4. Database

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

## 5. Tech Stack

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

## 6. Design & User Experience

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

## 7. Pages & Site Structure

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

## 8. Features & Functionality

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

## 9. E-Commerce

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

## 10. Payment Integration

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

## 11. Content Management

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

## 12. SEO & Analytics

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

## 13. Performance & Traffic

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

## 14. Security & Compliance

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

## 15. Third-Party Integrations

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

## 17. Timeline, Milestones & Release

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

## 18. Legal & Compliance

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

## 19. Branding & Assets

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

## 20. Communication & Project Management

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

## 📊 Quick Price Estimation Formula

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
