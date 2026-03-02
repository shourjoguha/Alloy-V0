/**
 * Settings Route (/settings)
 * User preferences: appearance, units, defaults, reset.
 */

import { createFileRoute } from '@tanstack/react-router';
import { toast } from 'sonner';
import { Moon, Sun, RotateCcw } from 'lucide-react';
import { PageContainer } from '../../components/layout/PageContainer';
import { ErrorBoundary } from '../../components/shared/ErrorBoundary';
import { useAppStore } from '../../stores/app.store';
import { cn } from '../../lib/utils';

export const Route = createFileRoute('/_app/settings')({
  component: () => (
    <ErrorBoundary scope="Settings">
      <SettingsPage />
    </ErrorBoundary>
  ),
});

function SettingsPage() {
  const prefs = useAppStore((s) => s.preferences);
  const age = useAppStore((s) => s.age);
  const gender = useAppStore((s) => s.gender);
  const setTheme = useAppStore((s) => s.setTheme);
  const setWeightUnit = useAppStore((s) => s.setWeightUnit);
  const setDistanceUnit = useAppStore((s) => s.setDistanceUnit);
  const setDefaultBodyMapView = useAppStore((s) => s.setDefaultBodyMapView);
  const setAge = useAppStore((s) => s.setAge);
  const setGender = useAppStore((s) => s.setGender);
  const resetPreferences = useAppStore((s) => s.resetPreferences);

  return (
    <PageContainer>
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
          Settings
        </h1>
        <p className="text-sm text-surface-400 mt-0.5">Manage your preferences</p>
      </div>

      <div className="space-y-6 max-w-md">
        {/* ── Profile ──────────────────────────────────────────────── */}
        <Section title="Profile">
          <Row label="Age">
            <input
              type="number"
              min={8}
              max={110}
              value={age ?? ''}
              onChange={(e) => {
                const v = e.target.value;
                if (v === '') { setAge(null); return; }
                const n = Number(v);
                if (n >= 8 && n <= 110) setAge(n);
              }}
              placeholder="—"
              className={cn(
                'w-20 px-3 py-1.5 rounded-lg text-sm text-right',
                'border border-surface-200 dark:border-surface-700',
                'bg-white dark:bg-surface-800 text-surface-800 dark:text-surface-200',
                'focus:outline-none focus:ring-2 focus:ring-primary-500'
              )}
            />
          </Row>
          <Row label="Gender">
            <SegmentedPicker
              options={['male', 'female']}
              value={gender ?? ''}
              onChange={(v) => setGender(v as 'male' | 'female')}
            />
          </Row>
        </Section>

        {/* ── Appearance ────────────────────────────────────────────── */}
        <Section title="Appearance">
          <Row label="Theme">
            <div className="flex items-center gap-1 p-1 rounded-xl bg-surface-100 dark:bg-surface-800">
              {(['light', 'dark'] as const).map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setTheme(t)}
                  className={cn(
                    'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all capitalize',
                    prefs.theme === t
                      ? 'bg-white dark:bg-surface-700 text-surface-800 dark:text-surface-200 shadow-sm'
                      : 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'
                  )}
                >
                  {t === 'light' ? <Sun className="w-3 h-3" /> : <Moon className="w-3 h-3" />}
                  {t}
                </button>
              ))}
            </div>
          </Row>
        </Section>

        {/* ── Units ─────────────────────────────────────────────── */}
        <Section title="Units">
          <Row label="Weight">
            <SegmentedPicker
              options={['kg', 'lbs']}
              value={prefs.weightUnit}
              onChange={(v) => setWeightUnit(v as 'kg' | 'lbs')}
            />
          </Row>
          <Row label="Distance">
            <SegmentedPicker
              options={['km', 'miles']}
              value={prefs.distanceUnit}
              onChange={(v) => setDistanceUnit(v as 'km' | 'miles')}
            />
          </Row>
        </Section>

        {/* ── Defaults ─────────────────────────────────────────── */}
        <Section title="Defaults">
          <Row label="Body map view">
            <SegmentedPicker
              options={['front', 'back']}
              value={prefs.defaultBodyMapView}
              onChange={(v) => setDefaultBodyMapView(v as 'front' | 'back')}
            />
          </Row>
        </Section>

        {/* ── Danger zone ──────────────────────────────────────── */}
        <Section title="Reset">
          <button
            type="button"
            onClick={() => {
              resetPreferences();
              toast.success('Preferences reset to defaults');
            }}
            className="flex items-center gap-2 px-4 py-2 rounded-xl border border-red-200 dark:border-red-900/40 text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset to defaults
          </button>
        </Section>
      </div>
    </PageContainer>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────────

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h2 className="text-xs font-semibold text-surface-400 dark:text-surface-500 uppercase tracking-wide">
        {title}
      </h2>
      <div className="space-y-3 bg-white dark:bg-surface-900 rounded-2xl border border-surface-100 dark:border-surface-800 p-4">
        {children}
      </div>
    </div>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span className="text-sm text-surface-700 dark:text-surface-300">{label}</span>
      {children}
    </div>
  );
}

function SegmentedPicker({
  options,
  value,
  onChange,
}: {
  options: string[];
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="flex items-center gap-1 p-1 rounded-xl bg-surface-100 dark:bg-surface-800">
      {options.map((opt) => (
        <button
          key={opt}
          type="button"
          onClick={() => onChange(opt)}
          className={cn(
            'px-3 py-1 rounded-lg text-xs font-medium transition-all capitalize',
            value === opt
              ? 'bg-white dark:bg-surface-700 text-surface-800 dark:text-surface-200 shadow-sm'
              : 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'
          )}
        >
          {opt}
        </button>
      ))}
    </div>
  );
}
