import { FileAudio, LoaderCircle, Music2, UploadCloud, Wand2 } from "lucide-react";
import { useRef, useState } from "react";

import { createJob } from "./api/jobs";
import type { AnalysisJob } from "./api/types";

const pipelineSteps = [
  "Import audio",
  "Analyze track",
  "Separate stems",
  "Transcribe parts",
  "Export scores"
];

const analysisSourceName = "demo.wav";

export function App() {
  const requestInFlight = useRef(false);
  const [job, setJob] = useState<AnalysisJob | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleRunAnalysis() {
    if (requestInFlight.current) {
      return;
    }

    requestInFlight.current = true;
    setIsLoading(true);
    setError(null);
    setJob(null);

    try {
      const createdJob = await createJob({
        source_name: analysisSourceName,
        source_type: "upload"
      });
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
          <div className="dropzone" aria-label="Audio import area">
            <FileAudio aria-hidden="true" />
            <h2>Drop an audio file</h2>
            <p>Start with WAV, MP3, or FLAC. Link ingestion can come after the core pipeline is solid.</p>
            <button type="button">
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
              Run an analysis to create a job and see its artifacts.
            </div>
          )}
        </section>
      </section>
    </main>
  );
}
