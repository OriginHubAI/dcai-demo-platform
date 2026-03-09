# Composable Guidelines

> **Standard**: Use Vue Composition API to encapsulate and reuse logic.

## General Principles

- **Naming**: Use camelCase with `use` prefix (e.g., `usePagination`).
- **Input Parameters**: Accept reactive references when necessary to ensure reactivity.
- **Output Structure**: Always return an object containing reactive state and functions.

## Implementation Patterns

- **Initialization**: Declare reactive state (`ref`, `reactive`) within the composable.
- **Side Effects**: Use `onMounted`, `watch`, or `onUnmounted` for internal side effects.
- **Communication**: Composables can call other composables to build complex logic.

```javascript
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  const increment = () => count.value++
  
  return { count, increment }
}
```

## Advanced Patterns

- **Watchers**: If the logic depends on an external reactive source, pass it as a `ref` or `computed`.
- **Global State**: For shared state across many components, use the `provide`/`inject` pattern within a top-level composable.

## Examples

### Good Composable Pattern
- `usePagination.js`: Encapsulates logic for dividing a list of items into pages.
- `useSearch.js`: Handles search input and filters based on a query.

## Anti-Patterns

- **Side Effects on Call**: Avoid performing side effects directly in the body of the composable. Use lifecycle hooks instead.
- **Large Composables**: If a composable handles too many responsibilities, break it into smaller, more focused units.
- **Direct Global State Mutation**: Never mutate global state directly without a formal update mechanism (e.g., a function returned by the composable).
- **Naming Conflicts**: Ensure return names are unique and descriptive to avoid conflicts in the component using them.
