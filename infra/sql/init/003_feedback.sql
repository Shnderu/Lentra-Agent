CREATE TABLE IF NOT EXISTS user_feedback (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    property_id BIGINT NOT NULL,
    event_type TEXT NOT NULL, -- view | click | ignore | save
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_feedback_user
ON user_feedback (user_id);

CREATE INDEX IF NOT EXISTS idx_feedback_property
ON user_feedback (property_id);
