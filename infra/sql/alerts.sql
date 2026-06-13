CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    min_price DOUBLE PRECISION,
    max_price DOUBLE PRECISION,
    city TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alerts_user
ON alerts (user_id);

CREATE INDEX IF NOT EXISTS idx_alerts_active
ON alerts (active);
