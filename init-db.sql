-- PostgreSQL initialization script for Agentic RAG
-- Creates necessary extensions and tables

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table (LlamaIndex will manage this, but we ensure the extension is ready)
-- The actual table structure is created by LlamaIndex's PGVectorStore

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE rag_db TO postgres;

-- Create a status table to track ingestion
CREATE TABLE IF NOT EXISTS ingestion_status (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    chunks_created INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
);

-- Create index on status for faster queries
CREATE INDEX IF NOT EXISTS idx_ingestion_status ON ingestion_status(status);

-- Function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for auto-updating timestamp
DROP TRIGGER IF EXISTS update_ingestion_status_updated_at ON ingestion_status;
CREATE TRIGGER update_ingestion_status_updated_at
    BEFORE UPDATE ON ingestion_status
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully';
END $$;
