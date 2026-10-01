# API reference

AUTH
- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/auth/logout`
- GET `/api/auth/me`

COURSES
- POST `/api/courses`
- GET `/api/courses`

ASSIGNMENTS
- POST `/api/assignments`
- GET `/api/assignments`
- GET `/api/assignments/{id}`
- PUT `/api/assignments/{id}`
- DELETE `/api/assignments/{id}`

SUBMISSIONS
- POST `/api/submissions/assignments/{id}/submit` multipart file
- GET `/api/submissions/me`
- GET `/api/submissions/assignment/{id}`
- GET `/api/submissions/{id}`
- GET `/api/submissions/{id}/download`

FEEDBACK
- POST `/api/submissions/{id}/grade`
- Feedback is returned in the submission resource.

Typical status codes: 200 success, 201 created, 400 validation/business rule, 401 unauthenticated, 403 unauthorized, 404 not found, 409 conflict, 413 too large, 503 temporary storage/transaction failure.
