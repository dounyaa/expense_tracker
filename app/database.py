from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql://dounya:root@localhost:5432/expense_tracker"

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind = engine, autoflush=False, expire_on_commit = False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
