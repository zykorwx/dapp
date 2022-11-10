import datetime as _dt
import uuid as _uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import (CHAR, BigInteger, Boolean, DateTime,
                                     Integer, String)

from config.db import Base, engine


class Empleado(Base):
    __tablename__ = "main_empleado"
    
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    uuid = Column(CHAR(32), default=str(_uuid.uuid4().hex), nullable=False)
    nombre = Column(String(40), nullable=False)
    apellidos = Column(String(40), nullable=False)
    pin = Column(String(6), nullable=False)
    fecha_creacion = Column(DateTime, default=_dt.datetime.utcnow, nullable=False)
    activo = Column(Boolean(), default=True, nullable=False)
    comercio_id = Column(BigInteger, ForeignKey("main_comercio.id"), nullable=False)

    comercio = relationship("Comercio", back_populates="empleados")


    def __repr__(self):
        return f"User(id={self.id!r}, name={self.nombre!r}, apellidos={self.apellidos!r})"

    __table_args__ = (
        UniqueConstraint(
            "pin",
            "comercio_id",
            name="main_empleado_pin_comercio_id_uniq"
        ),
    )

Base.metadata.create_all(engine)