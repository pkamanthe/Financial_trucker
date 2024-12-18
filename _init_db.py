from sqlalchemy import create_engine
from models import Base  # Ensure you import Base from your models module

# Replace 'sqlite:///./finance_tracker.db' with your actual database URL
SQLALCHEMY_DATABASE_URL = 'sqlite:///./finance_tracker.db'

# Create the SQLAlchemy engine with SQLite connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    """Initialize the database by creating tables."""
    # Use the Base metadata to create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized and tables created.")

# Run the initialization function when the script is executed directly
if __name__ == "__main__":
    init_db()
