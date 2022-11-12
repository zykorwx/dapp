import datetime as _dt
import uuid as _uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import (
    CHAR,
    BigInteger,
    Boolean,
    DateTime,
    Integer,
    String,
)
from sqlalchemy_utils import UUIDType

from app.config.db import Base, engine


class Empleado(Base):
    __tablename__ = "main_empleado"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    uuid = Column(UUIDType(binary=False), default=_uuid.uuid4)
    nombre = Column(String(40), nullable=False)
    apellidos = Column(String(40), nullable=False)
    pin = Column(String(6), nullable=False)
    fecha_creacion = Column(
        DateTime, default=_dt.datetime.utcnow, nullable=False
    )
    activo = Column(Boolean(), default=True, nullable=False)
    comercio_id = Column(
        BigInteger, ForeignKey("main_comercio.id"), nullable=False
    )

    comercio = relationship("Comercio", back_populates="empleados")

    def __repr__(self):
        return (
            f"Empleado(id={self.id!r}, "
            f"name={self.nombre!r}, "
            f"apellidos={self.apellidos!r})"
        )

    __table_args__ = (
        UniqueConstraint(
            "pin", "comercio_id", name="main_empleado_pin_comercio_id_uniq"
        ),
    )


Base.metadata.create_all(engine)
