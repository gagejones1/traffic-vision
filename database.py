from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 

# Load the PostgreSQL connection URL from the environment.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine and sessions used by the detection pipeline.
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

print("Sucessfully connected to PostgreSQL")

from models import Base

# Create the database tables defined by the SQLAlchemy models if they do not already exist.
Base.metadata.create_all(bind=engine)