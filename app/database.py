#this will handle database connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#connection (where is our postgresql located)
#SQLALCHEMY_DATABASE_URL = 'postgresql:<user>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#engine is responsible for establishing the database connection to the database server
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True: 

#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
#                                 password = 'Infamous2356', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection established")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2) 