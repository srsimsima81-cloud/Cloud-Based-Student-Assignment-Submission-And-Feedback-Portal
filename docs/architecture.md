# Architecture

## Recommended student architecture

Student/Teacher browser
→ React/Vite frontend
→ FastAPI REST API
→ authentication/RBAC
→ PostgreSQL metadata
→ private S3-compatible object storage

### Why this split?

PostgreSQL is used for transactional records:
users, courses, assignments, deadlines, submission metadata, marks and feedback.

Object storage is used for binary content:
PDF, DOCX, PPTX, ZIP and image submissions.

The API remains the authorization boundary. A student never receives AWS credentials and cannot bypass the API to retrieve another student's private object.

## Advanced cloud architecture

Users
→ CDN
→ static frontend
→ API Gateway/load balancer
→ autoscaled FastAPI/Lambda
→ managed PostgreSQL
→ private S3
→ queue/background workers
→ monitoring/logging

This supports elasticity around assignment-deadline spikes.
