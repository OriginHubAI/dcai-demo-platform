# Composables Guidelines

> Patterns for creating and using reusable Vue 3 logic.

---

## What is a Composable?

A "composable" is a function that leverages Vue Composition API (`ref`, `reactive`, `watch`, `computed`, lifecycle hooks) to encapsulate and reuse stateful logic.

This replaces "Hooks" from React and "Mixins" from Vue 2.

---

## Naming Conventions

Always start composables with `use`:

- `useAuth`
- `usePagination`
- `useFetch`
- `useEventListener`

---

## Basic Structure

A composable is just a plain javascript function that sets up localized state or connects to global state, and returns values/functions.

```javascript
// frontend/src/composables/useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  // 1. Define State
  const count = ref(initialValue)

  // 2. Define Computed properties
  const doubleCount = computed(() => count.value * 2)

  // 3. Define Methods
  const increment = () => {
    count.value++
  }
  const decrement = () => {
    count.value--
  }

  // 4. Return API
  return {
    count,
    doubleCount,
    increment,
    decrement
  }
}
```

---

## Handling Arguments (Flexible refs)

When a composable takes arguments, it should be designed to accept both raw primitive values OR reactive `refs`. This makes the composable significantly more flexible.

Use `toValue` (Vue 3.3+) or `unref` to conditionally unwrap the input:

```javascript
import { ref, watchEffect, unref } from 'vue'

// Accepts a string OR a ref containing a string
export function useFormatDate(dateStringRef) {
  const formattedDate = ref('')

  // Will re-run if dateStringRef is a reactive reference and its inner value changes
  watchEffect(() => {
    const rawValue = unref(dateStringRef) // unwraps if it's a ref, otherwise returns as-is
    if (rawValue) {
      formattedDate.value = new Date(rawValue).toLocaleDateString()
    }
  })

  return { formattedDate }
}
```

---

## Cleanup in Composables

If your composable establishes external connections, setups up intervals, or listens to DOM events, it MUST register its own teardown logic using `onUnmounted`. 

Because composables run synchronously inside `<script setup>`, the `onUnmounted` hook correctly binds to the component that called the composable.

```javascript
import { onMounted, onUnmounted } from 'vue'

export function useEventListener(target, event, callback) {
  onMounted(() => {
    target.addEventListener(event, callback)
  })

  // Automatically cleans up when the host component unmounts
  onUnmounted(() => {
    target.removeEventListener(event, callback)
  })
}
```

---

## Return Refs Object, NOT Reactive Objects

From composables, always return a plain javascript object containing `refs`, rather than a single `reactive` object.

```javascript
// GOOD: Returning a plain object of refs
export function useUserData() {
  const id = ref(1)
  const name = ref('Alice')
  
  return { id, name }
}

// In component:
// This works perfectly, reactivity is maintained!
const { id, name } = useUserData() 
```

If you returned a `reactive()` proxy, the destructuring assignment in the component would destroy the reactivity.

```javascript
// BAD: Returning a reactive object
export function useUserDataBad() {
  const state = reactive({ id: 1, name: 'Alice' })
  return state
}

// In component:
// THIS LOSES REACTIVITY
const { id, name } = useUserDataBad() 
```

---

## Global State via Composables

To share state across multiple independent components, hoist the state definitions *outside* the exported function.

```javascript
// src/composables/useTheme.js
import { ref, watchEffect } from 'vue'

// Shared across all component instances importing this file
const currentTheme = ref('light')

export function useTheme() {
  // Local logic
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light'
  }

  // Effect will run for each component, but react to the single global ref
  watchEffect(() => {
    document.body.className = currentTheme.value
  })

  return {
    currentTheme,
    toggleTheme
  }
}
```

---

**Language**: All documentation must be written in **English**.
