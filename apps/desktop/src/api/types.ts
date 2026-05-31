export type JobStatus =
  | "created"
  | "uploading"
  | "queued"
  | "processing"
  | "completed"
  | "failed";

export type SourceType = "upload" | "youtube" | "spotify";

export type ArtifactKind = "stem" | "midi" | "musicxml" | "pdf" | "log";

export type ArtifactStatus = "pending" | "ready" | "failed";

export interface JobArtifact {
  id: string;
  kind: ArtifactKind;
  name: string;
  status: ArtifactStatus;
  uri?: string | null;
}

export interface AnalysisJob {
  id: string;
  status: JobStatus;
  source_type: SourceType;
  source_name: string | null;
  created_at: string;
  updated_at: string;
  error: string | null;
  artifacts: JobArtifact[];
}

export interface CreateJobRequest {
  source_type: SourceType;
  source_name: string | null;
}
