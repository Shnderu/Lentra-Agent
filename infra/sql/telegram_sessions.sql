CREATE TABLE IF NOT EXISTS telegram_sessions (
    chat_id BIGINT PRIMARY KEY,
    state JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);
