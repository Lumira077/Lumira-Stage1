-- Initial bootstrap only; applied only to a new empty data directory.
\set ON_ERROR_STOP on
CREATE ROLE lumira_service_runtime NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE lumira_engineering_runtime NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE lumira_partner_runtime NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE DATABASE lumira_service_dev;
CREATE DATABASE lumira_engineering_dev;
CREATE DATABASE lumira_partner_dev;
REVOKE ALL ON DATABASE lumira_service_dev FROM PUBLIC;
REVOKE ALL ON DATABASE lumira_engineering_dev FROM PUBLIC;
REVOKE ALL ON DATABASE lumira_partner_dev FROM PUBLIC;
GRANT CONNECT ON DATABASE lumira_service_dev TO lumira_service_runtime;
GRANT CONNECT ON DATABASE lumira_engineering_dev TO lumira_engineering_runtime;
GRANT CONNECT ON DATABASE lumira_partner_dev TO lumira_partner_runtime;
\connect lumira_service_dev
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA app;
CREATE TABLE app.schema_migrations (version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now());
INSERT INTO app.schema_migrations(version) VALUES ('001-bootstrap');
GRANT USAGE ON SCHEMA app TO lumira_service_runtime;
\connect lumira_engineering_dev
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA engineering;
CREATE TABLE engineering.schema_migrations (version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now());
INSERT INTO engineering.schema_migrations(version) VALUES ('001-bootstrap');
GRANT USAGE ON SCHEMA engineering TO lumira_engineering_runtime;
\connect lumira_partner_dev
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA partner;
CREATE TABLE partner.schema_migrations (version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now());
INSERT INTO partner.schema_migrations(version) VALUES ('001-bootstrap');
GRANT USAGE ON SCHEMA partner TO lumira_partner_runtime;
