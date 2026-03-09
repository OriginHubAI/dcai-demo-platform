# Component Guidelines

> **Standard**: Use Vue 3 `<script setup>` syntax with Tailwind CSS utility classes.

## General Principles

- **Small and Focused**: Components should have a single responsibility.
- **Dumb Components**: Prefer functional components that only render data passed via props.
- **Consistent Structure**: Keep `<template>`, `<script setup>`, and `<style>` (if any) in that order.

## Prop Conventions

- **Definition**: Always use `defineProps` with explicit types and defaults.
- **Naming**: Use camelCase for prop names (e.g., `showStatus`).
- **Validation**: Use required or default values to ensure component stability.

```javascript
const props = defineProps({
  app: { type: Object, required: true },
  showDescription: { type: Boolean, default: true }
})
```

## Template Patterns

- **Tailwind Classes**: Use utility classes directly in the template. Avoid custom CSS unless absolutely necessary.
- **Dynamic Classes**: Use object or array syntax for clarity.
- **v-i18n**: Always use `$t` for text content to ensure localization support.

```html
<template>
  <div :class="[
    'p-4 rounded-lg border',
    isActive ? 'border-blue-500' : 'border-gray-200'
  ]">
    <h3 class="text-lg font-bold">{{ $t('common.title') }}</h3>
  </div>
</template>
```

## Logic Patterns

- **Computed Properties**: Use `computed` for all derived state from props or reactive variables.
- **Reactivity**: Use `ref` for primitive state and `reactive` for complex objects only when necessary.
- **Emits**: Use `defineEmits` for child-to-parent communication.

## Examples

### Good Component Pattern
- Uses `StatBadge.vue` as a reference for a small, reusable primitive.
- Uses `AppCard.vue` as a reference for a domain component that composes smaller components.

## Anti-Patterns

- **Direct Prop Modification**: Never modify props inside the component. Use events or local state instead.
- **Large Templates**: If a template exceeds 200 lines, consider breaking it into smaller sub-components.
- **Complex Logic in Templates**: Keep template expressions simple. Move logic to `computed` properties.
- **Hardcoded Strings**: Avoid using hardcoded strings for text; use the i18n system.
