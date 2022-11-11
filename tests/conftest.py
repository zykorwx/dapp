import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.config.db import Base, get_db
from app.main import app
from app.models.empleado import Empleado

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
def items():
    db = TestingSessionLocal()
    new_empleado: Empleado = Empleado(
        nombre="Saul",
        apellidos="Pineda Torres",
        pin="000001",
        comercio_id=1,
    )
    new_empleado2: Empleado = Empleado(
        nombre="Enrique",
        apellidos="Pineda",
        pin="000002",
        comercio_id=1,
    )
    db.add(new_empleado)
    db.add(new_empleado2)
    db.commit()
    db.close()
