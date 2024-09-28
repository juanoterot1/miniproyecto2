CREATE TABLE tenants (
    tenant_id SERIAL PRIMARY KEY,
    tenant_name VARCHAR(255) NOT NULL,
    schema_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    mail VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    value FLOAT,
    id_group INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    id_evaluation INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE
);

CREATE TABLE answers_detail (
    id SERIAL PRIMARY KEY,
    company VARCHAR NOT NULL,
    delegation VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dni VARCHAR NOT NULL,
    id_evaluation INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    id_question INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    qualification VARCHAR
);

CREATE TABLE answers_scores (
    id SERIAL PRIMARY KEY,
    company VARCHAR NOT NULL,
    delegation VARCHAR NOT NULL,
    dni VARCHAR NOT NULL,
    id_evaluation INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    id_user INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_qualification VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
