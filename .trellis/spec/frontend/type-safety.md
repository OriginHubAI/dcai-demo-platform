# Data Integrity and Validation Guidelines

> Since this project uses JavaScript instead of TypeScript, we rely on Vue Prop validation, JSDoc, and runtime validation for data integrity.

---

## Vue Component Props

Always use detailed prop validation in your Vue components to act as the first line of defense against bad data:

```vue
<!-- Good: Exhaustive Prop Validation -->
<script setup>
defineProps({
  user: {
    type: Object,
    required: true,
    validator(value) {
      // Custom validation logic
      return ['id', 'name', 'role'].every(key => key in value)
    }
  },
  status: {
    type: String,
    default: 'active',
    validator(value) {
      return ['active', 'inactive', 'pending'].includes(value)
    }
  },
  onComplete: {
    type: Function,
    default: () => {}
  }
})
</script>
```

---

## Shared Constants

Avoid duplicating Magic Strings or Lists of allowed values across different components.

```javascript
// frontend/src/config/constants.js
export const TODO_STATUS = {
  OPEN: 'open',
  IN_PROGRESS: 'in_progress',
  DONE: 'done'
};

export const TODO_STATUS_OPTIONS = [
  { value: TODO_STATUS.OPEN, label: 'Open' },
  { value: TODO_STATUS.IN_PROGRESS, label: 'In Progress' },
  { value: TODO_STATUS.DONE, label: 'Done' }
];
```

Usage in a component:

```vue
<script setup>
import { TODO_STATUS_OPTIONS } from '@/config/constants'
</script>

<template>
  <select v-model="selectedStatus">
    <option v-for="option in TODO_STATUS_OPTIONS" :key="option.value" :value="option.value">
      {{ option.label }}
    </option>
  </select>
</template>
```

---

## JSDoc for Complex Data Structures

When passing complex objects throughout the application (e.g., in Composables and API Services), use JSDoc to document the expected shape. Most modern IDEs will read JSDoc and provide autocomplete.

```javascript
/**
 * @typedef {Object} User
 * @property {string} id - The unique identifier
 * @property {string} name - Full display name
 * @property {('admin'|'user'|'guest')} role - Access level
 */

/**
 * Validates and processes a user object from the API.
 * @param {User} user
 * @returns {boolean} True if valid
 */
export function processUser(user) {
  if (!user || user.role === 'guest') return false;
  // ...
  return true;
}
```

---

## API Response Validation

Never trust API responses blindly. If the frontend entirely depends on an expected data structure, safely fallback if it is missing:

```javascript
// Good - Safe Optional Chaining & Defaulting
const userName = response?.data?.user?.name ?? 'Unknown User';

// Bad - Assumes structure exists
const userName = response.data.user.name; // Crashes if user is null
```

For critical data flows (such as configuration loading or highly complex forms), consider using a runtime validation library like `Zod` to parse the object safely before passing it to internal components.

---

**Language**: All documentation must be written in **English**.
