/**
 * Root Route
 * The top-level route wrapping all other routes.
 * Provides global providers: QueryClient, Toaster, theme class.
 */

import { createRootRoute, Outlet } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';
import { Toaster } from 'sonner';
import { useEffect } from 'react';
import { useAppStore } from '../stores/app.store';

const IS_DEV = import.meta.env.DEV;

function RootComponent() {
  const theme = useAppStore((s) => s.preferences.theme);

  // Apply theme class to <html> element
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);

  return (
    <>
      <Outlet />
      <Toaster
        position="bottom-center"
        richColors
        closeButton
        toastOptions={{
          duration: 4000,
          classNames: {
            toast: 'font-sans text-sm',
          },
        }}
      />
      {IS_DEV && <TanStackRouterDevtools position="bottom-right" />}
    </>
  );
}

export const Route = createRootRoute({
  component: RootComponent,
});
