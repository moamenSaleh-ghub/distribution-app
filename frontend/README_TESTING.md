# Frontend Testing Guide

## Setup

Install test dependencies:

```bash
cd frontend
npm install
```

## Running Tests

Run all tests:
```bash
npm test
```

Run tests in watch mode:
```bash
npm test -- --watch
```

Run tests with UI:
```bash
npm run test:ui
```

Run tests with coverage:
```bash
npm run test:coverage
```

## Test Structure

- `src/test/setup.js` - Test configuration and setup
- `src/test/api.test.js` - API client tests
- `src/test/components/` - Component tests
  - `ProductForm.test.jsx`
  - `CustomerForm.test.jsx`
  - `ProductTable.test.jsx`
  - `CustomerTable.test.jsx`

## Test Coverage

Tests cover:
- ✅ API client functions (GET, POST, PATCH)
- ✅ React components (rendering, user interactions)
- ✅ Form submissions and validation
- ✅ Error handling

## Testing Library

We use:
- **Vitest** - Test runner (compatible with Vite)
- **@testing-library/react** - React component testing
- **@testing-library/jest-dom** - DOM matchers
- **@testing-library/user-event** - User interaction simulation

