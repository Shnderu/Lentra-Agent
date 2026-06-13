ALTER TABLE processing_queue
ADD COLUMN IF NOT EXISTS result JSONB;
EOFcat << 'EOF' > /opt/lentra/infra/migrations/add_result_column.sql
ALTER TABLE processing_queue
ADD COLUMN IF NOT EXISTS result JSONB;
