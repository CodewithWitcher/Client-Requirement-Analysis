# 🔍 Complete SEO Framework & Tech Stack Guide (2026)

> A comprehensive reference for developers and teams choosing the right technology stack for SEO-optimized websites.

---

## 📋 Table of Contents

1. [SEO Scoring Criteria](#seo-scoring-criteria)
2. [Frontend Frameworks](#frontend-frameworks)
3. [Backend Frameworks](#backend-frameworks)
4. [Databases](#databases)
5. [CMS Platforms](#cms-platforms)
6. [Hosting & Deployment](#hosting--deployment)
7. [CDN & Performance](#cdn--performance)
8. [Search & Indexing Tools](#search--indexing-tools)
9. [Complete Tech Stacks](#complete-tech-stacks)
10. [SEO Tooling Ecosystem](#seo-tooling-ecosystem)
11. [Quick Reference Table](#quick-reference-table)

---

## SEO Scoring Criteria

Each framework/tool is rated on:

| Factor | Description |
|---|---|
| **Rendering** | SSR / SSG / CSR support |
| **Speed** | Core Web Vitals (LCP, CLS, INP) |
| **Crawlability** | How easily bots can index content |
| **Meta Control** | Ease of managing title, description, OG tags |
| **Structured Data** | Schema.org / JSON-LD support |
| **Sitemap** | Auto sitemap & robots.txt generation |
| **Ecosystem** | SEO plugins, libraries, integrations |

---

## Frontend Frameworks

### 🏆 BEST for SEO

---

#### 1. Next.js (React-based)
**SEO Score: 10/10**

```
Rendering:       SSR + SSG + ISR + CSR
Speed:           ⚡⚡⚡⚡⚡ Excellent
Crawlability:    ✅ Full HTML delivered to bots
Meta Control:    ✅ next/head or App Router metadata API
Sitemap:         ✅ next-sitemap / built-in App Router
```

**Why it's the best:**
- Full Server-Side Rendering ensures content is in raw HTML
- Incremental Static Regeneration (ISR) keeps content fresh without full rebuilds
- App Router (Next.js 13+) has a built-in `metadata` API for SEO
- Image optimization via `next/image` improves LCP scores
- Middleware for redirects, canonical URLs, and geolocation
- Massive ecosystem with thousands of SEO-friendly packages

**Best for:** E-commerce, SaaS marketing sites, news portals, large content platforms

---

#### 2. Astro
**SEO Score: 10/10**

```
Rendering:       SSG (default) + SSR (optional) + Island Architecture
Speed:           ⚡⚡⚡⚡⚡ Blazing fast (zero JS by default)
Crawlability:    ✅ Pure HTML output
Meta Control:    ✅ Full control via frontmatter & layouts
Sitemap:         ✅ @astrojs/sitemap integration
```

**Why it's exceptional:**
- Ships **zero JavaScript** by default — pure HTML output
- Islands Architecture only hydrates interactive components
- Fastest Core Web Vitals scores of any framework
- Framework-agnostic: use React, Vue, Svelte components inside Astro
- Perfect Lighthouse scores are achievable out-of-the-box

**Best for:** Blogs, documentation sites, portfolios, landing pages, content-heavy sites

---

#### 3. Nuxt.js (Vue-based)
**SEO Score: 9/10**

```
Rendering:       SSR + SSG + Hybrid
Speed:           ⚡⚡⚡⚡ Very Good
Crawlability:    ✅ Full HTML on SSR mode
Meta Control:    ✅ useHead() composable, nuxt/seo module
Sitemap:         ✅ @nuxtjs/sitemap
```

**Why it's great:**
- Nuxt SEO module bundles sitemap, robots, OG image generation
- `useHead()` provides reactive meta tag management
- Excellent Vue ecosystem for content sites
- Auto-imports reduce bundle size

**Best for:** Vue-based marketing sites, multilingual sites, content portals

---

#### 4. SvelteKit
**SEO Score: 9/10**

```
Rendering:       SSR + SSG + SPA
Speed:           ⚡⚡⚡⚡⚡ Excellent (smallest runtime)
Crawlability:    ✅ SSR delivers full HTML
Meta Control:    ✅ svelte:head for meta tags
Sitemap:         ✅ via svelte-sitemap
```

**Why it stands out:**
- Svelte compiles to vanilla JS — no virtual DOM overhead
- Smallest JavaScript bundle sizes among major frameworks
- Excellent for performance-first SEO

**Best for:** Fast marketing sites, blogs, lightweight web apps

---

#### 5. Remix (React-based)
**SEO Score: 9/10**

```
Rendering:       SSR-first (no SSG, but ISR-like caching)
Speed:           ⚡⚡⚡⚡ Great with proper caching
Crawlability:    ✅ Always server-rendered
Meta Control:    ✅ meta export per route
Sitemap:         ⚠️ Manual or third-party
```

**Why it's strong:**
- Every route is server-rendered by default
- Excellent `<meta>` exports per route
- Progressive enhancement improves UX signals (bounce rate, dwell time)

**Best for:** Web apps needing strong SEO, authenticated content sites

---

### ✅ GOOD for SEO

---

#### 6. Gatsby (React-based)
**SEO Score: 7/10**

```
Rendering:       SSG (primary) + DSG + SSR (limited)
Speed:           ⚡⚡⚡⚡ Good on static output
Crawlability:    ✅ Static HTML by default
Meta Control:    ✅ gatsby-plugin-react-helmet
Sitemap:         ✅ gatsby-plugin-sitemap
```

**Strengths:** Great plugin ecosystem, mature SEO tooling
**Weaknesses:** Slower build times, declining community adoption, complex data layer (GraphQL)

**Best for:** Small-to-medium blogs, portfolio sites, legacy projects

---

#### 7. WordPress (PHP + Themes)
**SEO Score: 7/10**

```
Rendering:       Server-rendered PHP (SSR equivalent)
Speed:           ⚡⚡ Varies (caching required)
Crawlability:    ✅ Full HTML output
Meta Control:    ✅ Yoast SEO / RankMath plugins
Sitemap:         ✅ Auto-generated by plugins
```

**Strengths:** World's most mature SEO plugin ecosystem, easiest for non-developers, huge community
**Weaknesses:** Slow without heavy optimization, security vulnerabilities, tech debt

**Best for:** Blogs, small business sites, news sites, beginners

---

#### 8. Hugo (Go-based Static Site Generator)
**SEO Score: 8/10**

```
Rendering:       SSG only
Speed:           ⚡⚡⚡⚡⚡ Fastest build times
Crawlability:    ✅ Pure static HTML
Meta Control:    ✅ Full template control
Sitemap:         ✅ Built-in sitemap generation
```

**Strengths:** Fastest builds (thousands of pages in seconds), lightweight output
**Weaknesses:** Go templating has steep learning curve, no client-side interactivity

**Best for:** Documentation, technical blogs, government/enterprise static sites

---

#### 9. Jekyll (Ruby-based)
**SEO Score: 7/10**

```
Rendering:       SSG only
Speed:           ⚡⚡⚡ Good
Crawlability:    ✅ Static HTML
Meta Control:    ✅ Via plugins and layouts
Sitemap:         ✅ jekyll-sitemap plugin
```

**Strengths:** Simple, battle-tested, GitHub Pages native support
**Weaknesses:** Slow builds for large sites, Ruby dependency, aging ecosystem

**Best for:** Developer blogs, documentation, open-source project sites

---

#### 10. Eleventy / 11ty (JavaScript)
**SEO Score: 8/10**

```
Rendering:       SSG
Speed:           ⚡⚡⚡⚡ Very fast builds
Crawlability:    ✅ Pure HTML
Meta Control:    ✅ Full control via templates
Sitemap:         ✅ eleventy-plugin-sitemap
```

**Strengths:** Zero client-side JS, flexible templating (Nunjucks, Liquid, JS), great Lighthouse scores
**Weaknesses:** Smaller ecosystem, less opinionated (can be overwhelming)

**Best for:** Performance-obsessed blogs, agency sites, JAMstack projects

---

### ❌ WORST for SEO

---

#### 11. Create React App (CRA)
**SEO Score: 2/10**

```
Rendering:       CSR only (Client-Side Rendering)
Speed:           ⚡ Poor initial load
Crawlability:    ❌ Googlebot sees empty HTML shell
Meta Control:    ❌ Tags rendered by JS (may not be crawled)
Sitemap:         ❌ Manual only
```

**Why it's bad:** The HTML delivered to crawlers is essentially empty — all content is rendered by JavaScript in the browser. While Googlebot can execute JS, it's unreliable and delayed.

---

#### 12. Plain Angular (without Angular Universal)
**SEO Score: 2/10**

```
Rendering:       CSR only
Speed:           ⚡ Heavy initial bundle
Crawlability:    ❌ JS-rendered content
Meta Control:    ❌ Unreliable for crawlers
Sitemap:         ❌ Manual
```

**Fix:** Use **Angular Universal** (SSR) to make it SEO-friendly.

---

#### 13. Plain Vue 3 (without Nuxt)
**SEO Score: 2/10**

```
Rendering:       CSR only
Speed:           ⚡⚡ Moderate
Crawlability:    ❌ JS-rendered content
Meta Control:    ❌ Dynamic, bot-unfriendly
Sitemap:         ❌ Manual
```

**Fix:** Use **Nuxt.js** for SSR/SSG support.

---

#### 14. Plain React (without Next.js/Remix)
**SEO Score: 2/10**

```
Rendering:       CSR only
Speed:           ⚡ Poor without optimization
Crawlability:    ❌ JS-rendered
Meta Control:    ❌ React Helmet works, but content still JS-rendered
Sitemap:         ❌ Manual
```

**Fix:** Use **Next.js** or **Remix**.

---

#### 15. Backbone.js / Ember.js / Knockout.js
**SEO Score: 1/10**

```
Rendering:       CSR only (legacy frameworks)
Speed:           ⚡ Poor
Crawlability:    ❌ Virtually zero
Meta Control:    ❌ None
Sitemap:         ❌ None
```

**Why:** These older SPA frameworks have no modern SSR support. Avoid entirely for public-facing SEO sites.

---

## Backend Frameworks

### 🏆 BEST for SEO

| Framework | Language | SSR Support | Speed | SEO Fit |
|---|---|---|---|---|
| **Node.js + Express** | JavaScript | ✅ Manual SSR | ⚡⚡⚡⚡ | Excellent with Next.js/Nuxt |
| **Django** | Python | ✅ Native template rendering | ⚡⚡⚡ | Excellent |
| **Laravel** | PHP | ✅ Blade templates | ⚡⚡⚡ | Excellent |
| **Ruby on Rails** | Ruby | ✅ ERB templates | ⚡⚡⚡ | Very Good |
| **Fastify** | JavaScript | ✅ SSR capable | ⚡⚡⚡⚡⚡ | Excellent |

### ✅ GOOD for SEO

| Framework | Language | SSR Support | Speed | SEO Fit |
|---|---|---|---|---|
| **Spring Boot** | Java | ✅ Thymeleaf templates | ⚡⚡⚡ | Good |
| **ASP.NET Core** | C# | ✅ Razor Pages | ⚡⚡⚡⚡ | Good |
| **Flask** | Python | ✅ Jinja2 templates | ⚡⚡⚡ | Good |
| **Phoenix** | Elixir | ✅ HEEx templates | ⚡⚡⚡⚡ | Good |
| **NestJS** | TypeScript | ✅ With SSR adapters | ⚡⚡⚡⚡ | Good |

### ❌ WORST for SEO (API-only, no rendering)

| Framework | Language | Note |
|---|---|---|
| **FastAPI** | Python | API only — no HTML rendering |
| **GraphQL servers** | Various | Data layer only, no rendering |
| **Supabase Edge Functions** | Deno/JS | API only |
| **Serverless functions only** | Various | Needs frontend for rendering |

---

## Databases

> Databases don't directly impact SEO, but affect **page speed** (Core Web Vitals) and **content freshness** — both SEO ranking factors.

### 🏆 BEST for SEO-Driven Sites

| Database | Type | Speed | Use Case |
|---|---|---|---|
| **PostgreSQL** | Relational SQL | ⚡⚡⚡⚡ | Full-text search, structured content |
| **MySQL / MariaDB** | Relational SQL | ⚡⚡⚡⚡ | WordPress, e-commerce, blogs |
| **SQLite** | Embedded SQL | ⚡⚡⚡⚡⚡ | Small sites, static-adjacent |
| **PlanetScale** | MySQL-compatible | ⚡⚡⚡⚡⚡ | Scalable, serverless MySQL |

### ✅ GOOD for SEO-Driven Sites

| Database | Type | Speed | Use Case |
|---|---|---|---|
| **MongoDB** | NoSQL Document | ⚡⚡⚡⚡ | Flexible content schemas, headless CMS |
| **Supabase** | PostgreSQL-as-a-service | ⚡⚡⚡⚡ | Modern Postgres with realtime |
| **Firebase Firestore** | NoSQL | ⚡⚡⚡ | Rapid prototyping (watch bundle size) |
| **Redis** | In-memory cache | ⚡⚡⚡⚡⚡ | Caching layer — improves TTFB |
| **Turso (libSQL)** | SQLite edge | ⚡⚡⚡⚡⚡ | Edge-distributed, ultra-low latency |

### ⚠️ USE WITH CAUTION

| Database | Issue |
|---|---|
| **DynamoDB** | High latency queries can slow pages |
| **CouchDB** | Slower queries, niche use case |
| **Neo4j** | Graph DB — not optimized for web content |

---

## CMS Platforms

### 🏆 BEST Headless CMS (for SEO + Modern Stack)

| CMS | Type | SEO Features | Best Pairing |
|---|---|---|---|
| **Sanity** | Headless | Custom previews, structured data | Next.js, Nuxt |
| **Contentful** | Headless | SEO fields, rich APIs | Next.js, Astro |
| **Strapi** | Self-hosted Headless | Full control, REST + GraphQL | Next.js, Nuxt |
| **Payload CMS** | Code-first Headless | Full TypeScript, flexible | Next.js |
| **Directus** | Data platform | REST/GraphQL, SEO-ready | Any frontend |

### ✅ GOOD Traditional CMS

| CMS | Type | SEO Features | Note |
|---|---|---|---|
| **WordPress** | Monolithic | Yoast, RankMath, sitemaps | Best plugin ecosystem |
| **Ghost** | Publishing | Built-in SEO, sitemaps, AMP | Great for blogs |
| **Drupal** | Monolithic | Metatag module, path aliases | Enterprise use |
| **Joomla** | Monolithic | SEO metadata, sitemaps | Declining community |

### ❌ WORST CMS for SEO

| CMS | Issue |
|---|---|
| **Wix (old)** | Poor rendering, limited control |
| **Squarespace** | Limited meta control, slow |
| **Webflow** | Good but limited programmatic SEO |
| **Weebly** | Outdated, poor technical SEO |

---

## Hosting & Deployment

### 🏆 BEST for SEO Performance

| Platform | Edge Network | TTFB | Free Tier | Best For |
|---|---|---|---|---|
| **Vercel** | Global Edge | ⚡⚡⚡⚡⚡ | ✅ Yes | Next.js, Astro, React |
| **Netlify** | Global CDN | ⚡⚡⚡⚡ | ✅ Yes | JAMstack, static sites |
| **Cloudflare Pages** | 300+ PoPs | ⚡⚡⚡⚡⚡ | ✅ Yes | Any framework |
| **AWS (CloudFront + S3)** | Global | ⚡⚡⚡⚡⚡ | ❌ Paid | Enterprise, full control |
| **Google Cloud Run** | Global | ⚡⚡⚡⚡ | ❌ Paid | Containerized apps |

### ✅ GOOD Hosting

| Platform | TTFB | Best For |
|---|---|---|
| **Railway** | ⚡⚡⚡ | Full-stack Node/Python apps |
| **Render** | ⚡⚡⚡ | Full-stack with databases |
| **DigitalOcean App Platform** | ⚡⚡⚡ | Docker, static, and server apps |
| **Fly.io** | ⚡⚡⚡⚡ | Edge computing, global deploys |

### ❌ WORST for SEO (Slow or Limited)

| Platform | Issue |
|---|---|
| **Shared cPanel hosting** | Slow TTFB, no edge, poor Core Web Vitals |
| **Heroku (free tier)** | Cold starts kill TTFB |
| **GitHub Pages (no CDN)** | No edge, no SSR support |
| **000webhost / free hosts** | Extremely slow, unreliable uptime |

---

## CDN & Performance

### 🏆 BEST CDN for SEO

| CDN | Edge Locations | Features | Cost |
|---|---|---|---|
| **Cloudflare** | 300+ cities | DDoS, Workers, image optimization | Free tier available |
| **AWS CloudFront** | 400+ PoPs | Lambda@Edge, signed URLs | Pay per use |
| **Fastly** | 90+ PoPs | Real-time purging, VCL | Enterprise |
| **Bunny CDN** | 114 PoPs | Affordable, fast | Very cheap |

### Performance Tools (SEO Critical)

| Tool | Purpose | Impact on SEO |
|---|---|---|
| **Cloudflare Image Resizing** | Optimize images on-the-fly | LCP improvement |
| **imgix / Cloudinary** | Image CDN + transformation | LCP, bandwidth |
| **Redis / Upstash** | Server-side caching | TTFB reduction |
| **Varnish Cache** | HTTP accelerator | TTFB, server load |

---

## Search & Indexing Tools

| Tool | Purpose | SEO Benefit |
|---|---|---|
| **Algolia** | Search-as-a-service | UX → lower bounce rate |
| **Meilisearch** | Self-hosted search | Fast, typo-tolerant |
| **Elasticsearch** | Full-text search | Content discoverability |
| **Typesense** | Open-source search | Lightweight alternative to Algolia |

---

## Complete Tech Stacks

### Stack 1: 🏆 Ultimate SEO Stack (Enterprise)

```
Frontend:    Next.js 15 (App Router + SSR/SSG/ISR)
Backend:     Node.js + Fastify (API routes)
Database:    PostgreSQL (via Supabase or Neon)
CMS:         Sanity (Headless)
Cache:       Redis (Upstash - serverless)
CDN:         Cloudflare (with Image Optimization)
Hosting:     Vercel (Edge Network)
Search:      Algolia
Auth:        NextAuth.js / Clerk
Analytics:   Google Analytics 4 + Vercel Analytics
SEO Tools:   next-sitemap, next-seo, Schema.org JSON-LD
Monitoring:  Sentry + Vercel Speed Insights
```

**Best for:** News portals, large e-commerce, SaaS marketing sites

---

### Stack 2: 🏆 Content-First SEO Stack (Blogs / Docs)

```
Frontend:    Astro 5 (Islands Architecture)
Backend:     Astro server endpoints (Deno/Node)
Database:    SQLite (Turso for edge)
CMS:         Markdown / MDX files or Contentful
Cache:       Built-in static generation
CDN:         Cloudflare Pages
Hosting:     Cloudflare Pages (free)
Search:      Pagefind (local static search)
Analytics:   Plausible (privacy-friendly)
SEO Tools:   @astrojs/sitemap, custom JSON-LD
```

**Best for:** Developer blogs, documentation, portfolios, landing pages

---

### Stack 3: ✅ Vue/Nuxt SEO Stack (Mid-size)

```
Frontend:    Nuxt 3 (SSR + SSG hybrid)
Backend:     Nitro server (built into Nuxt)
Database:    MySQL (PlanetScale serverless)
CMS:         Strapi (self-hosted headless)
Cache:       Redis
CDN:         Cloudflare
Hosting:     Netlify or Render
Search:      Meilisearch
Auth:        Nuxt Auth
Analytics:   Fathom Analytics
SEO Tools:   @nuxtjs/seo (sitemap + robots + og-image)
```

**Best for:** Vue teams, multilingual sites, marketing platforms

---

### Stack 4: ✅ Traditional SEO Stack (Small Business / Blog)

```
Frontend:    WordPress (PHP + theme)
Backend:     PHP 8.x + WordPress core
Database:    MySQL 8
CMS:         WordPress (built-in)
Cache:       WP Rocket + Redis Object Cache
CDN:         Cloudflare (free plan)
Hosting:     SiteGround / WP Engine / Kinsta
Search:      ElasticPress + Elasticsearch
Auth:        WordPress native
Analytics:   MonsterInsights (GA4)
SEO Tools:   Yoast SEO / RankMath + All in One SEO
```

**Best for:** Bloggers, small business sites, news sites, non-developers

---

### Stack 5: ✅ Svelte SEO Stack (Performance-Obsessed)

```
Frontend:    SvelteKit (SSR + SSG)
Backend:     SvelteKit server routes
Database:    PostgreSQL (Neon serverless)
CMS:         Directus (self-hosted)
Cache:       Edge caching via Cloudflare
CDN:         Cloudflare
Hosting:     Vercel or Cloudflare Pages
Search:      Typesense
Auth:        Lucia Auth
Analytics:   Plausible
SEO Tools:   svelte-meta-tags, custom sitemap endpoint
```

**Best for:** Startups, developer portfolios, high-performance marketing sites

---

### Stack 6: ❌ Avoid for SEO (Anti-Pattern)

```
Frontend:    Create React App (CSR only)
Backend:     Express.js (API only, no SSR)
Database:    MongoDB (unoptimized queries)
CMS:         None (hardcoded content)
Cache:       None
CDN:         None (direct server)
Hosting:     Heroku (free tier, cold starts)
Search:      None
```

**Problem:** Content is never in raw HTML → crawlers see empty pages → zero organic traffic

---

## SEO Tooling Ecosystem

### Meta & Structured Data

| Tool | Framework | Purpose |
|---|---|---|
| **next-seo** | Next.js | Meta tags, OG, JSON-LD |
| **next-sitemap** | Next.js | Sitemap + robots.txt |
| **nuxt/seo** | Nuxt.js | All-in-one SEO module |
| **react-helmet** | React | Dynamic head management |
| **svelte-meta-tags** | SvelteKit | Meta tag management |
| **schema-dts** | Any (TypeScript) | Type-safe Schema.org |

### Analytics & Monitoring

| Tool | Type | Privacy |
|---|---|---|
| **Google Analytics 4** | Full analytics | ⚠️ Not privacy-first |
| **Plausible** | Lightweight analytics | ✅ Privacy-friendly |
| **Fathom** | Simple analytics | ✅ GDPR compliant |
| **Umami** | Self-hosted analytics | ✅ Full data ownership |
| **Vercel Analytics** | Core Web Vitals | ✅ Privacy-first |

### SEO Auditing Tools

| Tool | Use Case |
|---|---|
| **Google Search Console** | Index status, queries, errors |
| **Ahrefs** | Backlinks, keyword tracking |
| **SEMrush** | Full SEO suite |
| **Screaming Frog** | Site crawl audit |
| **Lighthouse (Chrome)** | Core Web Vitals, performance |
| **PageSpeed Insights** | Real-world performance data |
| **Schema Markup Validator** | Validate structured data |

---

## Quick Reference Table

### Frontend Frameworks Summary

| Framework | SEO Rating | Rendering | Speed | Difficulty | Verdict |
|---|---|---|---|---|---|
| **Next.js** | ⭐⭐⭐⭐⭐ | SSR+SSG+ISR | ⚡⚡⚡⚡⚡ | Medium | 🏆 Best Overall |
| **Astro** | ⭐⭐⭐⭐⭐ | SSG+SSR | ⚡⚡⚡⚡⚡ | Easy | 🏆 Best for Content |
| **Nuxt.js** | ⭐⭐⭐⭐½ | SSR+SSG | ⚡⚡⚡⚡ | Medium | 🏆 Best Vue Option |
| **SvelteKit** | ⭐⭐⭐⭐½ | SSR+SSG | ⚡⚡⚡⚡⚡ | Medium | ✅ Great Performance |
| **Remix** | ⭐⭐⭐⭐ | SSR | ⚡⚡⚡⚡ | Medium | ✅ Strong SSR |
| **Gatsby** | ⭐⭐⭐½ | SSG | ⚡⚡⚡⚡ | Medium | ✅ Aging but Solid |
| **Hugo** | ⭐⭐⭐⭐ | SSG | ⚡⚡⚡⚡⚡ | Hard | ✅ Fast Builds |
| **Eleventy** | ⭐⭐⭐⭐ | SSG | ⚡⚡⚡⚡ | Medium | ✅ Flexible |
| **WordPress** | ⭐⭐⭐ | PHP SSR | ⚡⚡ | Easy | ✅ Best for Non-Devs |
| **Jekyll** | ⭐⭐⭐ | SSG | ⚡⚡⚡ | Easy | ✅ Simple Blogs |
| **CRA (React)** | ⭐ | CSR only | ⚡ | Easy | ❌ Avoid |
| **Plain Angular** | ⭐ | CSR only | ⚡⚡ | Hard | ❌ Avoid |
| **Plain Vue** | ⭐ | CSR only | ⚡⚡ | Easy | ❌ Avoid |
| **Plain React** | ⭐ | CSR only | ⚡ | Easy | ❌ Avoid |
| **Backbone/Ember** | ⭐ | CSR only | ⚡ | Hard | ❌ Never Use |

---

## Final Recommendations

### By Use Case

| Use Case | Recommended Stack |
|---|---|
| **Large E-commerce** | Next.js + PostgreSQL + Sanity + Vercel + Cloudflare |
| **News / Media Portal** | Next.js (ISR) + MySQL + Strapi + AWS CloudFront |
| **Developer Blog** | Astro + MDX + Cloudflare Pages |
| **Documentation Site** | Astro or Docusaurus + GitHub Pages |
| **Small Business Site** | WordPress + WP Rocket + Cloudflare |
| **Marketing / Landing** | Astro or SvelteKit + Cloudflare Pages |
| **SaaS Marketing** | Next.js + Contentful + Vercel |
| **Portfolio** | Astro or SvelteKit (static) |
| **Multilingual Site** | Nuxt.js + i18n module + Netlify |
| **High-traffic Blog** | Next.js (SSG/ISR) + Ghost CMS + Vercel |

---

> **Last Updated:** 2026 | Based on Google's current ranking signals, Core Web Vitals criteria, and framework capabilities.
>
> 💡 **Key Takeaway:** The single most important SEO decision is choosing **SSR or SSG** over **CSR**. Content must be in raw HTML before JavaScript executes. Everything else is optimization.
