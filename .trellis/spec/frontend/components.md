# Component Guidelines

> Semantic HTML, empty states, and scrollbar patterns for Vue 3 Single File Components (SFCs).

---

## Vue 3 SFC Structure

Always use the `<script setup>` syntax for defining components, followed by the `<template>`. Place `<style scoped>` at the bottom only if custom CSS is strictly necessary (prefer Tailwind utilities).

```vue
<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['click'])

function handleClick() {
  emit('click')
}
</script>

<template>
  <button @click="handleClick" class="px-4 py-2 bg-blue-500 rounded text-white">
    {{ title }}
  </button>
</template>
```

---

## Semantic HTML

Use proper HTML elements for accessibility and native browser behavior:

```vue
<!-- Good -->
<template>
  <button @click="handleClick">Click me</button>
</template>

<!-- Bad -->
<template>
  <div role="button" @click="handleClick">Click me</div>
</template>
```

### Exception: Nested Interactive Elements

HTML does not allow `<button>` inside `<button>`. When a clickable card contains nested buttons (e.g., delete button), use `<div role="button">` for the outer container:

```vue
<!-- Good - Card with nested delete button -->
<template>
  <div
    role="button"
    tabindex="0"
    @click="onClick(item)"
    @keydown.enter.prevent="onClick(item)"
    @keydown.space.prevent="onClick(item)"
    class="cursor-pointer focus-ring px-4 py-3"
  >
    <span>{{ item.title }}</span>
    <button @click.stop="onDelete(item.id)">
      Delete
    </button>
  </div>
</template>

<!-- Bad - Nested buttons cause hydration errors -->
<template>
  <button @click="onClick(item)">
    <span>{{ item.title }}</span>
    <button @click.stop="onDelete">Delete</button> <!-- ERROR: button inside button -->
  </button>
</template>
```

**Required attributes for `<div role="button">`:**

- `role="button"` - Accessibility role
- `tabindex="0"` - Make it focusable
- `@keydown.enter.prevent` / `@keydown.space.prevent` - Handle Enter/Space keys (Vue event modifiers make this easy)
- `cursor-pointer` - Visual affordance

---

## Empty State Visual Centering

When displaying empty states in flex-column layouts with headers, use negative margin to achieve visual centering:

```vue
<!-- Good - Visual centering with negative margin offset -->
<template>
  <div v-if="!isLoading && items.length === 0" class="flex-1 flex items-center justify-center">
    <div class="-mt-24">
      <EmptyState />
    </div>
  </div>
</template>

<!-- Bad - Mathematical centering looks "off" visually -->
<template>
  <div v-if="!isLoading && items.length === 0" class="flex-1 flex items-center justify-center">
    <EmptyState />
  </div>
</template>
```

**Why this pattern?**

- `flex-1 items-center` centers content in the **remaining space** below the header
- This creates mathematically correct but visually awkward positioning
- Negative margin (`-mt-24` to `-mt-32`) offsets the content upward for better visual balance

**Offset Guidelines:**

| Page Type                   | Offset   | Reason                               |
| --------------------------- | -------- | ------------------------------------ |
| Standard page header        | `-mt-24` | Compensates for ~80px header         |
| Header + action button/form | `-mt-32` | Additional offset for extra elements |

---

## Preventing Scrollbar Layout Shift

When a scrollable container's content grows to require a scrollbar, the scrollbar appearance can cause layout shift (content "jumps" left as scrollbar takes up space).

**Solution**: Use `scrollbar-gutter: stable` to reserve space for the scrollbar.

```vue
<!-- Good - Scrollbar space is always reserved -->
<template>
  <main
    class="flex-1 overflow-y-auto p-6"
    style="scrollbar-gutter: stable;"
  >
    <slot />
  </main>
</template>

<!-- Bad - Content shifts when scrollbar appears/disappears -->
<template>
  <main class="flex-1 overflow-y-auto p-6">
    <slot />
  </main>
</template>
```

---

## Scrollbar Auto-Hide (Notion-inspired)

Scrollbars should be invisible by default and fade in/out smoothly on hover. This follows Notion's design language.

**Implementation (CSS)** (Add to global styles or `main.css`):

```css
/* Global scrollbar styles */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--foreground) / 0);
  border-radius: 5px;
  transition: background 0.4s ease;
}

/* Show on container hover */
.scrollable:hover::-webkit-scrollbar-thumb {
  background: hsl(var(--foreground) / 0.12);
  transition: background 0.15s ease;
}

/* Darker on scrollbar hover */
.scrollable::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--foreground) / 0.22);
}

/* Even darker when dragging */
.scrollable::-webkit-scrollbar-thumb:active {
  background: hsl(var(--foreground) / 0.32);
}
```

---

## Quick Reference

| Pattern                    | When to Use                 |
| -------------------------- | --------------------------- |
| `role="button"` + tabindex | Nested interactive elements |
| `-mt-24` offset            | Empty state centering       |
| `scrollbar-gutter: stable` | Prevent layout shift        |
| Auto-hide scrollbar        | Any scrollable container    |

---

**Language**: All documentation must be written in **English**.
