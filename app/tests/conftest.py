from collections.abc import Generator
from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from sqlalchemy.pool import StaticPool
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError

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

@pytest.fixture
def client_without_db() -> Generator[TestClient, None, None]:
    fake_db = MagicMock()
    fake_db.execute.side_effect = SQLAlchemyError("Database unavailable")

    def override_get_db():
        yield fake_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)