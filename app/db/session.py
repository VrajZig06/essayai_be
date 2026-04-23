from sqlalchemy import create_engine
from app.config.settings import Setting
from sqlalchemy.orm import sessionmaker, create_session

DB_URL = Setting.DB_URL

engine = create_engine(DB_URL, echo=True)

# Create Local Session 
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Function: GET DB Session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error : {e}")
        raise e
    finally:
        db.close()