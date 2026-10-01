"""Authentication architecture notes.

Local development uses the included FastAPI JWT implementation.
For production, the same API boundary can be placed behind Supabase Auth
or AWS Cognito and the backend token verifier can be replaced with the
provider's JWKS/JWT verification mechanism.
"""
from os import getenv

def auth_provider():
    return getenv("AUTH_PROVIDER", "local")
