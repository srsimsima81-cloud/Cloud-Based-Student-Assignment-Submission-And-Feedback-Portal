# Cloud concepts

| Concept | Project location |
|---|---|
| Cloud computing | Independently deploy frontend, API, database and object storage |
| SaaS | Browser-based portal consumed as a service |
| PaaS | Managed PostgreSQL/auth/hosting in cloud deployment |
| IaaS | Advanced AWS design with VPC, EC2/load balancer |
| Cloud database | Managed PostgreSQL such as Supabase |
| Object storage | S3/private bucket or MinIO locally |
| Authentication | JWT implementation; managed provider can replace it |
| Authorization/RBAC | FastAPI dependencies and ownership checks |
| REST | `/api/auth`, `/api/courses`, `/api/assignments`, `/api/submissions` |
| Serverless | Advanced AWS Lambda option |
| Scalability | Stateless API + managed database + object storage |
| Elasticity | Autoscale API workers/serverless functions around deadline spikes |
| Availability | Managed services, health checks, replicas/backups in production |
| Load balancing | API Gateway/load balancer in advanced architecture |
| CDN | Static frontend assets |
| API Gateway | AWS advanced architecture |
| Environment variables | `.env.example`; secrets excluded from Git |
| Secrets management | Production provider secret store |
| Logging/monitoring | API/provider logs and health endpoint |
| Backup | Managed DB backup + S3 versioning/lifecycle |
| CI/CD | GitHub Actions workflow |
| Cloud deployment | Hosted frontend + FastAPI + managed PostgreSQL + S3 |

Database = structured metadata, relationships, grades and feedback. Object storage = large binary files. Files should not normally be stored as PostgreSQL binary fields because object storage is designed for durable, scalable object delivery.
