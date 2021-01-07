from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL", "sqlite:///data.db")
SQLALCHEMY_POOL_RECYCLE = int(getenv("DATABASE_POOL_RECYCLE", -1))
SQLALCHEMY_ARGUMENTS = {}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite:"):
    SQLALCHEMY_ARGUMENTS["check_same_thread"] = False

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args=SQLALCHEMY_ARGUMENTS,
                       pool_recycle=SQLALCHEMY_POOL_RECYCLE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=metadata)
