from app.security import hash_password, verify_password
def test_password_hash_round_trip():
    raw="StrongPass123!"
    hashed=hash_password(raw)
    assert hashed != raw
    assert verify_password(raw,hashed)
    assert not verify_password("wrong",hashed)
