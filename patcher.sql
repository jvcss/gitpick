--postgresql://postgres:postgres@192.168.100.3:5432/gitmanager

-- Create the PostgreSQL database (if it doesn't exist)
CREATE DATABASE gitmanager;

-- Connect to the database
\c gitmanager;

-- Create the "patcher" table
CREATE TABLE IF NOT EXISTS patcher (
    file_name_hash TEXT PRIMARY KEY,
    repo_url TEXT,
    pair_a_b TEXT,
    patch TEXT,
    apply_at TIMESTAMP,
    compare_at TIMESTAMP DEFAULT NOW()
);
