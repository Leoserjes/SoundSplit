export const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";
export const DEFAULT_API_ENVIRONMENT = "development";
export const API_UNREACHABLE_MESSAGE =
  "Could not reach the analysis service. Check that the API is running and try again.";

export const apiEnvironmentNames = ["development", "staging", "production"] as const;

export type ApiEnvironmentName = (typeof apiEnvironmentNames)[number];

export interface ApiConfig {
  baseUrl: string;
  environment: ApiEnvironmentName;
}

function isApiEnvironmentName(value: string): value is ApiEnvironmentName {
  return apiEnvironmentNames.includes(value as ApiEnvironmentName);
}

function normalizeApiBaseUrl(value: string) {
  const trimmedValue = value.trim().replace(/\/+$/, "");
  return trimmedValue.length > 0 ? trimmedValue : DEFAULT_API_BASE_URL;
}

export function getApiEnvironment(): ApiEnvironmentName {
  const configuredEnvironment = import.meta.env.VITE_API_ENVIRONMENT?.trim();

  if (configuredEnvironment && isApiEnvironmentName(configuredEnvironment)) {
    return configuredEnvironment;
  }

  return DEFAULT_API_ENVIRONMENT;
}

export function getApiBaseUrl() {
  return normalizeApiBaseUrl(import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL);
}

export function getApiConfig(): ApiConfig {
  return {
    baseUrl: getApiBaseUrl(),
    environment: getApiEnvironment()
  };
}
