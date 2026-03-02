/**
 * ThemeToggle
 * Moon/sun icon button. Reads and writes to AppStore.preferences.theme.
 */

import { Moon, Sun } from 'lucide-react';
import { useAppStore } from '../../stores/app.store';
import { Button } from '../ui/button';
import { Tooltip } from '../ui/tooltip';

export function ThemeToggle() {
  const theme = useAppStore((s) => s.preferences.theme);
  const setTheme = useAppStore((s) => s.setTheme);

  const isDark = theme === 'dark';

  return (
    <Tooltip content={isDark ? 'Switch to light mode' : 'Switch to dark mode'} side="right">
      <Button
        variant="ghost"
        size="icon"
        aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
        onClick={() => setTheme(isDark ? 'light' : 'dark')}
      >
        {isDark ? (
          <Sun className="w-4 h-4" />
        ) : (
          <Moon className="w-4 h-4" />
        )}
      </Button>
    </Tooltip>
  );
}
