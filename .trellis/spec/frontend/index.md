# Vue 3 + Tailwind Frontend Development Guidelines

> Universal frontend development guidelines for internal applications with Vue 3 + Vite + Tailwind CSS.

## Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Language**: JavaScript
- **Styling**: Tailwind CSS
- **Routing**: Vue Router 4
- **State Management**: Vue Reactivity API (`ref`, `reactive`, `provide`/`inject`) / Composables

---

## Documentation Files

| File                                                                           | Description                                     | Priority      |
| ------------------------------------------------------------------------------ | ----------------------------------------------- | ------------- |
| [vue-pitfalls.md](./vue-pitfalls.md)                                           | Critical Vue patterns and common mistakes       | **Must Read** |
| [composables.md](./composables.md)                                             | Creating and using Vue Composables              | Reference     |
| [state-management.md](./state-management.md)                                   | Shared state, layout, navigation patterns       | Reference     |
| [components.md](./components.md)                                               | Semantic HTML, empty states, scrollbar patterns | Reference     |
| [type-safety.md](./type-safety.md)                                             | Prop validation, JSDoc, and data structures     | Reference     |
| [directory-structure.md](./directory-structure.md)                             | Project structure conventions                   | Reference     |
| [css-design.md](./css-design.md)                                               | Tailwind styling and design tokens              | Reference     |
| [quality.md](./quality.md)                                                     | Code quality and performance standards          | Reference     |

---

## Quick Navigation by Task

### Before Starting Development

| Task                         | Document                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------ |
| Avoid common Vue mistakes    | [vue-pitfalls.md](./vue-pitfalls.md)                                           |

### During Development

| Task                     | Document                                     |
| ------------------------ | -------------------------------------------- |
| Create reusable logic    | [composables.md](./composables.md)           |
| Manage application state | [state-management.md](./state-management.md) |
| Build UI components      | [components.md](./components.md)             |
| Ensure data validity     | [type-safety.md](./type-safety.md)           |

### Before Committing

| Task                    | Document                         |
| ----------------------- | -------------------------------- |
| Check code quality      | [quality.md](./quality.md)       |
| Verify CSS organization | [css-design.md](./css-design.md) |

---

## Core Rules Summary

| Rule                                                         | Reference                                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Always use `.value` for refs** in JS                       | [vue-pitfalls.md](./vue-pitfalls.md)                                           |
| **Do not destructure props directly** without `toRefs`       | [vue-pitfalls.md](./vue-pitfalls.md)                                           |
| **Use `<script setup>` syntax**                              | [components.md](./components.md)                                               |
| **Provide keys in `v-for`**                                  | [quality.md](./quality.md)                                                     |
| **No non-null assertions or reckless `.value` assignments**  | [quality.md](./quality.md)                                                     |
| **Use `scrollbar-gutter: stable`** for scrollable containers | [components.md](./components.md)                                               |

---

## Architecture Overview

```text
+----------------------------------------------------------+
|                      Vue 3 App                           |
|  +--------------+  +--------------+  +-----------------+ |
|  |   App.vue    |  |  Vue Router  |  |    Services     | |
|  | (Layout Root)|  |  (Navigation)|  |  (API Calls)    | |
|  +------+-------+  +------+-------+  +--------+--------+ |
+---------|-----------------|-------------------|----------+
          |                 |                   |
          v                 v                   v
+---------+-----------------+-------------------+----------+
|  +----------------+   +-------------------+              |
|  |     Views      |   |    Composables    |              |
|  | (Page Modules) |<--| (Reusable Logic/  |              |
|  +-------+--------+   |  State Management)|              |
|          |            +-------------------+              |
|          v                                               |
|  +----------------+                                      |
|  |   Components   |                                      |
|  | (UI Elements)  |                                      |
|  +----------------+                                      |
+----------------------------------------------------------+
```

---

## Getting Started

1. **Read the Must-Read documents** - Especially Vue pitfalls
2. **Set up your project structure** - Follow [directory-structure.md](./directory-structure.md)
3. **Build Vue Composables** - Use patterns from [composables.md](./composables.md)
4. **Build components** - Follow [components.md](./components.md) properly structured with `<script setup>`, `<template>`, and Tailwind utilities.

---

**Language**: All documentation is written in **English**.
