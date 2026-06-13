CREATE TABLE IF NOT EXISTS user_profiles (
    user_id BIGINT PRIMARY KEY,
    min_price DOUBLE PRECISION DEFAULT 0,
    max_price DOUBLE PRECISION DEFAULT 999999,
    prefers_sea_view BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_profiles_price
ON user_profiles (min_price, max_price);
