# Frontend Directory Structure

> **Standard**: Domain-based component organization with centralized services and composables.

## Overview

```text
frontend/
├── assets/          # Global styles (Tailwind, main.css)
├── components/      # UI Components
│   ├── common/      # Reusable UI primitives (Buttons, Inputs, Badges)
│   ├── layout/      # Layout components (Header, Footer, Navbar)
│   └── [domain]/    # Domain-specific components (apps, datasets, models)
├── composables/     # Shared Vue Composition API logic (usePagination, useSearch)
├── config/          # Application configuration (API URLs, feature flags)
├── data/            # Mock data and static configuration constants
├── i18n/            # Internationalization (locales, index.js)
├── router/          # Vue Router configuration
├── services/        # API service layer (api.js)
├── views/           # Page-level components (Routes)
├── App.vue          # Root component
└── main.js          # Entry point
```

## Folder Guidelines

### `components/`
- **common/**: Components that are generic and reused across multiple domains. Examples: `StatBadge.vue`, `SearchBar.vue`.
- **layout/**: Structural components that define the app's shell. Examples: `AppHeader.vue`, `NavBar.vue`.
- **[domain]/**: Group components by their business domain. This keeps related logic together. Example: `frontend/components/apps/AppCard.vue`.

### `composables/`
- All reusable logic should be extracted here.
- File naming: `use[Name].js` (e.g., `usePagination.js`).
- Patterns: Always return reactive state and functions.

### `services/`
- Centralized API interaction.
- `api.js` is the main entry point, handling auth headers and environment switching (mock vs. real API).

### `views/`
- Components here represent top-level routes.
- Responsibility: Fetch data on mount, manage high-level page state, and orchestrate domain components.
- Naming: `[Name]Page.vue` (e.g., `AppsPage.vue`).

## Import Conventions

- Use the `@` alias for the `frontend/` directory.
- Order:
  1. Vue core (ref, computed, etc.)
  2. Libraries (vue-i18n, vue-router)
  3. Services (`@/services/...`)
  4. Composables (`@/composables/...`)
  5. Common components (`@/components/common/...`)
  6. Local/Domain components (`@/components/[domain]/...`)
