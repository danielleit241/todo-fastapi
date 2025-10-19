from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Override the get_db dependency to use the test database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

