from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Comments in this file were partially generated with Gemma3:27b (local server) then reviewed by the developer.

# Localisation of the SQLite database file
# (SQLite is a special type of database where everything is stored in an unique file
SQLALCHEMY_DATABASE_URL = "sqlite:///app/localdb.sqlite3"

# Create the database engine. This is the core interface for SQLAlchemy to interact with the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True, # If set to True, SQLAlchemy logs all SQL statements executed. Useful for debugging.
    connect_args={"check_same_thread": False} # Required for using SQLAlchemy with multiple threads (e.g., in a web application).  SQLite has threading limitations.
)

# SessionLocal is a class that manages database sessions.  Each session represents a connection to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class. All SQLAlchemy models (database tables) will inherit from this base.
Base = declarative_base()

def create_db():
    """
    Creates the database tables based on the defined SQLAlchemy models.
    This function should be called once during application startup 
    (e.g., when the application first starts or when a database migration is needed).
    """
    # Base.metadata.create_all(bind=engine) creates all tables defined in the models, if they don't already exist.
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency injection function to provide a database session.
    This function is designed to be used as a dependency in API endpoints (e.g., using FastAPI or similar frameworks).
    It opens a database session, yields it to the calling function, and then automatically closes the session 
    when the calling function is finished. This ensures that database connections are properly managed 
    and resources are released.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Ensures the database session is always closed, even if exceptions occur.