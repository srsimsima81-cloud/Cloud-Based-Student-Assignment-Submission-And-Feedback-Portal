# Test matrix

| ID | Scenario | Expected |
|---|---|---|
| T01 | Student registration | 201/token |
| T02 | Teacher login | 200 |
| T03 | Invalid login | 401 |
| T04 | Student dashboard | 200 |
| T05 | Teacher dashboard | 200 |
| T06 | Create assignment | 201 |
| T07 | View assignment | 200 |
| T08 | Valid PDF | 201 |
| T09 | Invalid extension | 400 |
| T10 | Oversized file | 413 |
| T11 | On-time submission | SUBMITTED |
| T12 | Late submission | LATE or rejected by policy |
| T13 | Resubmission | replacement allowed unless graded |
| T14 | Own submission | 200 |
| T15 | Other student's submission | 403 |
| T16 | Teacher submissions | 200 |
| T17 | Grade | GRADED |
| T18 | Marks above maximum | 400 |
| T19 | Student feedback | visible |
| T20 | Student grades | 403 |
| T21 | File retrieval | authorized only |
| T22 | Storage failure | no false success |
| T23 | DB failure | no false success |
| T24 | Logout | token removed |
| T25 | Protected route after logout | login redirect |

Automated tests included: password hashing and deadline status. Add PostgreSQL integration tests before production use.
