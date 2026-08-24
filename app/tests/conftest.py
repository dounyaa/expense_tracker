from collections.abc import Generator
from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from sqlalchemy.pool import StaticPool

DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool,)
TestingSessionLocal = sessionmaker(bind = test_engine, autoflush=False, expire_on_commit = False)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)