-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);

-- Insert initial data
INSERT INTO patients (name) VALUES
    ('Peter'),
    ('Klaus'),
    ('Maria'),
    ('Sven'),
    ('Claudia');
