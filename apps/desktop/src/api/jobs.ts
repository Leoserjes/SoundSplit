import type { AnalysisJob, CreateJobRequest } from "./types";

export const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL).replace(/\/+$/, "");
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

  try {
    return (await response.json()) as AnalysisJob;
  } catch {
    throw new Error("The analysis service returned an invalid response. Please try again.");
  }
}
