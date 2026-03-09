# State Management

> Best practices for managing state in Vue 3 using the native Reactivity API.

---

## Overview

We avoid heavy external state management libraries (like Vuex or Pinia) for simplicity. Instead, we use Vue 3's native Reactivity API (`ref`, `reactive`, `computed`) integrated either through **Composables** (for singleton global state) or **Dependency Injection** (`provide` / `inject`) when state needs to be scoped to a component tree.

---

## Global Singleton State (External Reactivity)

When you need application-wide state (like User Authentication status or Theme Preference), you can create reactive variables outside of any component instance in a standard JavaScript file, and export a composable function to interact with it.

```javascript
// src/composables/useAuth.js
import { ref, computed } from 'vue'
import { AuthService } from '../services/auth.service'

// State defined *outside* the function acts as a global singleton
const user = ref(null)
const isAuthenticated = ref(false)
const isLoading = ref(true)

export function useAuth() {
  const login = async (credentials) => {
    isLoading.value = true
    try {
      const response = await AuthService.login(credentials)
      user.value = response.user
      isAuthenticated.value = true
    } catch (e) {
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    await AuthService.logout()
    user.value = null
    isAuthenticated.value = false
  }

  return {
    // Expose readonly computed properties if you want to prevent direct mutation
    user: computed(() => user.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    isLoading: computed(() => isLoading.value),
    login,
    logout
  }
}
```

### Usage in Component

```vue
<script setup>
import { useAuth } from '@/composables/useAuth'

const { user, isAuthenticated, login, logout } = useAuth()
</script>

<template>
  <div v-if="isAuthenticated">
    <p>Welcome, {{ user.name }}</p>
    <button @click="logout">Logout</button>
  </div>
  <div v-else>
    <button @click="login({ username: 'test', password: '123' })">Login</button>
  </div>
</template>
```

---

## Scoped State (Provide / Inject)

When state should exist per-instance of a complex component or subtree (e.g., a multi-step wizard, or a DataGrid with filters and pagination), use Vue's `provide` and `inject` API. This prevents global pollution and correctly lifecycle-scopes the data.

### 1. Create a Provider context

Create an injection key and a setup function to encapsulate the logic:

```javascript
// src/composables/useDataGridState.js
import { ref, reactive, provide, inject } from 'vue'

const DataGridStateKey = Symbol('DataGridState')

export function createDataGridState() {
  const filters = reactive({ search: '', status: 'all' })
  const page = ref(1)

  const resetFilters = () => {
    filters.search = ''
    filters.status = 'all'
    page.value = 1
  }

  const state = {
    filters,
    page,
    resetFilters
  }

  provide(DataGridStateKey, state)

  return state
}

export function useDataGridState() {
  const state = inject(DataGridStateKey)
  if (!state) {
    throw new Error('useDataGridState requires createDataGridState to be called in a parent component.')
  }
  return state
}
```

### 2. Provide the state in the parent

```vue
<!-- DataGridWrapper.vue -->
<script setup>
import { createDataGridState } from '@/composables/useDataGridState'
import DataGridToolbar from './DataGridToolbar.vue'
import DataGridTable from './DataGridTable.vue'

// Initializes the state and provides it to all children
createDataGridState()
</script>

<template>
  <div class="data-grid-wrapper">
    <DataGridToolbar />
    <DataGridTable />
  </div>
</template>
```

### 3. Inject the state in children

```vue
<!-- DataGridToolbar.vue -->
<script setup>
import { useDataGridState } from '@/composables/useDataGridState'

const { filters, resetFilters } = useDataGridState()
</script>

<template>
  <div class="toolbar">
    <input v-model="filters.search" placeholder="Search..." />
    <button @click="resetFilters">Reset</button>
  </div>
</template>
```

---

## State Organization Summary

| State Type                    | Where to Store                     | Example |
| ----------------------------- | ---------------------------------- | ------- |
| **Component Local Data**      | `<script setup>` variables (`ref`) | Form input values, local dialog visibility |
| **Global Singleton Data**     | Exported from Composable file      | Authentication status, Theme Preference, Global Notifications |
| **Complex Subtree Logic**     | `provide` / `inject` Context       | Multi-step forms, complex DataGrid components |
| **Data Fetching / Caching**   | Local component OR Composables     | Wrapping `useFetch` to handle `loading`, `data`, `error` states |

---

**Language**: All documentation must be written in **English**.
