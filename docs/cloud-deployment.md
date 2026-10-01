# Cloud deployment

## Student-friendly

Frontend: static hosting such as Render Static Site.

Backend: Render Python Web Service or equivalent.

Database: managed PostgreSQL. Supabase is convenient because it also provides managed authentication.

Storage: private AWS S3 bucket.

Secrets: deployment environment/secret manager.

The free tiers of hosting providers change over time. Verify current quotas before deployment.

## AWS advanced

Frontend → S3 + CloudFront
API → API Gateway → Lambda or App Runner/EC2
Auth → Cognito
Database → RDS PostgreSQL (or DynamoDB if a NoSQL redesign is desired)
Files → S3
Logs/metrics → CloudWatch
Async jobs → SQS
Secrets → Secrets Manager

## Azure

Static Web Apps/App Service, API Management, Functions, Azure Database for PostgreSQL, Blob Storage, Entra ID, Azure Monitor, Service Bus.

## GCP

Firebase Hosting/Cloud Storage, API Gateway, Cloud Run/Functions, Cloud SQL, Cloud Storage, Firebase Auth/Identity Platform, Cloud Logging/Monitoring, Pub/Sub.

Local development uses Docker PostgreSQL and local storage/MinIO. Cloud deployment swaps these adapters for managed services.
