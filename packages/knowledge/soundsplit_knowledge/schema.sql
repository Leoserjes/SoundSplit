CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS knowledge;

CREATE TABLE IF NOT EXISTS knowledge.sync_state (
    root_id uuid PRIMARY KEY,
    profile text NOT NULL,
    last_synced_at timestamptz NOT NULL,
    document_count integer NOT NULL,
    chunk_count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS knowledge.documents (
    root_id uuid NOT NULL,
    page_id uuid NOT NULL,
    title text NOT NULL,
    page_url text NOT NULL,
    edited_at timestamptz NOT NULL,
    last_synced_at timestamptz NOT NULL,
    document_type text NOT NULL,
    status text,
    confidence text,
    ids text[] NOT NULL,
    tags text[] NOT NULL,
    metadata jsonb NOT NULL,
    warnings jsonb NOT NULL,
    content_hash text NOT NULL,
    profile text NOT NULL,
    active boolean NOT NULL DEFAULT true,
    PRIMARY KEY (root_id, page_id)
);

CREATE TABLE IF NOT EXISTS knowledge.chunks (
    root_id uuid NOT NULL,
    page_id uuid NOT NULL,
    chunk_id text NOT NULL,
    content text NOT NULL,
    block_id text,
    headings text[] NOT NULL,
    knowledge_type text NOT NULL,
    embedding vector(1024) NOT NULL,
    search_text tsvector NOT NULL,
    PRIMARY KEY (root_id, page_id, chunk_id),
    FOREIGN KEY (root_id, page_id) REFERENCES knowledge.documents(root_id, page_id)
);

CREATE INDEX IF NOT EXISTS knowledge_chunks_text ON knowledge.chunks USING gin(search_text);
CREATE INDEX IF NOT EXISTS knowledge_documents_ids ON knowledge.documents USING gin(ids);
CREATE INDEX IF NOT EXISTS knowledge_documents_tags ON knowledge.documents USING gin(tags);
-- Exact vector search is intentional for this small KB. Add ANN only after measuring retrieval recall.
