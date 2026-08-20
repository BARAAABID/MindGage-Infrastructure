from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. The database URL (This tells SQLite to create a file named 'mindgage.db' in my folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./mindgage.db"

# 2. The Engine (The actual connection to the database)
# 'check_same_thread' : False is required for FastAPI because it handles concurrent requests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Enable WAL Mode (Write-Ahead Logging) for high concurrency and safety
# This prevents the database from locking up if the user and the AI try to write at the exact same time 
with engine.connect() as connection:
    connection.exec_driver_sql("PRAGMA journal_model=WAL;")

# 4. The SessionLocal (This creates a temporary "workspace" for data befpre saving it)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. The Base (I will use this to create the database tables later)
Base = declarative_base()