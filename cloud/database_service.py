"""Cloud database adapter notes.

Production configuration points DATABASE_URL at managed PostgreSQL
(Supabase, AWS RDS, Azure Database for PostgreSQL, or Cloud SQL).
The application itself uses SQLAlchemy so the API code is not tied to SQLite.
"""
from os import getenv

def database_target():
    return getenv("DATABASE_URL", "not configured")
