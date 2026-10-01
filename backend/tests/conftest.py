import os
os.environ["DATABASE_URL"]="sqlite:///./test.db"
os.environ["JWT_SECRET"]="test-secret"
os.environ["STORAGE_BACKEND"]="local"
os.environ["LOCAL_STORAGE_DIR"]="test_storage"
