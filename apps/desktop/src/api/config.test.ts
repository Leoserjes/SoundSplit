import { afterEach, describe, expect, it, vi } from "vitest";

import {
  apiEnvironmentNames,
  DEFAULT_API_BASE_URL,
  DEFAULT_API_ENVIRONMENT,
  getApiBaseUrl,
  getApiConfig,
  getApiEnvironment
} from "./config";

describe("desktop API configuration", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it("defaults to the local development API", () => {
    expect(getApiBaseUrl()).toBe(DEFAULT_API_BASE_URL);
    expect(getApiEnvironment()).toBe(DEFAULT_API_ENVIRONMENT);
    expect(getApiConfig()).toEqual({
      baseUrl: DEFAULT_API_BASE_URL,
      environment: "development"
    });
  });

  it("uses a configured API URL without keeping trailing slashes", () => {
    vi.stubEnv("VITE_API_BASE_URL", " https://api.example.test/// ");

    expect(getApiBaseUrl()).toBe("https://api.example.test");
  });

  it("falls back to the local API when the configured URL is blank", () => {
    vi.stubEnv("VITE_API_BASE_URL", "   ");

    expect(getApiBaseUrl()).toBe(DEFAULT_API_BASE_URL);
  });

  it.each(apiEnvironmentNames)("accepts the %s API environment", (environment) => {
    vi.stubEnv("VITE_API_ENVIRONMENT", environment);

    expect(getApiEnvironment()).toBe(environment);
  });

  it("falls back to development for unknown API environments", () => {
    vi.stubEnv("VITE_API_ENVIRONMENT", "preview");

    expect(getApiEnvironment()).toBe("development");
  });
});
