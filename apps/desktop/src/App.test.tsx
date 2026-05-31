import "@testing-library/jest-dom/vitest";

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";
import { createJob } from "./api/jobs";
import type { AnalysisJob } from "./api/types";

vi.mock("./api/jobs", () => ({
  createJob: vi.fn()
}));

const createdJob: AnalysisJob = {
  artifacts: [
    {
      id: "artifact-vocals",
      kind: "stem",
      name: "Vocals",
      status: "pending",
      uri: null
    },
    {
      id: "artifact-score",
      kind: "musicxml",
      name: "Lead melody MusicXML",
      status: "pending",
      uri: null
    }
  ],
  created_at: "2026-05-30T10:00:00Z",
  error: null,
  id: "job-demo-123",
  source_name: "demo.wav",
  source_type: "upload",
  status: "queued",
  updated_at: "2026-05-30T10:00:00Z"
};

const mockedCreateJob = vi.mocked(createJob);

describe("App", () => {
  beforeEach(() => {
    mockedCreateJob.mockReset();
  });

  afterEach(() => {
    cleanup();
  });

  it("renders the initial harmonIA analysis workspace", () => {
    render(<App />);

    expect(screen.getByText("SoundSplit")).toBeInTheDocument();
    expect(screen.getByText("harmonIA")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "New music analysis" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Run analysis" })).toBeInTheDocument();
    expect(screen.getByLabelText("Audio import area")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Analysis outputs" })).toBeInTheDocument();
    expect(screen.getByText("Run an analysis to create a job and see its artifacts.")).toBeInTheDocument();
  });

  it("creates an upload job and displays the returned job details and artifacts", async () => {
    mockedCreateJob.mockResolvedValue(createdJob);
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(mockedCreateJob).toHaveBeenCalledWith({
      source_name: "demo.wav",
      source_type: "upload"
    });

    expect(await screen.findByText("job-demo-123")).toBeInTheDocument();
    expect(screen.getByText("demo.wav")).toBeInTheDocument();
    expect(screen.getByText("queued")).toBeInTheDocument();
    expect(screen.getByText("Vocals")).toBeInTheDocument();
    expect(screen.getByText("Lead melody MusicXML")).toBeInTheDocument();
  });

  it("shows a friendly error when job creation fails", async () => {
    mockedCreateJob.mockRejectedValue(
      new Error("Could not reach the analysis service. Please try again.")
    );
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Could not reach the analysis service. Please try again."
    );
  });

  it("clears a previous result when a new analysis fails", async () => {
    mockedCreateJob
      .mockResolvedValueOnce(createdJob)
      .mockRejectedValueOnce(new Error("Could not start the analysis. Please try again."));
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));
    expect(await screen.findByText("job-demo-123")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Could not start the analysis. Please try again."
    );
    expect(screen.queryByText("job-demo-123")).not.toBeInTheDocument();
  });

  it("blocks repeated clicks while job creation is loading", async () => {
    let resolveJob: ((job: AnalysisJob) => void) | undefined;
    mockedCreateJob.mockReturnValue(
      new Promise((resolve) => {
        resolveJob = resolve;
      })
    );
    render(<App />);

    const runButton = screen.getByRole("button", { name: "Run analysis" });
    fireEvent.click(runButton);
    fireEvent.click(runButton);

    expect(mockedCreateJob).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("button", { name: "Starting analysis..." })).toBeDisabled();

    resolveJob?.(createdJob);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Run analysis" })).toBeEnabled();
    });
  });
});
