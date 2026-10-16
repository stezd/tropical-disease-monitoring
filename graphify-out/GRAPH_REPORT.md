# Graph Report - tropical-disease-monitoring  (2026-10-14)

## Corpus Check
- 262 files · ~127,600 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 27 file(s) not represented in the graph (top: (none) 18, .example 2, .lock 2)

## Summary
- 1728 nodes · 4428 edges · 102 communities (73 shown, 29 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 209 edges (avg confidence: 0.91)
- Token cost: 48,000 input · 8,200 output

## Community Hubs (Navigation)
- User Management & API Services
- Generated API Types & Triage Contracts
- Backend Wiring & Auth Dependencies
- User & CRUD Tests
- Generated SDK Error & Response Types
- React Email Templates
- Playwright E2E Test Suite
- Triage Quiz Domain Logic
- Triage API Routes
- Triage Scoring Rules & Case Tests
- Triage Content Schema
- Triage Advice Builder
- Frontend Runtime Dependencies
- Backend Test Fixtures & Seed Data
- Card & Menu Primitives
- Alembic Migrations
- Biome Linter Config
- Frontend Package Manifest
- Sidebar, Appearance & User Menu
- Release Automation Scripts
- Flow Content Loading & Snapshot
- DataTable & Admin Tables
- Result Screen & QR Handover
- Login & Private User Routes
- Sidebar Primitives & Footer
- React Email Package Manifest
- Game Effects, Art & Settings
- User Routes & CRUD
- Project Documentation Overview
- Frontend Bootstrap & Theming
- TypeScript Compiler Config
- Database Models
- Generated URL Serializers
- shadcn Component Registry Config
- Alert, Badge & Button Primitives
- Generated HTTP Client Core
- App Shell & Route Screens
- Live Scoring Hooks & Thinking Screen
- Scoring Engine Abstraction
- Triage Blueprint & Content Docs
- Generated Client Core Types
- Deployment & Compose Docs
- Frontend Dev Dependencies
- Generated Client Utilities
- TropiCek Prototype Feature Concepts
- Clinical Route Mapping & Vitals
- Triage API Tests
- Generated Query Param Serializer
- Sheet Drawer Component
- Root Package Scripts
- React Email TS Config
- Backend Settings & Secrets
- Login SDK Service
- Triage SDK Service
- Logo & App Sidebar Branding
- Quiz State Store
- Quiz UI Helpers & Red Screen
- Login Token Route
- Emergency Red Route & Frontend Docs
- Frontend npm Scripts
- Vendored QR Code Generator
- Node TS Config
- Generated Body Serializers
- Generated Query Key Serializer
- Body Map & Pain Scale
- Vite Build Config
- GitHub CI Workflows
- Backend Docs & Email Templates
- FastAPI Brand Assets
- QR Code Generator Types
- Template Screenshots & Social Banner
- Admin Dashboard Screenshots
- Utils SDK Service
- Location & Province Detection
- Copy to Clipboard Hook
- Build TS Config
- Privacy & Standalone Policy
- OpenAPI Client Generator Config
- Vite Env Types
- React Email Biome Config
- Library Skills Docs
- Release Labeling Workflows
- Backend Format Script
- Backend Lint Script
- Backend Prestart Script
- Backend Start Script
- Backend Test Script
- Backend Tests-Start Script
- Client Generation Script
- Root Test Script
- Local Test Script
- Design System Button Pattern
- Backend Project Config

## God Nodes (most connected - your core abstractions)
1. `cn()` - 130 edges
2. `FlowContent` - 63 edges
3. `User` - 39 edges
4. `random_lower_string()` - 38 edges
5. `Answers` - 36 edges
6. `UserCreate` - 34 edges
7. `random_email()` - 34 edges
8. `QuizScreen()` - 31 edges
9. `create_user()` - 30 edges
10. `run()` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Library Skills (agents)` --semantically_similar_to--> `Library Skills (claude)`  [INFERRED] [semantically similar]
  .agents/skills/library-skills/SKILL.md → .claude/skills/library-skills/SKILL.md
- `Offline Emergency-Check Snapshot` --semantically_similar_to--> `renderRed() Emergency Screen`  [INFERRED] [semantically similar]
  backend/app/triage/content/README.md → docs/TropiCek-Simulasi.html
- `Serena Project Config` --conceptually_related_to--> `TropiCare`  [INFERRED]
  .serena/project.yml → AGENTS.md
- `Railway Deployment Guide` --conceptually_related_to--> `Offline Emergency-Check Snapshot`  [INFERRED]
  deployment-railway.md → backend/app/triage/content/README.md
- `0-10 Face Pain Scale` --conceptually_related_to--> `Triage Scoring Weights`  [INFERRED]
  docs/TropiCek-Simulasi.html → backend/app/triage/content/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Referral Route Determination Flow** — agents_referral_routes, agents_emergency_browser_check, agents_route_escalation_rules, design_route_colors [INFERRED 0.85]
- **CI/CD Quality Pipeline** — _github_workflows_test_backend_test_backend, _github_workflows_playwright_playwright_tests, _github_workflows_pre_commit_pre_commit, _github_workflows_zizmor_zizmor, _pre_commit_config_hooks [INFERRED 0.85]
- **TropiCare Documentation Set** — agents_tropicare, design_tropicare_design_system, readme_tropicare, claude_notes_for_claude [EXTRACTED 1.00]
- **Adaptive Triage Routing Flow** — docs_blueprint_red_flags, docs_blueprint_rute_merah, docs_blueprint_rute_kuning_khusus, docs_blueprint_rute_kuning, docs_blueprint_rute_hijau [EXTRACTED 1.00]
- **Triage Scoring and Route Decision Pipeline** — docs_tropicek_simulasi_compute, docs_tropicek_simulasi_decide, docs_tropicek_simulasi_crossval, docs_tropicek_simulasi_drugflags, backend_app_triage_content_readme_scoring_weights, docs_blueprint_cvd_risk_score [INFERRED 0.85]
- **Docker and Railway Deployment Stack** — compose, compose_override, compose_deploy, deployment_railway, deployment_docker_compose [INFERRED 0.85]
- **FastAPI brand asset family (icon, logo, light variants, favicon PNG)** — frontend_public_assets_images_fastapi_icon_logo, frontend_public_assets_images_fastapi_icon_light_logo, frontend_public_assets_images_fastapi_logo_logo, frontend_public_assets_images_fastapi_logo_light_logo, frontend_public_assets_images_favicon_logo [INFERRED 0.95]
- **Light/dark theme variant pairs of the FastAPI icon and logo** — frontend_public_assets_images_fastapi_icon_logo, frontend_public_assets_images_fastapi_icon_light_logo, frontend_public_assets_images_fastapi_logo_logo, frontend_public_assets_images_fastapi_logo_light_logo [INFERRED 0.95]
- **FastAPI template admin UI captured across themes and entity lists** — img_dashboard_users_admin_screen, img_dashboard_dark_users_admin_screen, img_dashboard_items_items_list_screen [INFERRED 0.85]
- **Generated OpenAPI spec, secured login/users endpoints, and the admin screens that consume them** — img_docs_swagger_ui_screen, img_dashboard_users_admin_screen, img_dashboard_items_items_list_screen, img_dashboard_dark_users_admin_screen [INFERRED 0.85]
- **FastAPI full-stack template auth + email round-trip (login form -> password recovery email -> react-email authoring -> Mailpit capture)** — img_login_screen, img_mailpit_password_recovery_email, img_react_email_preview, img_mailpit_dev_mailbox [INFERRED 0.85]
- **FastAPI template branding assets sharing the #009688 teal identity and lightning-bolt logo (social preview PNG/SVG and login page brand panel)** — img_github_social_preview_banner, img_github_social_preview_svg_artwork, img_login_screen [INFERRED 0.75]

## Communities (102 total, 29 thin omitted)

### Community 0 - "User Management & API Services"
Cohesion: 0.06
Nodes (102): UsersService, UserPublic, AddUser(), FormData, formSchema, columns, UserTableData, DeleteUser() (+94 more)

### Community 1 - "Generated API Types & Triage Contracts"
Cohesion: 0.05
Nodes (78): Answers, Body_login_login_access_token, Body_triage_analyze_photo, BodyRegion, ClientOptions, Cluster, DiseasePublic, HTTPValidationError (+70 more)

### Community 2 - "Backend Wiring & Auth Dependencies"
Cohesion: 0.06
Nodes (19): get_current_active_superuser(), get_current_user(), get_db(), recover_password(), recover_password_html_content(), reset_password(), test_token(), health_check() (+11 more)

### Community 3 - "User & CRUD Tests"
Cohesion: 0.16
Nodes (44): verify_password(), create_user(), UserCreate, test_reset_password(), test_create_user_by_normal_user(), test_create_user_existing_username(), test_create_user_new_email(), test_delete_user_current_super_user_error() (+36 more)

### Community 4 - "Generated SDK Error & Response Types"
Cohesion: 0.04
Nodes (50): Options, loginLoginAccessTokenErrors, loginLoginAccessTokenResponses, loginRecoverPasswordErrors, loginRecoverPasswordHtmlContentErrors, loginRecoverPasswordHtmlContentResponses, loginRecoverPasswordResponses, loginResetPasswordErrors (+42 more)

### Community 5 - "React Email Templates"
Cohesion: 0.08
Nodes (39): bodyTextStyle, NewAccount(), NewAccountProps, supportingTextStyle, bodyTextStyle, ResetPassword(), ResetPasswordProps, supportingTextStyle (+31 more)

### Community 6 - "Playwright E2E Test Suite"
Cohesion: 0.08
Nodes (17): client, PrivateService, __dirname, __filename, firstSuperuser, firstSuperuserPassword, tabs, EmailSummary (+9 more)

### Community 7 - "Triage Quiz Domain Logic"
Cohesion: 0.13
Nodes (40): Options(), ageOf(), asksPregnancy(), bmiOf(), companionQuestion(), diaValid(), glucoseValid(), hasRedFlag() (+32 more)

### Community 8 - "Triage API Routes"
Cohesion: 0.09
Nodes (17): analyze_photo(), _content(), create_screening(), read_flow(), read_screenings(), score_answers(), score_flow(), DiseasePublic (+9 more)

### Community 9 - "Triage Scoring Rules & Case Tests"
Cohesion: 0.13
Nodes (31): drug_flags(), FlowContent, cvd_risk(), RuleEngine, run(), test_chronic_gout(), test_chronic_tengkuk_scores_hypertension_and_lipids(), test_chronic_without_complaint_is_unknown() (+23 more)

### Community 10 - "Triage Content Schema"
Cohesion: 0.09
Nodes (26): Advice, AnalysisSteps, AsymmetryRule, BodyRegion, BodyRule, BodyWeights, ChikChronicWarning, Cluster (+18 more)

### Community 11 - "Triage Advice Builder"
Cohesion: 0.12
Nodes (22): build_result(), public(), cross_checks(), _fmt(), _missing_vitals(), _no_thermo_text(), _pct(), picked_options() (+14 more)

### Community 12 - "Frontend Runtime Dependencies"
Cohesion: 0.06
Nodes (34): dependencies, axios, class-variance-authority, clsx, form-data, @hookform/resolvers, lucide-react, @radix-ui/react-avatar (+26 more)

### Community 13 - "Backend Test Fixtures & Seed Data"
Cohesion: 0.12
Nodes (13): init_db(), update_user(), init(), main(), User, UserUpdate, client(), db() (+5 more)

### Community 14 - "Card & Menu Primitives"
Cohesion: 0.11
Nodes (24): Card(), CardAction(), CardContent(), CardDescription(), CardFooter(), CardHeader(), CardTitle(), DropdownMenuCheckboxItem() (+16 more)

### Community 15 - "Alembic Migrations"
Cohesion: 0.12
Nodes (13): get_url(), run_migrations_offline(), run_migrations_online(), downgrade(), upgrade(), downgrade(), upgrade(), downgrade() (+5 more)

### Community 16 - "Biome Linter Config"
Cohesion: 0.07
Nodes (29): source, assist, actions, css, parser, files, includes, formatter (+21 more)

### Community 17 - "Frontend Package Manifest"
Cohesion: 0.07
Nodes (29): @biomejs/biome, react, react-dom, @types/react, @types/react-dom, name, private, type (+21 more)

### Community 18 - "Sidebar, Appearance & User Menu"
Cohesion: 0.16
Nodes (26): Appearance(), ICON_MAP, LucideIcon, SidebarAppearance(), Item, Main(), MainProps, User() (+18 more)

### Community 19 - "Release Automation Scripts"
Cohesion: 0.17
Nodes (10): main(), bump_version(), current_version(), get_current_version(), get_release_notes_body(), parse_version(), prepare(), prepare_release() (+2 more)

### Community 20 - "Flow Content Loading & Snapshot"
Cohesion: 0.12
Nodes (15): get_content(), raw_content(), _read(), main(), snapshot(), test_bad_finding_disease_is_rejected(), test_bad_id_is_rejected(), test_content_loads() (+7 more)

### Community 21 - "DataTable & Admin Tables"
Cohesion: 0.18
Nodes (21): DataTable(), DataTableProps, PendingUsers(), Select(), SelectContent(), SelectItem(), SelectLabel(), SelectScrollDownButton() (+13 more)

### Community 22 - "Result Screen & QR Handover"
Cohesion: 0.17
Nodes (24): scoreAnswers(), useFlow(), Sparkles(), Card(), Rich(), WarnBox(), confetti(), jknURL() (+16 more)

### Community 23 - "Login & Private User Routes"
Cohesion: 0.12
Nodes (11): create_user(), PrivateUserCreate, get_password_hash(), test_get_access_token(), test_get_access_token_incorrect_password(), test_login_with_argon2_password_keeps_hash(), test_login_with_bcrypt_password_upgrades_to_argon2(), test_recovery_password() (+3 more)

### Community 24 - "Sidebar Primitives & Footer"
Cohesion: 0.13
Nodes (21): Footer(), SidebarContext, SidebarContextProps, SidebarGroupAction(), SidebarGroupLabel(), SidebarInput(), SidebarInset(), SidebarMenuAction() (+13 more)

### Community 25 - "React Email Package Manifest"
Cohesion: 0.08
Nodes (25): dependencies, react, react-dom, react-email, @react-email/components, devDependencies, @biomejs/biome, @react-email/ui (+17 more)

### Community 26 - "Game Effects, Art & Settings"
Cohesion: 0.15
Nodes (18): hop(), Palm(), Scene(), SideHill(), Modal(), Note, sfx, tone() (+10 more)

### Community 27 - "User Routes & CRUD"
Cohesion: 0.23
Nodes (11): create_user(), delete_user(), delete_user_me(), read_user_by_id(), read_user_me(), read_users(), register_user(), update_password_me() (+3 more)

### Community 28 - "Project Documentation Overview"
Cohesion: 0.12
Nodes (18): Deploy with Docker Compose, Playwright Tests Workflow, Serena Project Config, Chronic Path (PTM Screening), Infection Path (20 Tropical Diseases), JSON Quiz Content (backend/app/triage/content/), Gemma4 + RAG Prediction (self-hosted), Referral Routes (MERAH / KUNING KHUSUS / KUNING / HIJAU) (+10 more)

### Community 29 - "Frontend Bootstrap & Theming"
Cohesion: 0.11
Nodes (13): initialState, Theme, ThemeProvider(), ThemeProviderContext, ThemeProviderProps, ThemeProviderState, Toaster(), queryClient (+5 more)

### Community 30 - "TypeScript Compiler Config"
Cohesion: 0.10
Nodes (20): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+12 more)

### Community 31 - "Database Models"
Cohesion: 0.17
Nodes (14): get_datetime_utc(), NewPassword, Screening, ScreeningPublic, ScreeningsPublic, Token, TokenPayload, UpdatePassword (+6 more)

### Community 32 - "Generated URL Serializers"
Cohesion: 0.18
Nodes (18): createQuerySerializer(), ArraySeparatorStyle, ArrayStyle, MatrixStyle, ObjectSeparatorStyle, ObjectStyle, separatorArrayExplode(), separatorArrayNoExplode() (+10 more)

### Community 33 - "shadcn Component Registry Config"
Cohesion: 0.11
Nodes (18): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+10 more)

### Community 34 - "Alert, Badge & Button Primitives"
Cohesion: 0.16
Nodes (14): Alert(), AlertDescription(), AlertTitle(), alertVariants, Badge(), badgeVariants, ButtonGroup(), ButtonGroupSeparator() (+6 more)

### Community 35 - "Generated HTTP Client Core"
Cohesion: 0.20
Nodes (15): CreateClientConfig, BuildUrlFn, Client, ClientOptions, Config, CreateClientConfig, MethodFn, OmitKeys (+7 more)

### Community 36 - "App Shell & Route Screens"
Cohesion: 0.23
Nodes (13): ToastHost(), HomePage(), Loading(), ScreeningPage(), Shell(), SummaryPage(), WithFlow(), useQuiz() (+5 more)

### Community 37 - "Live Scoring Hooks & Thinking Screen"
Cohesion: 0.19
Nodes (13): FlowPublic, ScoreResult, FLOW_ID, OFFLINE, scoreKey(), useDebounced(), useLiveScore(), Mascot (+5 more)

### Community 38 - "Scoring Engine Abstraction"
Cohesion: 0.17
Nodes (9): features(), _flag(), ModelEngine, _num(), rank(), Ranked, ScoringEngine, test_features_are_numeric() (+1 more)

### Community 39 - "Triage Blueprint & Content Docs"
Cohesion: 0.20
Nodes (15): Triage Content README, Triage Scoring Weights, Shared Option IDs, Triage Content JSON Files, Triage Blueprint, Anthropometry and BMI, Chronic Disease (PTM) Path, CVD Risk Score (Framingham Adaptation) (+7 more)

### Community 40 - "Generated Client Core Types"
Cohesion: 0.19
Nodes (12): AuthToken, BodySerializer, QuerySerializer, QuerySerializerOptions, ServerSentEventsOptions, ServerSentEventsResult, StreamEvent, Client (+4 more)

### Community 41 - "Deployment & Compose Docs"
Cohesion: 0.22
Nodes (14): Docker Compose Base Stack, Backend Healthcheck via Python One-liner, Docker Compose Deploy Overlay, Docker Compose Local Override, Traefik Reverse Proxy, FastAPI Cloud Deployment Guide, Docker Compose Deployment Guide, Railway Deployment Guide (+6 more)

### Community 42 - "Frontend Dev Dependencies"
Cohesion: 0.14
Nodes (14): devDependencies, @biomejs/biome, dotenv, @hey-api/openapi-ts, @playwright/test, @tanstack/router-devtools, @tanstack/router-plugin, tw-animate-css (+6 more)

### Community 43 - "Generated Client Utilities"
Cohesion: 0.32
Nodes (12): createClient(), axiosHeadersKeywords, buildUrl(), checkForExistence(), createConfig(), mergeConfigs(), mergeHeaders(), setAuthParams() (+4 more)

### Community 44 - "TropiCek Prototype Feature Concepts"
Cohesion: 0.17
Nodes (13): Dynamic Deep-Dive HPI, Medico-Legal Disclaimer, Drug Warning Triggers, QR Triage Handover, Recommended Lab Tests, TropiCek HTML Simulation, crossVal() Cross-Validation, drugFlags() Drug Warnings (+5 more)

### Community 45 - "Clinical Route Mapping & Vitals"
Cohesion: 0.22
Nodes (13): One Health Ecology Risk Mapping, Route HIJAU (Self-care / Pharmacy), Route KUNING (Puskesmas / Clinic), Route KUNING KHUSUS (National Program Poli), Vital Sign Proxies, Doctor's Answers Document, Endemic Provinces, BMI Thresholds (+5 more)

### Community 46 - "Triage API Tests"
Cohesion: 0.29
Nodes (9): test_list_screenings_superuser_only(), test_photo_analysis_not_available(), test_read_chronic_flow(), test_read_flow(), test_read_unknown_flow(), test_save_needs_consent(), test_save_screening(), test_score() (+1 more)

### Community 47 - "Generated Query Param Serializer"
Cohesion: 0.20
Nodes (11): buildClientParams(), buildKeyMap(), extraPrefixes, extraPrefixesMap, Field, Fields, FieldsConfig, KeyMap (+3 more)

### Community 48 - "Sheet Drawer Component"
Cohesion: 0.26
Nodes (9): Sheet(), SheetContent(), SheetDescription(), SheetFooter(), SheetHeader(), SheetOverlay(), SheetPortal(), SheetTitle() (+1 more)

### Community 49 - "Root Package Scripts"
Cohesion: 0.17
Nodes (11): name, private, scripts, build, dev, email:dev, email:export, lint (+3 more)

### Community 50 - "React Email TS Config"
Cohesion: 0.17
Nodes (11): compilerOptions, composite, jsx, module, moduleResolution, noEmit, skipLibCheck, strict (+3 more)

### Community 52 - "Login SDK Service"
Cohesion: 0.18
Nodes (6): LoginService, loginLoginAccessTokenData, loginRecoverPasswordData, loginRecoverPasswordHtmlContentData, loginResetPasswordData, loginTestTokenData

### Community 53 - "Triage SDK Service"
Cohesion: 0.18
Nodes (6): TriageService, triageAnalyzePhotoData, triageCreateScreeningData, triageReadFlowData, triageReadScreeningsData, triageScoreFlowData

### Community 54 - "Logo & App Sidebar Branding"
Cohesion: 0.31
Nodes (9): Icon(), Logo(), LogoProps, Wordmark(), AppSidebar(), baseItems, SidebarContent(), SidebarFooter() (+1 more)

### Community 55 - "Quiz State Store"
Cohesion: 0.24
Nodes (9): blankAnswers(), QuizAnswers, fresh(), listeners, Phase, quiz, QuizState, read() (+1 more)

### Community 56 - "Quiz UI Helpers & Red Screen"
Cohesion: 0.33
Nodes (8): Choice, copyText(), emit(), RED_TAB, StageMap(), toast(), toastListeners, RedScreen()

### Community 57 - "Login Token Route"
Cohesion: 0.22
Nodes (3): login_access_token(), create_access_token(), authenticate()

### Community 58 - "Emergency Red Route & Frontend Docs"
Cohesion: 0.25
Nodes (9): Offline Emergency-Check Snapshot, 119 Emergency Activation, Emergency Red Flags / Primary Survey, Route MERAH (IGD Emergency), Red Route First Aid DO/DON'T, renderRed() Emergency Screen, Frontend README, Generated OpenAPI Client (+1 more)

### Community 59 - "Frontend npm Scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, generate-client, lint, preview, test, test:ui

### Community 60 - "Vendored QR Code Generator"
Cohesion: 0.39
Nodes (6): C(), e(), i(), a(), d(), p()

### Community 61 - "Node TS Config"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 62 - "Generated Body Serializers"
Cohesion: 0.29
Nodes (4): formDataBodySerializer, jsonBodySerializer, QuerySerializerOptionsObject, urlSearchParamsBodySerializer

### Community 63 - "Generated Query Key Serializer"
Cohesion: 0.48
Nodes (6): isPlainObject(), JsonValue, queryKeyJsonReplacer(), serializeQueryKeyValue(), serializeSearchParams(), stringifyToJsonValue()

### Community 64 - "Body Map & Pain Scale"
Cohesion: 0.33
Nodes (6): BodyMap(), PAIN_COLORS, PainScale(), SHAPES, SKIN, StepBody()

### Community 65 - "Vite Build Config"
Cohesion: 0.29
Nodes (4): @tailwindcss/vite, @tanstack/router-plugin, vite, @vitejs/plugin-react-swc

### Community 66 - "GitHub CI Workflows"
Cohesion: 0.33
Nodes (6): Dependabot Configuration, PR Push Workflows, pre-commit Workflow, Test Backend Workflow, Zizmor Security Workflow, Pre-commit Hooks Configuration

### Community 67 - "Backend Docs & Email Templates"
Cohesion: 0.33
Nodes (6): New Account Email Template, Test Email Template, Backend README, React Email Email Templates, generate_*_email() Jinja Context Builder, Alembic Database Migrations

### Community 68 - "FastAPI Brand Assets"
Cohesion: 0.60
Nodes (6): FastAPI Icon light variant (pure white circle + white bolt, for dark backgrounds), FastAPI Icon (teal circle with white lightning bolt, 500x500 SVG), FastAPI Logo light variant (all-white icon and wordmark, for dark backgrounds), FastAPI Logo (teal icon plus "FastAPI" Ubuntu wordmark, horizontal lockup), FastAPI brand asset set in frontend/public/assets/images (official framework icon/logo, light + dark variants), FastAPI favicon PNG (teal circle with white lightning bolt, rasterized icon)

### Community 70 - "Template Screenshots & Social Banner"
Cohesion: 0.40
Nodes (6): GitHub Social Preview Banner (PNG) — teal FastAPI lightning-bolt mark plus 'Full Stack' / 'FastAPI' / 'Template' wordmark on white, 1280x640 repo social card, teal #009688 brand color, GitHub Social Preview Banner (SVG source) — Inkscape-authored vector artwork exporting to github-social-preview.png: filled teal circle (id path875...) with white lightning-bolt path, plus three Ubuntu-font text spans 'Full Stack', 'FastAPI', 'Template'; viewBox 338.66x169.33mm, 96 dpi export, Login screen screenshot — two-column auth layout: left brand panel with FastAPI logo, right form card titled 'Login to your account' with Email field (user@example.com), Password field with reveal eye toggle and 'Forgot your password?' link, teal 'Log In' button, 'Sign up' link, and dark footer 'FastAPI Template - 2025' with GitHub/X/LinkedIn icons, Mailpit dev mailbox screenshot — local SMTP catcher at localhost showing inbox list of two unread messages 'Full Stack FastAPI Project - Password recovery for user admin@example.com' and a message detail pane with HTML/HTML Source/Text/Headers/Raw/HTML Check/Link Check tabs; rendered email has heading 'Reset your password', teal 'Reset password' button, copyable http://localhost:5173/reset-password?token=... link, 'This link will expire in 48 hours.' and copyright 2026, Password recovery email template — transactional 'Reset your password' email with subject 'Full Stack FastAPI Project - Password recovery for user admin@example.com', from <info@example.com> to <admin@example.com>, containing a reset-password deep link with a token and a 48-hour expiry; rationale: enables self-service account recovery without exposing whether an email is registered, and Mailpit is used so no real mail leaves the dev environment, React Email preview screenshot — react-email dev server with file sidebar (new_account, reset_password, test_email) and reset_password.tsx selected in a split source/preview toolbar; rendered preview shows the same reset-password template with unresolved template variables {{ PROJECT_NAME }}, {{ username }}, {{ project_name }}, {{ link }}, {{ valid_hours }}, and a bottom status bar with Linter/Compatibility/Spam/Resend checks

### Community 71 - "Admin Dashboard Screenshots"
Cohesion: 0.50
Nodes (5): favicon.svg — rounded-square app icon with bespectacled mascot face, dashboard-dark.png — same Admin > Users screen in dark theme, dashboard-items.png — Items screen listing the template's demo Item records, dashboard.png — Admin > Users screen (light theme) listing 72 user accounts, docs.png — generated Swagger UI at /docs showing login and users endpoints

### Community 72 - "Utils SDK Service"
Cohesion: 0.40
Nodes (3): UtilsService, utilsHealthCheckData, utilsTestEmailData

### Community 74 - "Location & Province Detection"
Cohesion: 0.67
Nodes (3): askProvince(), Province, provinceFromCoords()

### Community 76 - "Build TS Config"
Cohesion: 0.50
Nodes (3): exclude, extends, ./tsconfig.json

## Ambiguous Edges - Review These
- `FastAPI Icon light variant (pure white circle + white bolt, for dark backgrounds)` → `FastAPI favicon PNG (teal circle with white lightning bolt, rasterized icon)`  [AMBIGUOUS]
  frontend/public/assets/images/favicon.png · relation: conceptually_related_to
- `favicon.svg — rounded-square app icon with bespectacled mascot face` → `docs.png — generated Swagger UI at /docs showing login and users endpoints`  [AMBIGUOUS]
  frontend/public/favicon.svg · relation: conceptually_related_to

## Knowledge Gaps
- **62 isolated node(s):** `app`, `@radix-ui/react-radio-group`, `@radix-ui/react-scroll-area`, `@tanstack/react-query-devtools`, `@tanstack/react-router-devtools` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 532 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `random_lower_string()` connect `User & CRUD Tests` to `Backend Test Fixtures & Seed Data`, `Playwright E2E Test Suite`, `Login & Private User Routes`?**
  _High betweenness centrality (0.303) - this node is a cross-community bridge._
- **Are the 49 inferred relationships involving `FlowContent` (e.g. with `_content()` and `build_result()`) actually correct?**
  _`FlowContent` has 49 INFERRED edges - model-reasoned connections that need verification._
- **What connects `app`, `@radix-ui/react-radio-group`, `@radix-ui/react-scroll-area` to the rest of the system?**
  _62 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `User Management & API Services` be split into smaller, more focused modules?**
  _Cohesion score 0.05574980574980575 - nodes in this community are weakly interconnected._
- **Why does `@playwright/test` connect `Playwright E2E Test Suite` to `Frontend Package Manifest`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `FastAPI Icon light variant (pure white circle + white bolt, for dark backgrounds)` and `FastAPI favicon PNG (teal circle with white lightning bolt, rasterized icon)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `favicon.svg — rounded-square app icon with bespectacled mascot face` and `docs.png — generated Swagger UI at /docs showing login and users endpoints`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
