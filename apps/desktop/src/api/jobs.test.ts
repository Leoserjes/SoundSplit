import { afterEach, describe, expect, it, vi } from "vitest";

import { createJob, DEFAULT_API_BASE_URL } from "./jobs";
import type { AnalysisJob } from "./types";

const createdJob: AnalysisJob = {
  artifacts: [],
  created_at: "2026-05-30T10:00:00Z",
  error: null,
  id: "job-demo-123",
  source_name: "demo.wav",
  source_type: "upload",
  status: "queued",
  updated_at: "2026-05-30T10:00:00Z"
};

describe("createJob", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("posts a typed upload job to the default API URL in browser dev", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue(createdJob),
      ok: true
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(
      createJob({
        source_name: "demo.wav",
        source_type: "upload"
      })
    ).resolves.toEqual(createdJob);

    expect(fetchMock).toHaveBeenCalledWith(`${DEFAULT_API_BASE_URL}/v1/jobs`, {
      body: JSON.stringify({
        source_name: "demo.wav",
        source_type: "upload"
      }),
      headers: {
        "Content-Type": "application/json"
      },
      method: "POST"
    });
  });

  it("uses the configured API URL without keeping a trailing slash", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "http://localhost:9000/");
    const fetchMock = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue(createdJob),
      ok: true
    });
    vi.stubGlobal("fetch", fetchMock);

    await createJob({
      source_name: "demo.wav",
      source_type: "upload"
    });

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:9000/v1/jobs",
      expect.any(Object)
    );
  });

  it("surfaces a friendly error when the service cannot be reached", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));

    await expect(
      createJob({
        source_name: "demo.wav",
        source_type: "upload"
      })
    ).rejects.toThrow("Could not reach the analysis service. Please try again.");
  });

  it("surfaces a friendly error when the service rejects the request", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false
      })
    );

    await expect(
      createJob({
        source_name: "demo.wav",
        source_type: "upload"
      })
    ).rejects.toThrow("Could not start the analysis. Please try again.");
  });

  it("surfaces a friendly error when the service returns invalid JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: vi.fn().mockRejectedValue(new SyntaxError("Unexpected token")),
        ok: true
      })
    );

    await expect(
      createJob({
        source_name: "demo.wav",
        source_type: "upload"
      })
    ).rejects.toThrow("The analysis service returned an invalid response. Please try again.");
  });
});
