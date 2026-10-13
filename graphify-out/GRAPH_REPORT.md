# Graph Report - tropical-disease-monitoring  (2026-10-13)

## Corpus Check
- 232 files · ~90,635 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 23 file(s) not represented in the graph (top: (none) 17, .lock 2, .ini 1)

## Summary
- 1292 nodes · 3557 edges · 72 communities (46 shown, 26 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 73 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Form
- Utils
- Types.Gen
- Routetree.Gen
- Test Users
- Layout
- Models
- Types.Gen
- Pagination
- Random
- Package
- Dropdown Menu
- Conftest
- Prepare Release
- Biome
- Sidebar
- Env
- Select
- Package
- Package
- Items
- Test Login
- Theme Provider
- Sdk.Gen
- Tsconfig
- Pathserializer.Gen
- Components
- Types.Gen
- Test Items
- Sidebar
- Types.Gen
- Package
- Utils.Gen
- Sheet
- Params.Gen
- Tsconfig
- Config
- Sdk.Gen
- Package
- Package
- Tsconfig.Node
- Bodyserializer.Gen
- Querykeyserializer.Gen
- Package
- Agents
- Sdk.Gen
- Tsconfig.Build
- Openapi Ts.Config
- Sdk.Gen
- Footer
- Vite Env.D
- Biome
- Format
- Lint
- Prestart
- Test
- Tests Start
- Blueprint
- Blueprint
- Readitem Itemsreaditemdata
- Generate Client
- Test
- Test Local
- Rencana Kerja
- Module 71

## God Nodes (most connected - your core abstractions)
1. `cn()` - 129 edges
2. `random_lower_string()` - 40 edges
3. `User` - 39 edges
4. `Button()` - 38 edges
5. `UserCreate` - 34 edges
6. `random_email()` - 34 edges
7. `create_user()` - 30 edges
8. `LoadingButton()` - 29 edges
9. `lucide-react` - 26 edges
10. `useAuth()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Visual Analogue Scale (VAS) Nyeri` --conceptually_related_to--> `Tahap 3: Anamnesis Mendalam Dinamis (Deep-Dive HPI)`  [INFERRED]
  DESIGN.md → docs/Blueprint.md
- `Integrasi Tombol Mobile JKN` --conceptually_related_to--> `Triage Routing & Scoring Logic`  [INFERRED]
  AGENTS.md → docs/Blueprint.md
- `get_current_user()` --uses--> `User`  [INFERRED]
  backend/app/api/deps.py → backend/app/models.py
- `get_current_active_superuser()` --uses--> `User`  [INFERRED]
  backend/app/api/deps.py → backend/app/models.py
- `read_items()` --uses--> `ItemPublic`  [INFERRED]
  backend/app/api/routes/items.py → backend/app/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pipeline Triase TropiCek (Tahap 1 s/d Tahap 3 & Scoring)** — docs_blueprint_tahap1_filter_gawat_darurat, docs_blueprint_tahap2_chief_complaint, docs_blueprint_tahap3_deep_dive, docs_blueprint_scoring_and_triage [EXTRACTED 1.00]

## Communities (72 total, 26 thin omitted)

### Community 0 - "Form"
Cohesion: 0.07
Nodes (99): ItemsService, ItemPublic, UserPublic, AddUser(), FormData, formSchema, DeleteUser(), DeleteUserProps (+91 more)

### Community 1 - "Utils"
Cohesion: 0.05
Nodes (18): get_current_active_superuser(), get_current_user(), get_db(), login_access_token(), recover_password_html_content(), test_token(), health_check(), test_email() (+10 more)

### Community 2 - "Types.Gen"
Cohesion: 0.06
Nodes (65): Body_login_login_access_token, ClientOptions, HTTPValidationError, ItemCreate, itemsCreateItemError, itemsCreateItemResponse, itemsDeleteItemError, itemsDeleteItemResponse (+57 more)

### Community 3 - "Routetree.Gen"
Cohesion: 0.06
Nodes (48): columns, UserTableData, ErrorComponent(), NotFound(), Tabs(), TabsContent(), TabsList(), TabsTrigger() (+40 more)

### Community 4 - "Test Users"
Cohesion: 0.16
Nodes (45): verify_password(), authenticate(), create_user(), UserCreate, test_reset_password(), test_create_user_by_normal_user(), test_create_user_existing_username(), test_create_user_new_email() (+37 more)

### Community 5 - "Layout"
Cohesion: 0.08
Nodes (39): bodyTextStyle, NewAccount(), NewAccountProps, supportingTextStyle, bodyTextStyle, ResetPassword(), ResetPasswordProps, supportingTextStyle (+31 more)

### Community 6 - "Models"
Cohesion: 0.13
Nodes (29): recover_password(), reset_password(), create_user(), delete_user(), delete_user_me(), read_user_by_id(), read_user_me(), read_users() (+21 more)

### Community 7 - "Types.Gen"
Cohesion: 0.05
Nodes (41): Options, itemsCreateItemData, itemsCreateItemErrors, itemsCreateItemResponses, itemsDeleteItemData, itemsDeleteItemErrors, itemsReadItemErrors, itemsReadItemResponses (+33 more)

### Community 8 - "Pagination"
Cohesion: 0.10
Nodes (32): Alert(), AlertDescription(), AlertTitle(), alertVariants, AvatarImage(), Badge(), badgeVariants, ButtonGroup() (+24 more)

### Community 9 - "Random"
Cohesion: 0.12
Nodes (17): __dirname, __filename, firstSuperuser, firstSuperuserPassword, tabs, EmailSummary, waitForEmailHtml(), createUser() (+9 more)

### Community 10 - "Package"
Cohesion: 0.06
Nodes (34): dependencies, axios, class-variance-authority, clsx, form-data, @hookform/resolvers, lucide-react, @radix-ui/react-avatar (+26 more)

### Community 11 - "Dropdown Menu"
Cohesion: 0.12
Nodes (26): Appearance(), ICON_MAP, LucideIcon, SidebarAppearance(), ItemActionsMenu(), User(), UserInfo(), UserInfoProps (+18 more)

### Community 12 - "Conftest"
Cohesion: 0.11
Nodes (12): init_db(), init(), main(), User, test_create_user(), client(), db(), normal_user_token_headers() (+4 more)

### Community 13 - "Prepare Release"
Cohesion: 0.15
Nodes (10): main(), bump_version(), current_version(), get_current_version(), get_release_notes_body(), parse_version(), prepare(), prepare_release() (+2 more)

### Community 14 - "Biome"
Cohesion: 0.07
Nodes (29): source, assist, actions, css, parser, files, includes, formatter (+21 more)

### Community 15 - "Sidebar"
Cohesion: 0.11
Nodes (25): Item, Main(), MainProps, SidebarContext, SidebarContextProps, SidebarGroup(), SidebarGroupAction(), SidebarGroupContent() (+17 more)

### Community 16 - "Env"
Cohesion: 0.13
Nodes (11): get_url(), run_migrations_offline(), run_migrations_online(), downgrade(), upgrade(), downgrade(), upgrade(), downgrade() (+3 more)

### Community 17 - "Select"
Cohesion: 0.23
Nodes (20): DataTable(), DataTableProps, PendingItems(), PendingUsers(), Select(), SelectContent(), SelectItem(), SelectLabel() (+12 more)

### Community 18 - "Package"
Cohesion: 0.08
Nodes (25): dependencies, react, react-dom, react-email, @react-email/components, devDependencies, @biomejs/biome, @react-email/ui (+17 more)

### Community 19 - "Package"
Cohesion: 0.08
Nodes (24): @biomejs/biome, react, react-dom, @types/react, @types/react-dom, name, private, type (+16 more)

### Community 20 - "Items"
Cohesion: 0.18
Nodes (9): create_item(), delete_item(), read_item(), read_items(), update_item(), create_item(), update_user(), Item (+1 more)

### Community 21 - "Test Login"
Cohesion: 0.14
Nodes (11): create_user(), PrivateUserCreate, get_password_hash(), test_get_access_token(), test_get_access_token_incorrect_password(), test_login_with_argon2_password_keeps_hash(), test_login_with_bcrypt_password_upgrades_to_argon2(), test_recovery_password() (+3 more)

### Community 22 - "Theme Provider"
Cohesion: 0.11
Nodes (15): client, initialState, Theme, ThemeProvider(), ThemeProviderContext, ThemeProviderProps, ThemeProviderState, Toaster() (+7 more)

### Community 23 - "Sdk.Gen"
Cohesion: 0.10
Nodes (11): UsersService, usersCreateUserData, usersDeleteUserData, usersDeleteUserMeData, usersReadUserByIdData, usersReadUserMeData, usersReadUsersData, usersRegisterUserData (+3 more)

### Community 24 - "Tsconfig"
Cohesion: 0.10
Nodes (20): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+12 more)

### Community 25 - "Pathserializer.Gen"
Cohesion: 0.18
Nodes (18): createQuerySerializer(), ArraySeparatorStyle, ArrayStyle, MatrixStyle, ObjectSeparatorStyle, ObjectStyle, separatorArrayExplode(), separatorArrayNoExplode() (+10 more)

### Community 26 - "Components"
Cohesion: 0.11
Nodes (18): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+10 more)

### Community 27 - "Types.Gen"
Cohesion: 0.20
Nodes (15): CreateClientConfig, BuildUrlFn, Client, ClientOptions, Config, CreateClientConfig, MethodFn, OmitKeys (+7 more)

### Community 28 - "Test Items"
Cohesion: 0.31
Nodes (12): test_create_item(), test_delete_item(), test_delete_item_not_enough_permissions(), test_delete_item_not_found(), test_read_item(), test_read_item_not_enough_permissions(), test_read_item_not_found(), test_read_items() (+4 more)

### Community 29 - "Sidebar"
Cohesion: 0.22
Nodes (12): Footer(), Logo(), LogoProps, AppSidebar(), baseItems, SidebarContent(), SidebarFooter(), SidebarHeader() (+4 more)

### Community 30 - "Types.Gen"
Cohesion: 0.19
Nodes (12): AuthToken, BodySerializer, QuerySerializer, QuerySerializerOptions, ServerSentEventsOptions, ServerSentEventsResult, StreamEvent, Client (+4 more)

### Community 31 - "Package"
Cohesion: 0.14
Nodes (14): devDependencies, @biomejs/biome, dotenv, @hey-api/openapi-ts, @playwright/test, @tanstack/router-devtools, @tanstack/router-plugin, tw-animate-css (+6 more)

### Community 32 - "Utils.Gen"
Cohesion: 0.32
Nodes (12): createClient(), axiosHeadersKeywords, buildUrl(), checkForExistence(), createConfig(), mergeConfigs(), mergeHeaders(), setAuthParams() (+4 more)

### Community 33 - "Sheet"
Cohesion: 0.23
Nodes (10): Sheet(), SheetContent(), SheetDescription(), SheetFooter(), SheetHeader(), SheetOverlay(), SheetPortal(), SheetTitle() (+2 more)

### Community 34 - "Params.Gen"
Cohesion: 0.20
Nodes (11): buildClientParams(), buildKeyMap(), extraPrefixes, extraPrefixesMap, Field, Fields, FieldsConfig, KeyMap (+3 more)

### Community 35 - "Tsconfig"
Cohesion: 0.17
Nodes (11): compilerOptions, composite, jsx, module, moduleResolution, noEmit, skipLibCheck, strict (+3 more)

### Community 37 - "Sdk.Gen"
Cohesion: 0.18
Nodes (6): LoginService, loginLoginAccessTokenData, loginRecoverPasswordData, loginRecoverPasswordHtmlContentData, loginResetPasswordData, loginTestTokenData

### Community 38 - "Package"
Cohesion: 0.18
Nodes (10): name, private, scripts, dev, email:dev, email:export, lint, test (+2 more)

### Community 39 - "Package"
Cohesion: 0.25
Nodes (8): scripts, build, dev, generate-client, lint, preview, test, test:ui

### Community 40 - "Tsconfig.Node"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 41 - "Bodyserializer.Gen"
Cohesion: 0.29
Nodes (4): formDataBodySerializer, jsonBodySerializer, QuerySerializerOptionsObject, urlSearchParamsBodySerializer

### Community 42 - "Querykeyserializer.Gen"
Cohesion: 0.48
Nodes (6): isPlainObject(), JsonValue, queryKeyJsonReplacer(), serializeQueryKeyValue(), serializeSearchParams(), stringifyToJsonValue()

### Community 43 - "Package"
Cohesion: 0.33
Nodes (4): @tailwindcss/vite, @tanstack/router-plugin, vite, @vitejs/plugin-react-swc

### Community 44 - "Agents"
Cohesion: 0.40
Nodes (5): Etika Medis: Skrining Bukan Diagnosis & Privasi, Integrasi Tombol Mobile JKN, Visual Analogue Scale (VAS) Nyeri, Triage Routing & Scoring Logic, Tahap 3: Anamnesis Mendalam Dinamis (Deep-Dive HPI)

### Community 45 - "Sdk.Gen"
Cohesion: 0.40
Nodes (3): UtilsService, utilsHealthCheckData, utilsTestEmailData

### Community 46 - "Tsconfig.Build"
Cohesion: 0.50
Nodes (3): exclude, extends, ./tsconfig.json

## Knowledge Gaps
- **32 isolated node(s):** `app`, `@radix-ui/react-radio-group`, `@radix-ui/react-scroll-area`, `form-data`, `react` (+27 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 423 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `random_lower_string()` connect `Test Users` to `Random`, `Conftest`, `Items`, `Test Login`, `Test Items`?**
  _High betweenness centrality (0.281) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `User` (e.g. with `get_current_active_superuser()` and `get_current_user()`) actually correct?**
  _`User` has 23 INFERRED edges - model-reasoned connections that need verification._
- **What connects `app`, `@radix-ui/react-radio-group`, `@radix-ui/react-scroll-area` to the rest of the system?**
  _32 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Form` be split into smaller, more focused modules?**
  _Cohesion score 0.0733115468409586 - nodes in this community are weakly interconnected._
- **Why does `@playwright/test` connect `Random` to `Package`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Should `Utils` be split into smaller, more focused modules?**
  _Cohesion score 0.05311676909569798 - nodes in this community are weakly interconnected._
- **Why does `cn()` connect `Pagination` to `Form`, `Sheet`, `Routetree.Gen`, `Dropdown Menu`, `Sidebar`, `Select`, `Sidebar`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._