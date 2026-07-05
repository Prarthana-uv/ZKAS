-- Zero-Knowledge Authentication System Database Schema
-- PostgreSQL schema for ZKAS

-- Create UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    public_key JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Login attempts table (for security logging)
CREATE TABLE login_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    success BOOLEAN NOT NULL,
    ip_address INET,
    user_agent TEXT,
    attempted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for login attempts queries
CREATE INDEX idx_login_attempts_user_id ON login_attempts(user_id);
CREATE INDEX idx_login_attempts_attempted_at ON login_attempts(attempted_at);

-- Sessions table (for active session management)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Create index for session lookups
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- Proof verification logs table
CREATE TABLE proof_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    proof_hash VARCHAR(64),
    valid BOOLEAN NOT NULL,
    verification_time_ms INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for proof logs
CREATE INDEX idx_proof_logs_user_id ON proof_logs(user_id);
CREATE INDEX idx_proof_logs_created_at ON proof_logs(created_at);

-- Security events table (for audit trail)
CREATE TABLE security_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(50) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    description TEXT,
    details JSONB,
    severity VARCHAR(20) DEFAULT 'INFO',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for security events
CREATE INDEX idx_security_events_user_id ON security_events(user_id);
CREATE INDEX idx_security_events_created_at ON security_events(created_at);
CREATE INDEX idx_security_events_severity ON security_events(severity);

-- Audit table (track all changes)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    user_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for audit log
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for users table
CREATE TRIGGER users_updated_at_trigger
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Create function for audit logging
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, record_id, new_values)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, to_jsonb(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, to_jsonb(OLD), to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values)
        VALUES (TG_TABLE_NAME, TG_OP, OLD.id, to_jsonb(OLD));
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for audit logging
CREATE TRIGGER audit_users_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_changes();

CREATE TRIGGER audit_login_attempts_trigger
AFTER INSERT ON login_attempts
FOR EACH ROW
EXECUTE FUNCTION audit_changes();

-- Views for easier queries
CREATE VIEW failed_login_attempts AS
SELECT 
    u.username,
    u.email,
    COUNT(*) as attempt_count,
    MAX(la.attempted_at) as last_attempt
FROM login_attempts la
JOIN users u ON la.user_id = u.id
WHERE la.success = FALSE
    AND la.attempted_at > CURRENT_TIMESTAMP - INTERVAL '1 hour'
GROUP BY u.id, u.username, u.email
ORDER BY attempt_count DESC;

CREATE VIEW active_sessions AS
SELECT 
    s.id,
    u.username,
    u.email,
    s.ip_address,
    s.created_at,
    s.expires_at
FROM sessions s
JOIN users u ON s.user_id = u.id
WHERE s.expires_at > CURRENT_TIMESTAMP;

CREATE VIEW user_activity AS
SELECT 
    u.username,
    u.email,
    COUNT(DISTINCT la.id) as total_login_attempts,
    COUNT(DISTINCT CASE WHEN la.success THEN la.id END) as successful_logins,
    MAX(la.attempted_at) as last_activity
FROM users u
LEFT JOIN login_attempts la ON u.id = la.user_id
GROUP BY u.id, u.username, u.email;
