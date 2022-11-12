from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.config.db import Base, get_db
from app.main import app
from app.models.comercio import Comercio

SQLALCHEMY_DATABASE_URL = "sqlite:///db_test.sqlite3"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
if not database_exists:
    create_database(engine.url)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


client = TestClient(app)


@pytest.fixture
def add_comercio():
    db = TestingSessionLocal()
    comercio = Comercio(
        id=1,
        uuid=UUID("993385d0519d459da8e47e48238a7e8f"),
        nombre="Comercio 1",
        activo=True,
        api_key=UUID("5a25c9f25c334f4197df4d2aafca5fd9"),
    )
    db.add(comercio)
    db.commit()
    db.close()
