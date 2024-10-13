from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update with your SQLite database path
DATABASE_URL = "sqlite:///./predictions.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
from .models import Base
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
