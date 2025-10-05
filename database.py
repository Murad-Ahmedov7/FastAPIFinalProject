
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,declarative_base,sessionmaker

DATABASE_URL = 'sqlite:///./fastapi_final_new.db'
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()