import type { AnalysisJob, CreateJobRequest } from "./types";

export const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL).replace(/\/+$/, "");
}

async function parseJsonResponse(response: Response): Promise<AnalysisJob> {
  try {
    return (await response.json()) as AnalysisJob;
  } catch {
    throw new Error("The analysis service returned an invalid response. Please try again.");
  }
}

async function getApiErrorMessage(response: Response, fallbackMessage: string) {
  try {
    const payload = (await response.json()) as { detail?: unknown };
    return typeof payload.detail === "string" ? payload.detail : fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

export async function createJob(payload: CreateJobRequest): Promise<AnalysisJob> {
  let response: Response;

  try {
    response = await fetch(`${getApiBaseUrl()}/v1/jobs`, {
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json"
      },
      method: "POST"
    });
  } catch {
    throw new Error("Could not reach the analysis service. Please try again.");
  }

  if (!response.ok) {
    throw new Error("Could not start the analysis. Please try again.");
  }

  return parseJsonResponse(response);
}

export async function uploadAudioJob(file: File): Promise<AnalysisJob> {
  const formData = new FormData();
  formData.append("file", file);

  let response: Response;

  try {
    response = await fetch(`${getApiBaseUrl()}/v1/jobs/upload`, {
      body: formData,
      method: "POST"
    });
  } catch {
    throw new Error("Could not reach the analysis service. Please try again.");
  }

  if (!response.ok) {
    throw new Error(await getApiErrorMessage(response, "Could not start the analysis. Please try again."));
  }

  return parseJsonResponse(response);
}
