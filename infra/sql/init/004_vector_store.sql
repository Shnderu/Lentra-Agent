CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS property_embeddings (
    property_id BIGINT PRIMARY KEY,
    embedding vector(1536),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_embedding
ON property_embeddings
USING ivfflat (embedding vector_cosine_ops);
