from sqlalchemy import create_engine
from models import Base  


SQLALCHEMY_DATABASE_URL = 'sqlite:///./finance_tracker.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    """Initialize the database by creating tables."""
   
    Base.metadata.create_all(bind=engine)
    print("Database initialized and tables created.")


if __name__ == "__main__":
    init_db()
