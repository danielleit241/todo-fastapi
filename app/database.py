from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.CONNECTION_STRING
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()

# while True:
#     try:
#         conn = engine.connect()
#         print("Database connection successful")
#         conn.close()
#         break
#     except Exception as e:
#         print("Database connection failed")
#         print(f"Error: {e}")