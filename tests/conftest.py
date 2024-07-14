import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.shared.infra.database.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# Config db url for tests - same as in docker-compose.test-integration.yml
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db_test/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        yield db_session
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides[get_db] = get_db
