# Decentrathon Frontend

Frontend app bootstrapped with Vite + React + TypeScript, with routing, Tailwind CSS v4, and shadcn/ui primitives.

## Stack

- React 19
- TypeScript 5
- Vite 8
- React Router 7
- Tailwind CSS 4
- shadcn/ui + Base UI
- TanStack Query (installed and ready for data fetching)

## Prerequisites

- Node.js 20+
- npm 10+

## Getting Started

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Open the local URL printed by Vite (usually `http://localhost:5173`).

## Available Scripts

- `npm run dev` - Start Vite dev server with HMR
- `npm run build` - Type-check and build for production
- `npm run preview` - Preview the production build locally
- `npm run lint` - Run ESLint

## Project Structure

```text
frontend/
  public/
  src/
    components/
      ui/
    lib/
    pages/
    App.tsx
    index.css
    main.tsx
  components.json
  vite.config.ts
  tsconfig.json
  package.json
```

## Routing

Routing is configured in `src/main.tsx` using `createBrowserRouter` and `RouterProvider`.

## UI and Styling

- Global styles and design tokens live in `src/index.css`.
- shadcn configuration is defined in `components.json`.
- The `@` alias maps to `src/` (configured in `vite.config.ts`).

## Notes

- React Compiler support is enabled through the Vite + Babel plugin setup.
- `src/pages/` is currently empty and ready for route-based pages.
