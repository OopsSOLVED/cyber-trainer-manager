import { useState, useEffect } from 'react';
import { fetchHealth, type HealthResponse } from './services/api';
import './App.css';

/**
 * Main application shell.
 *
 * Session 1: Displays application status page with live health check
 * from the backend API. Demonstrates the design system and confirms
 * frontend-to-backend connectivity.
 *
 * Future sessions will replace this with a full layout containing
 * navigation, sidebar, dashboard, and feature pages.
 */
function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function checkHealth() {
      try {
        const data = await fetchHealth();
        if (mounted) {
          setHealth(data);
          setError(null);
        }
      } catch (err) {
        if (mounted) {
          setError(
            err instanceof Error
              ? err.message
              : 'Unable to reach backend API'
          );
          setHealth(null);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    checkHealth();

    // Poll health every 30 seconds
    const interval = setInterval(checkHealth, 30000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const statusClass = loading
    ? 'loading'
    : health
      ? 'healthy'
      : 'unhealthy';

  const statusLabel = loading
    ? 'Connecting...'
    : health
      ? 'All Systems Operational'
      : 'Backend Unreachable';

  return (
    <div className="app">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero__icon" aria-hidden="true">
          🛡️
        </div>

        <h1 className="hero__title">
          <span className="gradient-text">Cyber Trainer</span>
          <br />
          Task Manager
        </h1>

        <p className="hero__subtitle">
          A production learning platform that turns the cybersecurity-trainer
          skill stack into a daily execution plan, tracks progress, and mirrors
          the live dashboard into Google Sheets.
        </p>
      </section>

      {/* Status Card */}
      <div className="status-card glass-card">
        <div className="status-card__header">
          <span className="status-card__title">System Status</span>
          <div className="status-card__indicator">
            <span className={`status-dot status-dot--${statusClass}`} />
            <span className={`status-card__label status-card__label--${statusClass}`}>
              {statusLabel}
            </span>
          </div>
        </div>

        <div className="status-details">
          <div className="status-row">
            <span className="status-row__key">Application</span>
            <span className="status-row__value">
              {health?.application ?? '—'}
            </span>
          </div>
          <div className="status-row">
            <span className="status-row__key">Version</span>
            <span className="status-row__value status-row__value--accent">
              {health?.version ?? '—'}
            </span>
          </div>
          <div className="status-row">
            <span className="status-row__key">Environment</span>
            <span className="status-row__value">
              {health?.environment ?? '—'}
            </span>
          </div>
          <div className="status-row">
            <span className="status-row__key">Last Check</span>
            <span className="status-row__value">
              {health?.timestamp
                ? new Date(health.timestamp).toLocaleTimeString()
                : '—'}
            </span>
          </div>
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}
      </div>

      {/* Session Info */}
      <div className="session-info">
        <span className="badge badge--cyan">Session 1</span>
        <span className="badge badge--purple" style={{ marginLeft: '8px' }}>
          Foundation
        </span>
        <p className="session-info__text">
          Project skeleton deployed — backend, frontend, and infrastructure ready.
        </p>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p className="app-footer__text">
          Cybersecurity Trainer Task Manager &middot; Built with FastAPI + React + TypeScript
        </p>
      </footer>
    </div>
  );
}

export default App;
