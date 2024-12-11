from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


engine = create_engine(f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/todosapp')

session = sessionmaker(bind=engine, autoflush=False, autocommit=False)




def get_db_connection():
    db = session()
    try:
        yield db
    finally:
        db.close()


