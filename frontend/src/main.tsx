import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createRouter, RouterProvider } from '@tanstack/react-router';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './api/queryClient';
import { routeTree } from './routeTree.gen';
import './index.css';

// Create the router instance with the generated route tree
const router = createRouter({
  routeTree,
  defaultPreload: 'intent',          // Prefetch on hover/focus
  defaultPreloadStaleTime: 0,        // Always use fresh data on preload
  scrollRestoration: true,
});

// Register the router for type safety across the app
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

const rootEl = document.getElementById('root');
if (!rootEl) throw new Error('Root element not found');

createRoot(rootEl).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>
);
