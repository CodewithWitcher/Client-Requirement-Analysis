# ✅ Mobile Application Project Checklist

> **Purpose:** A step-by-step checklist to follow throughout the entire mobile app project lifecycle. Use this to ensure nothing is missed from initial contact to post-launch support.

---

## Phase 1: Pre-Project (Discovery & Planning)

### 1.1 Client Discovery
- [ ] Initial client meeting/call completed
- [ ] Client Questionnaire filled out
- [ ] App purpose and goals documented
- [ ] Target audience identified (age, geography, behavior)
- [ ] Competitor apps analyzed (features, ratings, reviews)
- [ ] Client's existing assets collected (logo, brand, API docs)
- [ ] Reference/inspiration apps reviewed with client
- [ ] Monetization strategy discussed

### 1.2 Requirements Documentation
- [ ] All screens/flows listed with descriptions
- [ ] All features and functionalities listed with priority
- [ ] Platform decided (Android / iOS / Both)
- [ ] Development approach decided (Native / Flutter / React Native)
- [ ] Backend approach decided (Custom / Firebase / Supabase / etc.)
- [ ] Authentication methods decided
- [ ] Third-party integrations identified
- [ ] Payment requirements documented (if applicable)
- [ ] Push notification requirements documented
- [ ] Offline requirements documented
- [ ] Device feature requirements (Camera, GPS, Bluetooth, etc.)
- [ ] Security and compliance requirements noted
- [ ] Multi-language requirements noted
- [ ] Accessibility requirements noted

### 1.3 Project Scope & Quotation
- [ ] Pricing calculation completed (use Pricing Parameters sheet)
- [ ] MVP vs Full scope decided
- [ ] Feature roadmap created (Phase 1, Phase 2, etc.)
- [ ] Project scope document prepared
- [ ] Timeline with milestones created
- [ ] Quotation / Proposal sent to client
- [ ] Quotation approved by client
- [ ] Payment terms agreed upon
- [ ] Advance payment received
- [ ] Contract / Agreement signed
- [ ] NDA signed (if required)
- [ ] Project start date confirmed

---

## Phase 2: Setup & Infrastructure

### 2.1 App Store Accounts
- [ ] Google Play Developer account ready ($25 one-time)
- [ ] Apple Developer account ready ($99/year)
- [ ] Account ownership decided (Client / Developer)
- [ ] Team members added to accounts (if needed)
- [ ] App ID / Bundle ID reserved
- [ ] Signing certificates generated
- [ ] Provisioning profiles created (iOS)
- [ ] Keystore created (Android)

### 2.2 Development Environment
- [ ] Git repository created
- [ ] Branch strategy decided (main, develop, feature branches)
- [ ] Flutter/React Native/Native project initialized
- [ ] Project structure set up (folders, packages)
- [ ] Code formatting & linting rules set up
- [ ] CI/CD pipeline configured (GitHub Actions / Fastlane / Codemagic)
- [ ] Automated build setup for Android
- [ ] Automated build setup for iOS
- [ ] Project management tool set up (Trello, Jira, Notion)
- [ ] Communication channel set up (Slack, WhatsApp)
- [ ] File sharing set up (Google Drive, Figma links)

### 2.3 Backend & Database Setup
- [ ] Backend project initialized / Firebase project created
- [ ] Database set up and configured
- [ ] Database schema / collections designed
- [ ] Cloud storage configured (S3 / Firebase Storage / etc.)
- [ ] API framework set up (Express, FastAPI, etc.)
- [ ] Authentication service configured
- [ ] Environment variables configured
- [ ] Staging / development server deployed
- [ ] API testing tool set up (Postman / Insomnia)

### 2.4 Third-Party Services
- [ ] Push notification service set up (FCM / OneSignal)
- [ ] Analytics service set up (Firebase Analytics / Mixpanel)
- [ ] Crash reporting set up (Crashlytics / Sentry)
- [ ] Payment gateway developer account created
- [ ] Maps API key obtained (if needed)
- [ ] SMS/Email service configured (Twilio / SendGrid)
- [ ] Other API keys obtained and documented

---

## Phase 3: Design

### 3.1 UI/UX Design
- [ ] User flows / User journeys mapped
- [ ] Information architecture created
- [ ] Wireframes created (low-fidelity)
- [ ] Wireframes approved by client
- [ ] High-fidelity mockups designed (Figma/XD)
- [ ] All screens designed for primary platform
- [ ] Screens adapted for secondary platform (if both)
- [ ] Tablet layouts designed (if needed)
- [ ] Dark mode designed (if needed)
- [ ] Interactive prototype created
- [ ] Prototype shared with client for review
- [ ] Design revisions completed
- [ ] Final design approved by client

### 3.2 App Assets
- [ ] App icon designed (all sizes)
- [ ] Splash screen designed
- [ ] Onboarding screens designed (if applicable)
- [ ] Empty state illustrations created
- [ ] Error state illustrations created
- [ ] Custom icons created (if needed)
- [ ] Lottie animations created (if applicable)
- [ ] App store screenshots designed
- [ ] App store feature graphic designed
- [ ] Design system / Component library documented

---

## Phase 4: Development

### 4.1 Core App Structure
- [ ] Navigation / Routing set up
- [ ] State management set up (Provider / Bloc / Redux / Riverpod)
- [ ] Theme / Styling system implemented (colors, fonts, spacing)
- [ ] Responsive layout utilities implemented
- [ ] Network layer / API client set up (Dio / Axios / http)
- [ ] Error handling framework implemented
- [ ] Local storage utility set up
- [ ] App configuration (dev/staging/prod environments)
- [ ] Dependency injection set up (if using)
- [ ] Localization/i18n framework set up (if multi-language)

### 4.2 Authentication
- [ ] Login screen implemented
- [ ] Registration screen implemented
- [ ] Email/Password auth working
- [ ] Phone/OTP auth working (if applicable)
- [ ] Google Sign-In working (if applicable)
- [ ] Apple Sign-In working (if applicable)
- [ ] Facebook Login working (if applicable)
- [ ] Biometric auth working (if applicable)
- [ ] Forgot password flow working
- [ ] Email/Phone verification working
- [ ] Session management / Token refresh working
- [ ] Auto-login (remember me) working
- [ ] Logout working
- [ ] Account deletion working (required by Apple)
- [ ] Guest mode working (if applicable)

### 4.3 Screen Development
- [ ] Splash screen implemented
- [ ] Onboarding screens implemented (if applicable)
- [ ] Home / Main screen implemented
- [ ] Profile screen implemented
- [ ] Settings screen implemented
- [ ] Search screen implemented
- [ ] Detail screens implemented
- [ ] List / Feed screens implemented
- [ ] Form screens implemented
- [ ] Chat screens implemented (if applicable)
- [ ] Cart / Checkout screens implemented (if applicable)
- [ ] Order tracking screens (if applicable)
- [ ] Notification center screen implemented
- [ ] All other screens implemented
- [ ] All screens handle loading states
- [ ] All screens handle error states
- [ ] All screens handle empty states
- [ ] Pull-to-refresh implemented where needed
- [ ] Infinite scroll / pagination implemented where needed

### 4.4 Backend Development
- [ ] User management API endpoints
- [ ] Authentication API endpoints
- [ ] Core business logic API endpoints
- [ ] File upload API endpoints
- [ ] Search API endpoints
- [ ] Notification API endpoints
- [ ] Payment API endpoints (if applicable)
- [ ] Admin API endpoints
- [ ] API input validation
- [ ] API error handling standardized
- [ ] API rate limiting
- [ ] API versioning
- [ ] API documentation (Swagger / Postman collection)
- [ ] Database indexes created for performance
- [ ] Background jobs / scheduled tasks (if needed)
- [ ] WebSocket / real-time endpoints (if applicable)

### 4.5 Features & Integrations
- [ ] Push notifications sending and receiving
- [ ] Push notification handling (foreground / background / terminated)
- [ ] Deep linking working
- [ ] In-app messaging / Chat working (if applicable)
- [ ] GPS / Location services working (if applicable)
- [ ] Maps integration working (if applicable)
- [ ] Camera integration working (if applicable)
- [ ] Gallery / Image picker working (if applicable)
- [ ] File picker / Document scanner working (if applicable)
- [ ] QR/Barcode scanner working (if applicable)
- [ ] Payment gateway integrated and tested (if applicable)
- [ ] In-app purchases configured (if applicable)
- [ ] Subscription management working (if applicable)
- [ ] Social sharing working (if applicable)
- [ ] Email/SMS service integrated
- [ ] Analytics events tracked
- [ ] Crash reporting working
- [ ] All third-party SDKs integrated
- [ ] Offline mode working (if applicable)
- [ ] Data sync working (if applicable)
- [ ] Background tasks working (if applicable)

### 4.6 Admin Panel (if applicable)
- [ ] Admin authentication
- [ ] Dashboard with key metrics
- [ ] User management (view, edit, ban)
- [ ] Content management
- [ ] Order management (if e-commerce)
- [ ] Push notification composer
- [ ] Analytics overview
- [ ] Report generation
- [ ] Settings / Configuration panel

---

## Phase 5: Testing

### 5.1 Unit & Integration Testing
- [ ] Unit tests written for critical business logic
- [ ] Unit tests written for state management
- [ ] API integration tests written
- [ ] Widget / UI tests written (if applicable)
- [ ] All tests passing
- [ ] Code coverage > 70% (target)

### 5.2 Manual Testing
- [ ] All screens manually tested
- [ ] All user flows tested end-to-end
- [ ] All forms tested (valid + invalid input)
- [ ] All buttons and CTAs working
- [ ] Navigation (forward, back, deep link) tested
- [ ] Login/Logout flow tested
- [ ] Payment flow tested (sandbox)
- [ ] Push notification tested (all states)
- [ ] Offline behavior tested
- [ ] Error scenarios tested (no network, server error, timeout)
- [ ] Edge cases tested (empty data, large data, special characters)
- [ ] Permissions tested (camera, location, contacts, etc.)
- [ ] App lifecycle tested (background, foreground, kill, resume)

### 5.3 Device Testing
- [ ] Android — Small phone (e.g., 5" screen)
- [ ] Android — Medium phone (e.g., 6" screen)
- [ ] Android — Large phone (e.g., 6.7" screen)
- [ ] Android — Tablet (if applicable)
- [ ] iOS — iPhone SE / Mini
- [ ] iOS — iPhone Standard (14/15/16)
- [ ] iOS — iPhone Pro Max
- [ ] iOS — iPad (if applicable)
- [ ] Different OS versions tested
- [ ] Notch / Dynamic Island / Punch-hole handling verified
- [ ] Landscape mode tested (if supported)
- [ ] Dark mode tested
- [ ] Accessibility tested (screen reader, font scaling)

### 5.4 Performance Testing
- [ ] App startup time < 3 seconds
- [ ] Screen transitions smooth (60fps)
- [ ] No memory leaks
- [ ] No excessive battery drain
- [ ] App size within acceptable limits
- [ ] API response times acceptable
- [ ] Large list / data scrolling smooth
- [ ] Image loading optimized (caching, placeholders)

### 5.5 Security Testing
- [ ] API endpoints require authentication
- [ ] Sensitive data encrypted in local storage
- [ ] No hardcoded secrets in code
- [ ] Certificate pinning working (if implemented)
- [ ] Session timeout working
- [ ] Jailbreak/Root detection working (if implemented)
- [ ] Input validation on both client and server
- [ ] No sensitive data in logs

### 5.6 Beta Testing
- [ ] Beta build created (TestFlight / Play Console Internal Testing)
- [ ] Beta testers identified and invited
- [ ] Beta test feedback collected
- [ ] Beta test issues resolved
- [ ] Beta feedback incorporated
- [ ] Final beta sign-off received

### 5.7 User Acceptance Testing (UAT)
- [ ] UAT build provided to client
- [ ] Test scenarios shared with client
- [ ] Client feedback collected
- [ ] UAT issues resolved
- [ ] Final UAT sign-off from client

---

## Phase 6: Pre-Launch Preparation

### 6.1 App Store Preparation — Google Play
- [ ] App title finalized
- [ ] Short description written (80 chars)
- [ ] Full description written (4000 chars)
- [ ] Category selected
- [ ] Privacy policy URL ready
- [ ] App icon uploaded (512×512)
- [ ] Feature graphic uploaded (1024×500)
- [ ] Screenshots uploaded (min 2 per device type)
- [ ] Content rating questionnaire completed
- [ ] Target audience and content settings configured
- [ ] Data safety section completed
- [ ] App pricing set (Free / Paid)
- [ ] In-app products configured (if applicable)
- [ ] Subscriptions configured (if applicable)
- [ ] App signing configured (Google Play App Signing)
- [ ] Release track selected (Internal / Closed / Open / Production)
- [ ] Release notes written

### 6.2 App Store Preparation — Apple App Store
- [ ] App name chosen and verified available
- [ ] Subtitle written (30 chars)
- [ ] Description written
- [ ] Keywords set (100 chars)
- [ ] Category selected
- [ ] Privacy policy URL ready
- [ ] App icon uploaded (1024×1024)
- [ ] Screenshots uploaded for all required device sizes
- [ ] App preview video uploaded (optional)
- [ ] Age rating set
- [ ] App privacy details completed (nutrition labels)
- [ ] In-app purchases configured (if applicable)
- [ ] Subscriptions configured (if applicable)
- [ ] App pricing set
- [ ] Review notes prepared (for Apple review team)
- [ ] Demo account credentials ready (for Apple reviewer)
- [ ] Contact information set
- [ ] What's New text written

### 6.3 Final Code Preparation
- [ ] All TODO/FIXME comments resolved
- [ ] All console.log / print statements removed
- [ ] Debug flags disabled
- [ ] Environment configured for production
- [ ] ProGuard / R8 rules configured (Android)
- [ ] App size optimized
- [ ] Code obfuscation enabled
- [ ] Version number and build number set
- [ ] Changelog documented
- [ ] Final code review completed
- [ ] Code merged to main/release branch

---

## Phase 7: Launch

### 7.1 Build & Submit
- [ ] Production build generated (Android — AAB)
- [ ] Production build generated (iOS — Archive)
- [ ] Build tested via TestFlight / Internal Testing
- [ ] Android app submitted to Google Play
- [ ] iOS app submitted to App Store Connect
- [ ] App review status monitored
- [ ] Review feedback addressed (if rejected)
- [ ] App approved
- [ ] Release date set / Published

### 7.2 Post-Submission
- [ ] App live and accessible on Play Store
- [ ] App live and accessible on App Store
- [ ] Download and install from store — verified working
- [ ] All features working on production
- [ ] Payments working in live mode
- [ ] Push notifications working
- [ ] Analytics receiving data
- [ ] Crash reporting active
- [ ] Backend / API performing well
- [ ] No critical bugs in first 24-48 hours

---

## Phase 8: Post-Launch

### 8.1 Monitoring (First 2 Weeks)
- [ ] Crash rate monitored daily
- [ ] App ratings and reviews monitored
- [ ] User metrics tracked (DAU, MAU, retention)
- [ ] Server / API performance monitored
- [ ] Error rates monitored
- [ ] User feedback collected
- [ ] Critical bugs fixed immediately
- [ ] Hotfix release pushed (if needed)

### 8.2 Handover
- [ ] All credentials shared securely with client
- [ ] App store account access provided / transferred
- [ ] Backend / server access provided
- [ ] Database access provided
- [ ] Firebase / Supabase project access provided
- [ ] Source code access provided (if agreed)
- [ ] Design files (Figma) access provided (if agreed)
- [ ] API documentation shared
- [ ] Third-party service credentials shared
- [ ] All API keys and service accounts documented
- [ ] Admin panel walkthrough / training completed
- [ ] User manual / documentation delivered
- [ ] Client has list of all services, logins, renewal dates

### 8.3 Final Payment & Closure
- [ ] Final payment received
- [ ] Invoice sent
- [ ] Client feedback collected
- [ ] Testimonial requested
- [ ] Project archived (code, docs, designs, credentials)
- [ ] Case study created (for portfolio)
- [ ] Maintenance plan agreed upon (if applicable)
- [ ] Warranty / support period communicated

### 8.4 Ongoing Maintenance (if applicable)
- [ ] Crash monitoring active
- [ ] Performance monitoring active
- [ ] OS update compatibility checked (new Android/iOS versions)
- [ ] Library / SDK updates scheduled
- [ ] Security patches applied promptly
- [ ] App store policy changes monitored
- [ ] User feedback reviewed regularly
- [ ] Analytics reports generated (monthly/quarterly)
- [ ] Feature updates planned and deployed
- [ ] App store listing updated for new features
- [ ] Server costs monitored and optimized
- [ ] Database maintained (cleanup, optimization)
- [ ] Backup verified regularly
- [ ] Support tickets responded to within SLA

---

## Quick Reference: Common App Rejection Reasons

### Google Play Rejections
| # | Reason | Prevention |
|---|--------|------------|
| 1 | Crashes or ANRs | Thorough testing on multiple devices |
| 2 | Privacy policy missing | Add URL before submission |
| 3 | Deceptive behavior | App must do what it claims |
| 4 | Permissions not justified | Only request necessary permissions |
| 5 | Data safety form incomplete | Fill accurately |
| 6 | Intellectual property violation | Use original content |
| 7 | Ads policy violation | Follow AdMob policies |
| 8 | Impersonation | Don't copy other apps |

### Apple App Store Rejections
| # | Reason | Prevention |
|---|--------|------------|
| 1 | Crashes during review | Test on latest iOS version |
| 2 | Incomplete information | Provide demo account credentials |
| 3 | Guideline 4.3 — Spam/similar apps | Ensure app provides unique value |
| 4 | Privacy policy missing/inadequate | Include comprehensive privacy policy |
| 5 | Sign in with Apple missing | Add if other social logins exist |
| 6 | No account deletion | Must provide account deletion |
| 7 | In-app purchase required (digital goods) | Can't use external payment for digital |
| 8 | Guideline 2.1 — Performance | Optimize for speed and stability |
| 9 | Metadata issues | Match screenshots to actual app |
| 10 | Kids category issues | Follow COPPA if targeting children |

---

## Quick Reference: Common Mistakes to Avoid

| # | Mistake | Prevention |
|---|---------|------------|
| 1 | No contract | Always sign before starting |
| 2 | Scope creep | Document scope, charge for extras |
| 3 | No advance payment | Take 30-50% advance |
| 4 | Skipping design phase | Design first, develop second |
| 5 | Not testing on real devices | Don't rely only on emulators |
| 6 | Hardcoded API keys | Use environment variables |
| 7 | No crash reporting | Set up Crashlytics/Sentry from day 1 |
| 8 | No version control | Use Git from the start |
| 9 | Ignoring app store guidelines | Read guidelines before development |
| 10 | No backup strategy | Set up automated backups |
| 11 | Poor error handling | Handle network, auth, server errors gracefully |
| 12 | No analytics | Install analytics before launch |
| 13 | Forgetting account deletion | Apple requires it — build it in |
| 14 | Not planning for updates | Build with maintainability in mind |

---

> **Tip:** Copy this checklist into your project management tool at the start of every mobile app project. Check off items as you complete them.
