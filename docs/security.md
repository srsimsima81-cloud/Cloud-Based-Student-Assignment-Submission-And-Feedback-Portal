# Security

Implemented:
- bcrypt password hashing
- expiring JWT
- backend RBAC
- ownership checks
- private storage
- signed S3 download URLs
- server-side file type/size checks
- server-side deadline checks
- CORS configuration
- environment variables
- no cloud secrets in frontend

Production:
- HTTPS/TLS
- Supabase Auth or Cognito
- managed secret storage
- S3 Block Public Access
- least-privilege IAM
- encryption in transit/at rest
- malware scanning before institutional files are accepted
- rate limiting/API gateway
- audit logs
- encrypted DB connections
- backups and restore testing

Avoid making S3 public, putting AWS secrets in `VITE_*`, trusting browser time/role, storing plaintext passwords, accepting arbitrary extensions, or relying on hidden React buttons for authorization.
