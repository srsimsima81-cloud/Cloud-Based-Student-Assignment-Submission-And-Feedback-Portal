# Scalability

10 students: one API instance, PostgreSQL and object storage.

1,000 students: multiple stateless API instances, connection pooling, indexes, pagination, CDN and centralized logging.

100,000 students uploading near a deadline:
Users → CDN → frontend
Users → API Gateway/load balancer → autoscaled API
API → managed PostgreSQL
API → S3
API → queue → virus scanning/notifications/background workers
API → cache for frequently read metadata

Direct-to-S3 presigned uploads can reduce application-server bandwidth. Database transactions protect metadata. Idempotency keys prevent repeated browser retries from creating duplicate logical submissions. Queues smooth non-critical work.
