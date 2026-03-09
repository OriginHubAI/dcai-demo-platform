# Code Quality

> **Standard**: Use ESLint and Prettier for automatic formatting and linting. Maintain high standards for accessibility and performance.

## General Principles

- **Readability**: Code should be clear and self-documenting. Use descriptive names for variables and functions.
- **Consistency**: Adhere to the project's established patterns (e.g., using `@` for imports, domain-driven component folders).
- **Simplicity**: Favor simple, direct solutions over complex ones. Avoid over-engineering.

## Linting and Formatting

- **Tooling**: Use ESLint for linting and Prettier for formatting. Ensure these tools are run before any commit.
- **Rules**: Follow the standard Vue 3 and JavaScript rules. Any exceptions should be clearly documented.

## Performance

- **Lazy Loading**: Use dynamic imports for route components to ensure faster initial load times.
- **Reactivity Optimization**: Avoid unnecessary reactive updates. Use `v-once` for static content where appropriate.
- **Asset Optimization**: Optimize images and assets before adding them to the project.

## Accessibility (A11y)

- **Semantic HTML**: Always use appropriate HTML elements (e.g., `button` for actions, `a` for links).
- **ARIA Attributes**: Use ARIA attributes where necessary to improve screen reader support.
- **Keyboard Navigation**: Ensure all interactive elements are reachable and usable via keyboard.

## Anti-Patterns

- **Unused Imports**: Always remove unused imports from your files.
- **Console Logs**: Remove any debug console logs before committing your code.
- **Direct DOM Manipulation**: Avoid using `document.querySelector` or similar methods; use Vue's template system and `ref` instead.
- **Large Component Files**: Break down components that are too large to maintain.
