from sqlalchemy import create_engine as _ce
from sqlalchemy.orm import declarative_base as _db
from sqlalchemy.orm import sessionmaker as _ssmaker

engine = _ce(
    'sqlite:///db.sqlite3',
    echo=True,
    connect_args={"check_same_thread": False}
)

Base = _db()

Session = _ssmaker(bind=engine)

session = Session()
