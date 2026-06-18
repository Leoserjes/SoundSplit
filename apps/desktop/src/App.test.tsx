import "@testing-library/jest-dom/vitest";

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";
import { uploadAudioJob } from "./api/jobs";
import type { AnalysisJob } from "./api/types";

vi.mock("./api/jobs", () => ({
  uploadAudioJob: vi.fn()
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
  source_name: "song.wav",
  source_type: "upload",
  status: "queued",
  updated_at: "2026-05-30T10:00:00Z"
};

const mockedUploadAudioJob = vi.mocked(uploadAudioJob);

describe("App", () => {
  beforeEach(() => {
    mockedUploadAudioJob.mockReset();
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
    expect(screen.getByText("Choose an audio file to create a job and see its artifacts.")).toBeInTheDocument();
  });

  it("asks for an audio file before starting analysis", async () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Choose an audio file before running analysis."
    );
    expect(mockedUploadAudioJob).not.toHaveBeenCalled();
  });

  it("selects an audio file and uploads it to create an analysis job", async () => {
    const audioFile = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    mockedUploadAudioJob.mockResolvedValue(createdJob);
    render(<App />);

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [audioFile] }
    });
    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(mockedUploadAudioJob).toHaveBeenCalledWith(audioFile);

    expect(await screen.findByText("job-demo-123")).toBeInTheDocument();
    expect(screen.getAllByText("song.wav")).toHaveLength(2);
    expect(screen.getByText("queued")).toBeInTheDocument();
    expect(screen.getByText("Vocals")).toBeInTheDocument();
    expect(screen.getByText("Lead melody MusicXML")).toBeInTheDocument();
  });

  it("accepts a dropped audio file", () => {
    const audioFile = new File(["audio-bytes"], "dropped.flac", { type: "audio/flac" });
    render(<App />);

    fireEvent.drop(screen.getByLabelText("Audio import area"), {
      dataTransfer: { files: [audioFile] }
    });

    expect(screen.getByText("dropped.flac")).toBeInTheDocument();
    expect(screen.getByText("Run analysis to create a job and see its artifacts.")).toBeInTheDocument();
  });

  it("shows a validation error for unsupported files", async () => {
    const textFile = new File(["notes"], "notes.txt", { type: "text/plain" });
    render(<App />);

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [textFile] }
    });

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Choose a WAV, MP3, or FLAC file."
    );
    expect(screen.queryByText("notes.txt")).not.toBeInTheDocument();
  });

  it("shows a validation error for empty audio files", async () => {
    const emptyFile = new File([], "empty.wav", { type: "audio/wav" });
    render(<App />);

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [emptyFile] }
    });

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Choose a non-empty audio file."
    );
    expect(screen.queryByText("empty.wav")).not.toBeInTheDocument();
  });

  it("shows a friendly error when upload fails", async () => {
    const audioFile = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    mockedUploadAudioJob.mockRejectedValue(
      new Error("Could not reach the analysis service. Please try again.")
    );
    render(<App />);

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [audioFile] }
    });
    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Could not reach the analysis service. Please try again."
    );
  });

  it("clears a previous result when a new analysis fails", async () => {
    const firstFile = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    const secondFile = new File(["other-audio-bytes"], "second.mp3", { type: "audio/mpeg" });
    mockedUploadAudioJob
      .mockResolvedValueOnce(createdJob)
      .mockRejectedValueOnce(new Error("Could not start the analysis. Please try again."));
    render(<App />);

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [firstFile] }
    });
    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));
    expect(await screen.findByText("job-demo-123")).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [secondFile] }
    });
    fireEvent.click(screen.getByRole("button", { name: "Run analysis" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Could not start the analysis. Please try again."
    );
    expect(screen.queryByText("job-demo-123")).not.toBeInTheDocument();
  });

  it("blocks repeated clicks while job creation is loading", async () => {
    const audioFile = new File(["audio-bytes"], "song.wav", { type: "audio/wav" });
    let resolveJob: ((job: AnalysisJob) => void) | undefined;
    mockedUploadAudioJob.mockReturnValue(
      new Promise((resolve) => {
        resolveJob = resolve;
      })
    );
    render(<App />);

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [audioFile] }
    });
    const runButton = screen.getByRole("button", { name: "Run analysis" });
    fireEvent.click(runButton);
    fireEvent.click(runButton);

    expect(mockedUploadAudioJob).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("button", { name: "Starting analysis..." })).toBeDisabled();

    resolveJob?.(createdJob);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Run analysis" })).toBeEnabled();
    });
  });
});
