# Project explanation

## Simple

This portal replaces email/paper assignment collection with one web workspace. Teachers publish coursework and deadlines; students upload files remotely; teachers review private files and enter marks and feedback; students see the result from their dashboard.

## Technical

React is the client. FastAPI exposes REST APIs and enforces authentication, RBAC and resource ownership. PostgreSQL stores structured metadata and relationships. Object storage stores PDFs/DOCX/ZIP/images. The database stores the storage key rather than binary file contents.

## Workflow

Teacher → creates assignment → PostgreSQL → student dashboard → student upload → object storage → verified object → submission metadata in PostgreSQL → teacher review → marks + feedback → PostgreSQL → student feedback view.

## Industry relevance

The same separation is common in LMS, universities, corporate training, certification platforms, bootcamps and EdTech products.

Benefits include centralized records, remote access, scalable file storage, automated tracking, less paperwork, centralized feedback, and controlled access.
