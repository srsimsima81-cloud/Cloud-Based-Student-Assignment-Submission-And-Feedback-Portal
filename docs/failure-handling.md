# Failure handling

Upload failure: do not create a successful DB record. If storage succeeded but DB failed, delete the new object as compensation.

Database unavailable: return a temporary error and do not claim success.

Storage unavailable: reject the submission instead of creating metadata pointing to a missing object.

Expired token: return 401; frontend clears token and redirects to login.

Duplicate request: use the assignment/student uniqueness rule; production should add an idempotency key.

Internet drop: show an error and allow retry. Large production uploads can use multipart/resumable upload.

Backend failure: stateless API instances can be replaced by another healthy instance.

Retry only transient operations, with bounded exponential backoff and jitter. Never blindly retry non-idempotent grading/submission writes without idempotency protection.
