"""SQLAlchemy objects."""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = settings.database
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_ARGUMENTS = {}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite:"):
    SQLALCHEMY_ARGUMENTS["check_same_thread"] = False

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args=SQLALCHEMY_ARGUMENTS,
                       pool_recycle=SQLALCHEMY_POOL_RECYCLE,
                       pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=metadata)
