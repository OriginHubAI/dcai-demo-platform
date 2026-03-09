# Type Safety

> **Standard**: Use Vue 3 `defineProps` for component validation and JSDoc for functions. This project uses JavaScript, but we aim for high type clarity.

## Prop Validation

- **Explicit Types**: Use `String`, `Number`, `Boolean`, `Object`, `Array`, or `Function` for prop definitions.
- **Requirements**: Specify `required: true` for all essential props.
- **Defaults**: Provide sensible default values for optional props.

```javascript
const props = defineProps({
  id: { type: String, required: true },
  items: { type: Array, default: () => [] },
  onUpdate: { type: Function, default: null }
})
```

## Function Annotations (JSDoc)

- **Annotation**: Use JSDoc to describe function parameters and return types.
- **Description**: Add a brief description for complex logic.

```javascript
/**
 * Fetches items from the API.
 * @param {Object} params - Query parameters.
 * @param {string} params.type - Filter by item type.
 * @returns {Promise<Array>} List of items.
 */
async function fetchItems(params) {
  // implementation
}
```

## Anti-Patterns

- **Implicit Types**: Avoid using props without explicit type validation.
- **Untyped Objects**: For complex prop objects, provide detailed comments or use a structured JSDoc `@typedef` if necessary.
- **Lack of Documentation**: For any non-trivial function, always include JSDoc to help future maintainers.
- **Prop Overloading**: Keep prop objects simple. If a component needs too many properties, consider passing a single, well-defined object.
