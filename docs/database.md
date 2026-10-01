# Database design

USERS: user_id PK, name, email, password_hash, role, created_at.

COURSES: course_id PK, course_name, teacher_id FK → USERS, created_at.

ASSIGNMENTS: assignment_id PK, course_id FK → COURSES, title, description, deadline, max_marks, allowed_file_types, max_file_size, created_by FK → USERS, created_at.

SUBMISSIONS: submission_id PK, assignment_id FK → ASSIGNMENTS, student_id FK → USERS, file_name, file_url, storage_path, submitted_at, submission_status, marks, feedback, graded_at.

Relationships:
Teacher → Course → Assignment → Submission ← Student.

Indexes are used on email, role, teacher ownership, assignment deadline, student ownership and assignment/student submission lookup.

Object storage is preferred for files. PostgreSQL stores metadata and relationships.
