import datetime as _dt
import uuid as _uuid

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import (CHAR, BigInteger, Boolean, DateTime,
                                     Integer, String)

from config.db import Base, engine


class Comercio(Base):
    __tablename__ = "main_comercio"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    uuid = Column(CHAR(32), default=str(_uuid.uuid4().hex), nullable=False)
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean(), default=True, nullable=False)
    email_contacto = Column(String(50))
    telefono_contacto = Column(String(15))
    api_key = Column(CHAR(32), default=str(_uuid.uuid4().hex), nullable=False)
    fecha_creacion = Column(DateTime, default=_dt.datetime.utcnow, nullable=False)

    empleados = relationship("Empleado", back_populates="comercio")

    def __repr__(self):
        return (
            f"Comercio(id={self.id!r}, "
            f"nombre={self.nombre!r}, "
            f"email_contacto={self.email_contacto!r}), "
            f"api_key={self.api_key!r})"
        )


Base.metadata.create_all(engine)