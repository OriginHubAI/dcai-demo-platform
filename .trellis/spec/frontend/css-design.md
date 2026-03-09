# CSS & Design System

> Tailwind CSS conventions and design tokens for Vue 3 applications.

---

## Tailwind First

This project relies entirely on **Tailwind CSS** for styling. We prioritize writing utility classes directly in the `<template>` of our Vue components rather than creating custom CSS modules or BEM classes.

```vue
<!-- Good: Tailwind utilities -->
<template>
  <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
    Submit
  </button>
</template>

<!-- Bad: Extracting basic styles to custom CSS -->
<template>
  <button class="btn btn-primary">Submit</button>
</template>
<style scoped>
.btn.btn-primary { ... }
</style>
```

---

## Design Tokens

If there are project-wide tokens (like custom colors or spacing), configure them inside `tailwind.config.js` to ensure consistency. Use the native CSS approach for dynamically changing these tokens (e.g., for dark mode).

### CSS Custom Properties

Define root variables (e.g., HSL formatted for Tailwind compatibility) in the main entry CSS file:

```css
/* frontend/assets/main.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Colors */
    --color-background: 0 0% 100%;
    --color-foreground: 20 14% 4%;
    --color-primary: 24 10% 10%;
    --color-primary-foreground: 60 9% 98%;
  }

  .dark {
    --color-background: 20 14% 4%;
    --color-foreground: 60 9% 98%;
    --color-primary: 60 9% 98%;
    --color-primary-foreground: 24 10% 10%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### Extending Tailwind Theme

Map these CSS variables inside `tailwind.config.js`:

```javascript
// frontend/tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--color-background))",
        foreground: "hsl(var(--color-foreground))",
        primary: {
          DEFAULT: "hsl(var(--color-primary))",
          foreground: "hsl(var(--color-primary-foreground))",
        },
      },
    },
  },
  plugins: [],
}
```

---

## When to use Custom CSS

In rare instances where complex custom behavior cannot be achieved via Tailwind, place scoped CSS inside the Vue component:

```vue
<template>
  <div class="complex-animation-box relative">...</div>
</template>

<style scoped>
.complex-animation-box {
  /* Complex clip paths or custom keyframes not supported by tailwind easily */
}
</style>
```

When building globally reusable components where repetitive Tailwind classes become a burden, you can use the `@apply` directive within `main.css`, but this should be kept to an absolute minimum.

---

## Base Styles

### Typography

By default, Tailwind's preflight solves most typography normalization challenges. The `main.css` file can specify a default font family by updating the base layer:

```css
@layer base {
  html {
    font-family: 'Inter', system-ui, sans-serif;
  }
}
```

### Focus States

Use Tailwind's `focus-visible:` modifier to provide focus rings only to keyboard users:

```html
<button class="focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2">
  Action
</button>
```

---

## Scrollbars (Notion-style)

Scrollbars should be styled using custom global CSS inside `main.css` to override webkit defaults:

```css
/* frontend/assets/main.css */

/* Hide scrollbars by default, show on hover */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--color-foreground) / 0);
  border-radius: 5px;
  transition: background 0.4s ease;
}

/* Show on container hover */
.scrollable:hover::-webkit-scrollbar-thumb {
  background: hsl(var(--color-foreground) / 0.12);
  transition: background 0.15s ease;
}

/* Darker on scrollbar hover */
.scrollable::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--color-foreground) / 0.22);
}

/* Even darker when dragging */
.scrollable::-webkit-scrollbar-thumb:active {
  background: hsl(var(--color-foreground) / 0.32);
}
```

---

## Quick Reference

| Style Need                       | Approach                              |
| -------------------------------- | ------------------------------------- |
| Colors / Standard Spacing        | Utility classes (`bg-blue-500 px-4`)  |
| Custom Design System Colors      | Modify `tailwind.config.js`           |
| Complex logic/pseudo-elements    | `<style scoped>` within Vue SFC       |
| Global defaults (font, scrollbar)| Place in `frontend/assets/main.css`   |

---

**Language**: All documentation must be written in **English**.
