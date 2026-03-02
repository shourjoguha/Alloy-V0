/**
 * Error Boundary
 * Catches errors in child component trees and renders a fallback UI.
 * Wrap major route components and complex widgets with this.
 */

import { Component } from 'react';
import type { ReactNode, ErrorInfo } from 'react';
import { ErrorFallback } from './ErrorFallback';

interface Props {
  children: ReactNode;
  /** Custom fallback — defaults to <ErrorFallback> */
  fallback?: ReactNode;
  /** Scope label for logging (e.g. "DashboardWidget" or "WorkoutBuilder") */
  scope?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    const scope = this.props.scope ?? 'Unknown';
    console.error(`[ErrorBoundary:${scope}]`, error, info.componentStack);

    // Best-effort error reporting to backend
    try {
      const payload = {
        scope,
        message: error.message,
        stack: error.stack?.slice(0, 2000),
        componentStack: info.componentStack?.slice(0, 2000),
        url: window.location.href,
        timestamp: new Date().toISOString(),
      };
      navigator.sendBeacon(
        '/api/errors',
        new Blob([JSON.stringify(payload)], { type: 'application/json' }),
      );
    } catch {
      // Silently ignore — don't mask the original error
    }
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <ErrorFallback
          error={this.state.error}
          onReset={this.handleReset}
          scope={this.props.scope}
        />
      );
    }
    return this.props.children;
  }
}
