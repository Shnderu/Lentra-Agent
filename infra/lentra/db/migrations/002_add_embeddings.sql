ALTER TABLE properties
ADD COLUMN IF NOT EXISTS embedding JSONB;

CREATE INDEX IF NOT EXISTS idx_properties_embedding_gin
ON properties USING GIN (embedding);
