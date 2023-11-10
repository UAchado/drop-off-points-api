import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{os.environ['DATABASE_USER']}:" + \
    f"{os.environ['DATABASE_PASSWORD']}@" + \
    f"{os.environ['DATABASE_HOST']}/" + \
    f"{os.environ['DATABASE_NAME']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

