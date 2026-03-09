# Code Quality Guidelines

> Performance and code quality standards.

---

## Package Manager

**Use npm**:

```bash
# Good
npm install
npm run lint

# Avoid mixing package managers
pnpm install  # Don't
yarn install  # Don't
```

---

## Before Every Commit

Run these checks before committing:

```bash
# 1. Lint
npm run lint

# 2. Manual testing
# Test the feature you changed visually inside the browser.
```

**Checklist**:

- [ ] `npm run lint` - 0 errors, 0 warnings
- [ ] Manual testing passes
- [ ] No console errors in Browser DevTools

---

## Vue 3 Specific Quality Rules

### Keying `v-for` loops

Always provide a unique `:key` attribute when using `v-for`. Never use the array `index` as the key if the array elements can be reordered, added, or deleted.

```vue
<!-- Good -->
<li v-for="item in items" :key="item.id">{{ item.name }}</li>

<!-- Bad -->
<li v-for="(item, index) in items" :key="index">{{ item.name }}</li>
```

### Avoiding `v-if` with `v-for`

**Never use `v-if` on the same element as `v-for`.** Vue 3 evaluates `v-if` BEFORE `v-for`, so the `v-if` condition will not have access to the loop variable.

```vue
<!-- Good: Filter in a computed property -->
<li v-for="activeItem in computedActiveItems" :key="activeItem.id">...</li>

<!-- Good: Use a wrapper <template> for the loop -->
<template v-for="item in items" :key="item.id">
  <li v-if="item.isActive">...</li>
</template>

<!-- Bad -->
<li v-for="item in items" v-if="item.isActive" :key="item.id">...</li>
```

---

## Clean Up Unused Imports & Dead Code

After refactoring, always check for and remove unused imports and commented-out blocks of old code:

```javascript
// Bad - dead code
import { oldFunction } from '../services/api';
// oldFunction();

// Good - only import what you use
import { newFunction } from '../services/api';
```

**Tip**: The linter is configured to catch unused variables and imports.

---

## Performance Guidelines

### Computed Properties vs Methods

Use `computed` for derived data that should be cached. Only use methods for actions or calculations that truly need to run on every render.

```javascript
// Good: Cached until 'items' changes
const activeItemsCount = computed(() => {
  return items.value.filter(i => i.active).length
})

// Bad: Re-evaluates every time the component updates for unrelated reasons
const getActiveItemsCount = () => {
  return items.value.filter(i => i.active).length
}
```

### Debounce Expensive Operations

```javascript
// Using lodash-es or similar for debounce
import { debounce } from 'lodash-es'
import { watch, ref } from 'vue'

const searchQuery = ref('')

// Debounce the API call
const fetchResults = debounce((query) => {
  api.search(query)
}, 300)

watch(searchQuery, (newQuery) => {
  fetchResults(newQuery)
})
```

---

## Component Organization

### File Length

- **Vue Components**: Max ~300 lines. Break large templates into smaller child components.
- **Composables**: Max ~150 lines. Extract pure JS helper functions.

### Function Length

- Keep JS functions under 50 lines when possible
- Extract helper functions for complex logic
- Use descriptive names for extracted functions (`preparePayload`, `formatDate`)

---

## Error Handling

### API Calls

Handle errors gracefully entirely to prevent the application from crashing.

```javascript
// Good - handle errors explicitly
try {
  const result = await api.fetchData();
  data.value = result;
} catch (error) {
  console.error('Unexpected error:', error);
  // Show a toast notification to the user
  toast.error('Failed to fetch data');
} finally {
  isLoading.value = false;
}
```

---

**Language**: All documentation must be written in **English**.
