ALTER TABLE processing_queue
ADD COLUMN IF NOT EXISTS result JSONB;
EOFcat << 'EOF' > /opt/lentra/infra/migrations/002_response_layer.sql
ALTER TABLE processing_queue
ADD COLUMN IF NOT EXISTS result JSONB;
