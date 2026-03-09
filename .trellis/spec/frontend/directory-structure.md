# Directory Structure

> Project structure conventions for the Vue 3 Frontend application.

---

## Recommended Directory Structure

The `frontend/` directory organizes code by technical concern and domain.

```text
frontend/
├── index.html                # HTML entry point for Vite
├── package.json              # Dependencies and scripts
├── vite.config.js            # Vite bundler configuration
├── tailwind.config.js        # Tailwind CSS configuration
│
├── public/                   # Static assets (favicons, etc.)
│   └── favicon.ico
│
└── src/                      # Source code
    ├── main.js               # Application bootstrap (mounts App.vue)
    ├── App.vue               # Root application layout component
    │
    ├── assets/               # Local static assets and global CSS
    │   ├── main.css          # Tailwind and global styles
    │   └── images/
    │
    ├── components/           # Reusable Vue components
    │   ├── common/           # Generic UI components (Buttons, Inputs)
    │   ├── layout/           # Shared page wrappers (Header, Sidebar)
    │   └── domains/          # Domain-specific components
    │       ├── apps/
    │       ├── datasets/     
    │       └── models/
    │
    ├── composables/          # Vue Composition API logic (hooks)
    │   ├── useAuth.js
    │   ├── useFetch.js
    │   └── ...
    │
    ├── config/               # App configuration (API endpoints, constants)
    │   └── constants.js
    │
    ├── i18n/                 # Internationalization logic
    │   ├── index.js          # Vue i18n setup
    │   └── locales/          # Translation dictionaries (en.json, zh.json)
    │
    ├── router/               # Vue Router configuration
    │   └── index.js          # Route definitions
    │
    ├── services/             # API layer (fetch wrappers, Axios config)
    │   ├── api.js            # Core networking client
    │   ├── auth.service.js
    │   └── dataset.service.js
    │
    └── views/                # Full page views (routed components)
        ├── HomeView.vue
        ├── DatasetListView.vue
        ├── ModelDetailView.vue
        └── ...
```

---

## Component Organization

### Reusable UI (`components/common/`)

Dumb, presentation components that do not fetch their own data or access global state. They rely entirely on `props` and standard Vue events (`emit`).

### Domain Components (`components/domains/`)

Reusable chunks of UI that belong to a specific feature area but aren't full pages. They may contain domain-specific logic or connect directly to API services if appropriate.

### Page Views (`views/`)

Components loaded by Vue Router. These fetch the primary data needed for the route and orchestrate domain components.

---

## Logic Organization (Composables)

Shared stateful logic is extracted into **Composables** (`composables/`). This encapsulates reactivity (`ref`, `reactive`), lifecycle hooks (`onMounted`), and effects (`watch`).

Names should always start with `use`, e.g., `useAuth.js`, `usePagination.js`.

---

## Networking and API Layer (`services/`)

To keep Vue components clean, network requests and data transformations belong in `services/`.

1. **`api.js`**: Configures the base HTTP client (e.g., handling auth tokens, interceptors).
2. **Domain services (e.g., `model.service.js`)**: Exports functions that components can call to load or submit data.

```javascript
// Example service structure
import api from './api';

export const ModelService = {
  getModels(params) {
    return api.get('/api/v2/models', { params });
  },
  getModelDetail(id) {
    return api.get(`/api/v2/models/${id}`);
  }
};
```

---

## State Management

Instead of external libraries like Pinia or Redux, global state is managed natively using Vue's Reactivity API. This is usually implemented via the Provider pattern (using `provide`/`inject`) or via shared Reactive State exported from a Composable module.

*(See [state-management.md](./state-management.md) for details)*

---

**Language**: All documentation must be written in **English**.
