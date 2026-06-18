import { FileAudio, LoaderCircle, Music2, UploadCloud, Wand2 } from "lucide-react";
import type { ChangeEvent, DragEvent } from "react";
import { useRef, useState } from "react";

import { uploadAudioJob } from "./api/jobs";
import type { AnalysisJob } from "./api/types";

const pipelineSteps = [
  "Import audio",
  "Analyze track",
  "Separate stems",
  "Transcribe parts",
  "Export scores"
];

const supportedAudioExtensions = [".wav", ".mp3", ".flac"];
const maxUploadBytes = 100 * 1024 * 1024;

function getFileExtension(fileName: string) {
  const extensionStart = fileName.lastIndexOf(".");
  return extensionStart >= 0 ? fileName.slice(extensionStart).toLowerCase() : "";
}

function getAudioFileValidationError(file: File) {
  if (!supportedAudioExtensions.includes(getFileExtension(file.name))) {
    return "Choose a WAV, MP3, or FLAC file.";
  }

  if (file.size === 0) {
    return "Choose a non-empty audio file.";
  }

  if (file.size > maxUploadBytes) {
    return "Choose an audio file up to 100 MB.";
  }

  return null;
}

export function App() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const requestInFlight = useRef(false);
  const [job, setJob] = useState<AnalysisJob | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDraggingFile, setIsDraggingFile] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleSelectedFile(file: File) {
    const validationError = getAudioFileValidationError(file);
    setJob(null);

    if (validationError) {
      setSelectedFile(null);
      setError(validationError);
      return;
    }

    setSelectedFile(file);
    setError(null);
  }

  function handleFileInputChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.currentTarget.files?.[0];
    if (file) {
      handleSelectedFile(file);
    }
    event.currentTarget.value = "";
  }

  function handleDragOver(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
    setIsDraggingFile(true);
  }

  function handleDragLeave() {
    setIsDraggingFile(false);
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDraggingFile(false);

    const file = event.dataTransfer.files[0];
    if (file) {
      handleSelectedFile(file);
    }
  }

  async function handleRunAnalysis() {
    if (requestInFlight.current) {
      return;
    }

    if (!selectedFile) {
      setError("Choose an audio file before running analysis.");
      return;
    }

    requestInFlight.current = true;
    setIsLoading(true);
    setError(null);
    setJob(null);

    try {
      const createdJob = await uploadAudioJob(selectedFile);
      setJob(createdJob);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not start the analysis. Please try again."
      );
    } finally {
      requestInFlight.current = false;
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Music2 aria-hidden="true" />
          <div>
            <span>SoundSplit</span>
            <strong>harmonIA</strong>
          </div>
        </div>

        <nav className="project-nav" aria-label="Projects">
          <button className="active" type="button">Current project</button>
          <button type="button">Recent analyses</button>
          <button type="button">Exports</button>
          <button type="button">Settings</button>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Desktop workspace</p>
            <h1>New music analysis</h1>
          </div>
          <button
            aria-busy={isLoading}
            className="primary-action"
            disabled={isLoading}
            onClick={handleRunAnalysis}
            type="button"
          >
            {isLoading ? (
              <LoaderCircle aria-hidden="true" className="spin" />
            ) : (
              <Wand2 aria-hidden="true" />
            )}
            {isLoading ? "Starting analysis..." : "Run analysis"}
          </button>
        </header>

        <section className="analysis-grid">
          <div
            aria-label="Audio import area"
            className={`dropzone${isDraggingFile ? " dragging" : ""}${
              selectedFile ? " has-file" : ""
            }`}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <FileAudio aria-hidden="true" />
            <h2>{selectedFile ? "Ready to analyze" : "Drop an audio file"}</h2>
            <p>Use a WAV, MP3, or FLAC file up to 100 MB.</p>
            {selectedFile && (
              <div className="selected-file" aria-live="polite">
                <span>Selected file</span>
                <strong>{selectedFile.name}</strong>
              </div>
            )}
            <input
              accept=".wav,.mp3,.flac,audio/wav,audio/mpeg,audio/flac"
              aria-label="Choose audio file"
              className="file-input"
              onChange={handleFileInputChange}
              ref={fileInputRef}
              type="file"
            />
            <button onClick={() => fileInputRef.current?.click()} type="button">
              <UploadCloud aria-hidden="true" />
              Select file
            </button>
          </div>

          <div className="panel">
            <h2>Pipeline</h2>
            <ol className="timeline">
              {pipelineSteps.map((step, index) => (
                <li key={step}>
                  <span>{index + 1}</span>
                  {step}
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="results-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Artifacts</p>
              <h2>Analysis outputs</h2>
            </div>
          </div>

          {error && (
            <div className="feedback-message error-message" role="alert">
              {error}
            </div>
          )}

          {job ? (
            <>
              <dl className="job-summary" aria-label="Created analysis job">
                <div>
                  <dt>Job ID</dt>
                  <dd>{job.id}</dd>
                </div>
                <div>
                  <dt>Status</dt>
                  <dd>
                    <span className="status">{job.status}</span>
                  </dd>
                </div>
                <div>
                  <dt>Source</dt>
                  <dd>{job.source_name ?? "Unknown source"}</dd>
                </div>
              </dl>

              <div className="artifact-list">
                {job.artifacts.map((artifact) => (
                  <article className="artifact-row" key={artifact.id}>
                    <div>
                      <strong>{artifact.name}</strong>
                      <span>{artifact.kind}</span>
                    </div>
                    <span className="status">{artifact.status}</span>
                  </article>
                ))}
              </div>
            </>
          ) : (
            <div className="feedback-message empty-message">
              {selectedFile
                ? "Run analysis to create a job and see its artifacts."
                : "Choose an audio file to create a job and see its artifacts."}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}
