from sqlalchemy import inspect
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

def create_if_not_exists_database():
    insp = inspect(engine)
    if not insp.has_table("posts"):
        models.Base.metadata.create_all(bind=engine)
        print("Database and tables created.")
        return
    print("Database already exists, skipping creation.")

def seed_posts(db: Session):
    if db.query(models.Post).first():
        print("Posts already seeded, skipping.")
        return  
    
    print("Seeding posts...")
    sample_posts = [
        models.Post(title="First Post", content="This is the content of the first post", published=True, vote=10),
        models.Post(title="Second Post", content="This is the content of the second post", published=False),
        models.Post(title="Third Post", content="This is the content of the third post", published=True, vote=5),
    ]
    db.add_all(sample_posts)
    print("Posts seeded.")
    db.commit()

def seed_data():
    create_if_not_exists_database()
    db = SessionLocal()
    try:
        seed_posts(db)
    finally:
        db.close()
        print("Database seeding complete.")

if __name__ == "__main__":
    seed_data()