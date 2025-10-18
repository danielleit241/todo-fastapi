from sqlalchemy import inspect
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

list_models = ["posts", "users", "votes"]

def drop_all_tables():
    models.Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")

def create_if_not_exists_database():
    insp = inspect(engine)
    drop_all_tables()
    for model in list_models:
        if not insp.has_table(model):
            models.Base.metadata.create_all(bind=engine)
            print("Database and tables created.")
            break
    else:
        print("Database already exists, skipping creation.")
        return

def seed_posts(db: Session):
    if db.query(models.Post).first():
        print("Posts already seeded, skipping.")
        return  
    
    print("Seeding posts...")
    sample_posts = [
        models.Post(title="First Post", content="This is the content of the first post", published=True, owner_id=1),
        models.Post(title="Second Post", content="This is the content of the second post", published=False, owner_id=2),
        models.Post(title="Third Post", content="This is the content of the third post", published=True, owner_id=3),
    ]
    db.add_all(sample_posts)
    print("Posts seeded.")
    db.commit()

def seed_users(db: Session):
    if db.query(models.User).first():
        print("Users already seeded, skipping.")
        return  
    
    print("Seeding users...")
    sample_users = [
        models.User(email="user1@example.com", hashed_password="hashedpassword1"),
        models.User(email="user2@example.com", hashed_password="hashedpassword2"),
        models.User(email="user3@example.com", hashed_password="hashedpassword3"),
    ]
    db.add_all(sample_users)
    print("Users seeded.")
    db.commit()

def seed_votes(db: Session):
    if db.query(models.Vote).first():
        print("Votes already seeded, skipping.")
        return  
    
    print("Seeding votes...")
    sample_votes = [
        models.Vote(user_id=1, post_id=1),
        models.Vote(user_id=2, post_id=1),
        models.Vote(user_id=3, post_id=2),
    ]
    db.add_all(sample_votes)
    print("Votes seeded.")
    db.commit()

def seed_data():
    create_if_not_exists_database()
    db = SessionLocal()
    try:
        seed_users(db)
        seed_posts(db)
        seed_votes(db)
    finally:
        db.close()
        print("Database seeding complete.")

if __name__ == "__main__":
    seed_data()