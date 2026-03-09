# API and Mock Pattern

> **Standard**: Use a centralized service layer that switches between mock data and real API calls based on project configuration.

## Service Layer (`services/api.js`)

All external interactions must be centralized in `frontend/services/api.js`. This allows for unified authentication handling and easy environment switching.

### Mock vs. Real Mode

The project uses a configuration utility to determine if it should serve mock data or call the backend API.

- **Mock Mode**: When `isMockMode()` is true, the service dynamically imports data from `frontend/data/*.js`.
- **API Mode**: When `isApiMode()` is true, it uses `fetchWithAuth` to make HTTP calls.

```javascript
/**
 * Example Pattern: Fetching tasks
 */
export const taskApi = {
  async getTasks(params = {}) {
    if (isMockMode()) {
      // Dynamic import to keep mock data out of main bundle if not needed
      const { tasks } = await import('@/data/tasks.js')
      return { list: tasks, total: tasks.length }
    }
    
    const queryParams = new URLSearchParams(params)
    const url = getApiUrl(`/tasks?${queryParams}`)
    return await fetchWithAuth(url)
  }
}
```

## Mock Data (`data/`)

Mock data is stored in the `frontend/data/` directory as simple JavaScript modules. This is essential for:
- **Local Development**: Working on the frontend before the backend is ready.
- **Testing**: Providing consistent, predictable data for UI tests.
- **Demos**: Running the frontend as a standalone prototype.

## Authentication

- **fetchWithAuth**: A generic wrapper that automatically adds the `Authorization` header if a token exists in `localStorage`.
- **Error Handling**: Standardized catching of HTTP errors with consistent logging.

## Best Practices

- **Dynamic Imports**: Always use `await import()` for mock data within service methods to ensure it's only loaded when needed.
- **Consistency**: The shape of the data returned by the mock service must match the shape of the actual API response exactly.
- **No Direct Fetching**: Never call `fetch` or `axios` directly within components or composables. Always use the service layer.
