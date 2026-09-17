/**
 * API client for the Cybersecurity Trainer Task Manager backend.
 *
 * Provides a centralized fetch wrapper configured with the
 * backend base URL. Uses the Vite proxy in development.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/**
 * Health check response from the backend.
 */
export interface HealthResponse {
  status: string;
  application: string;
  version: string;
  timestamp: string;
  environment: string;
}

/**
 * Readiness check response from the backend.
 */
export interface ReadinessResponse {
  status: string;
  version: string;
  timestamp: string;
  checks: Record<string, boolean>;
}

/**
 * Generic API error.
 */
export class ApiError extends Error {
  statusCode: number;

  constructor(statusCode: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
  }
}

/**
 * Make a GET request to the API.
 */
async function apiGet<T>(path: string): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, `API request failed: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

/**
 * Fetch the health status from the backend.
 */
export async function fetchHealth(): Promise<HealthResponse> {
  return apiGet<HealthResponse>('/api/v1/health');
}

/**
 * Fetch the readiness status from the backend.
 */
export async function fetchReadiness(): Promise<ReadinessResponse> {
  return apiGet<ReadinessResponse>('/api/v1/health/readiness');
}

export default {
  fetchHealth,
  fetchReadiness,
};
