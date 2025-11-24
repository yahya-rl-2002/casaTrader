-- Initialize TimescaleDB for Fear & Greed Index
-- This script sets up the database with TimescaleDB extensions

-- Create TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create database if not exists (handled by Docker)
-- CREATE DATABASE fear_greed_db;

-- Connect to the database
\c fear_greed_db;

-- Create TimescaleDB extension in the target database
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create tables (these will be created by SQLAlchemy, but we can prepare the structure)
-- The actual table creation will be handled by the Python application

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE fear_greed_db TO fear_greed_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO fear_greed_user;

-- Create indexes for better performance (will be created after tables are created)
-- These will be added by the application after table creation

-- Set up TimescaleDB specific configurations
-- These will be applied after the tables are converted to hypertables

COMMENT ON DATABASE fear_greed_db IS 'Fear & Greed Index Database with TimescaleDB for time-series data';







