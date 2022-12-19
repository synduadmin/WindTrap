# THE FOLLOWING COMMANDS CREATE THE DB AND TABLE FOR THE LOGS

CREATE USER log WITH PASSWORD 'log';
CREATE DATABASE log;
GRANT ALL PRIVILEGES ON DATABASE log TO log;
GRANT ALL ON SCHEMA public TO log;
CREATE TABLE IF NOT EXISTS public.log
(
    event_timestamp timestamp with time zone,
    data jsonb,
    status integer
);
