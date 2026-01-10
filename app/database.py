from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# form => "postgresql://<username>:<password>@<ip/hostname>/<database_name>"
SQL_ALCHEMY_URL =  "postgresql://postgres:kottak@localhost/tutoDB"


engine = create_engine(SQL_ALCHEMY_URL)

SessionLocal = sessionmaker(bind=engine,
                            autocommit=False,
                            autoflush=False,
                            )

Base = declarative_base()

# generateur pour acces a la DB:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
