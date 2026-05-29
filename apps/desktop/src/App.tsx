import { Download, FileAudio, Music2, Play, UploadCloud, Wand2 } from "lucide-react";

const pipelineSteps = [
  "Import audio",
  "Analyze track",
  "Separate stems",
  "Transcribe parts",
  "Export scores"
];

const artifacts = [
  { name: "Vocals", type: "Stem", status: "Pending" },
  { name: "Drums", type: "Stem", status: "Pending" },
  { name: "Bass", type: "Stem", status: "Pending" },
  { name: "Lead melody", type: "MIDI", status: "Pending" },
  { name: "Lead score", type: "MusicXML", status: "Pending" }
];

export function App() {
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
          <button className="primary-action" type="button">
            <Wand2 aria-hidden="true" />
            Run analysis
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
              <h2>Expected outputs</h2>
            </div>
          </div>

          <div className="artifact-list">
            {artifacts.map((artifact) => (
              <article className="artifact-row" key={`${artifact.type}-${artifact.name}`}>
                <div>
                  <strong>{artifact.name}</strong>
                  <span>{artifact.type}</span>
                </div>
                <span className="status">{artifact.status}</span>
                <div className="artifact-actions">
                  <button aria-label={`Preview ${artifact.name}`} type="button">
                    <Play aria-hidden="true" />
                  </button>
                  <button aria-label={`Download ${artifact.name}`} type="button">
                    <Download aria-hidden="true" />
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

