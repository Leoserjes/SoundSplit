import { afterEach, describe, expect, it, vi } from "vitest";

import { API_UNREACHABLE_MESSAGE, DEFAULT_API_BASE_URL } from "./config";
import { createJob, uploadAudioJob } from "./jobs";
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
    ).rejects.toThrow(API_UNREACHABLE_MESSAGE);
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

describe("uploadAudioJob", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("posts a selected audio file as multipart form data", async () => {
    const file = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    const fetchMock = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue({
        ...createdJob,
        source_name: "song.wav"
      }),
      ok: true
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(uploadAudioJob(file)).resolves.toEqual({
      ...createdJob,
      source_name: "song.wav"
    });

    expect(fetchMock).toHaveBeenCalledWith(`${DEFAULT_API_BASE_URL}/v1/jobs/upload`, {
      body: expect.any(FormData),
      method: "POST"
    });

    const request = fetchMock.mock.calls[0][1] as RequestInit;
    expect(request.body).toBeInstanceOf(FormData);
    expect((request.body as FormData).get("file")).toBe(file);
  });

  it("uses API validation messages when the upload is rejected", async () => {
    const file = new File(["notes"], "notes.txt", { type: "text/plain" });
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: vi.fn().mockResolvedValue({
          detail: "Unsupported audio format. Use a WAV, MP3, or FLAC file."
        }),
        ok: false
      })
    );

    await expect(uploadAudioJob(file)).rejects.toThrow(
      "Unsupported audio format. Use a WAV, MP3, or FLAC file."
    );
  });

  it("surfaces a friendly error when the upload service cannot be reached", async () => {
    const file = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));

    await expect(uploadAudioJob(file)).rejects.toThrow(
      API_UNREACHABLE_MESSAGE
    );
  });

  it("surfaces a friendly error when upload response JSON is invalid", async () => {
    const file = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: vi.fn().mockRejectedValue(new SyntaxError("Unexpected token")),
        ok: true
      })
    );

    await expect(uploadAudioJob(file)).rejects.toThrow(
      "The analysis service returned an invalid response. Please try again."
    );
  });
});
