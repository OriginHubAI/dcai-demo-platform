# State Management

> **Standard**: Use Vue 3 Composition API with `ref`, `reactive`, and `provide`/`inject` for local and shared state. Avoid heavy state management libraries unless the complexity warrants it.

## Local Component State

- **Pattern**: Use `ref` and `computed` within individual components.
- **Goal**: Keep state localized to where it is used.

## Shared State (Global)

- **Pattern**: Use a centralized `provide`/`inject` pattern or exported reactive objects.
- **Centralized Service**: The `api.js` service acts as a single point of truth for external data, but UI state should be managed separately if it spans multiple domains.

## Data Flow

- **Fetch on Mount**: Fetch data in the `onMounted` hook of the view components.
- **Prop Drilling**: Avoid deep prop drilling by using `provide`/`inject` for state shared across a large subtree.
- **Single Source of Truth**: Ensure that state representing external data is fetched and managed in a way that avoids duplication.

## Implementation Patterns

- **Reactive Objects**: For data structures with multiple related properties, use `reactive`.
- **References**: For primitive values or individual items, use `ref`.

```javascript
// Example of a shared state composable
import { ref, provide, inject } from 'vue'

const KEY = Symbol('GlobalState')

export function provideGlobalState() {
  const state = ref({ user: null, loading: false })
  provide(KEY, state)
  return state
}

export function useGlobalState() {
  return inject(KEY)
}
```

## Anti-Patterns

- **Global State Overuse**: Don't put everything in global state. Keep UI-specific state local.
- **Direct Store Mutation**: Always use descriptive methods to update state, ensuring consistency and ease of debugging.
- **Complex Dependency Chains**: Avoid building complex, interdependent reactive chains that are difficult to trace.
