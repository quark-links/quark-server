from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hashids import Hashids

# TODO: Load hashids config from environment variables
hashids = Hashids(min_length=0, alphabet=("abcdefghijklmnopqrstuvwxyzABCDEFGHI"
                                          "JKLMNOPQRSTUVWXYZ0123456789"),
                  salt="keyboardcat")

# TODO: Load database URI from environment variables
SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=metadata)
