from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.db import get_db
from config.exceptions import DuplicatedPinError
from models.empleado import Empleado
from schemas.empleado import (
    EmpleadoResponse,
    EmpleadoSchema,
    EmpleadosResponse,
    NewEmpleado,
)

empleado = APIRouter(tags=["Empleados"])
_empleados_exclude = {"data": {"__all__": {"nombre", "apellidos", "uuid"}}}
_empleado_exclude = {"data": {"nombre", "apellidos", "uuid"}}


@empleado.get(
    "/empleados",
    response_model=EmpleadosResponse,
    response_model_exclude=_empleados_exclude,
)
def get_empleados(db: Session = Depends(get_db)):
    empleados: List[EmpleadoSchema] = []
    for empleado in db.query(Empleado).all():
        empleados.append(EmpleadoSchema.from_orm(empleado))
    response = EmpleadosResponse(data=empleados)
    return response


@empleado.get("/empleados/{uuid}", response_model=EmpleadoResponse)
def get_empleado(uuid: str, db: Session = Depends(get_db)):
    empleado = EmpleadoSchema.from_orm(
        db.get(Empleado).filter_by(uuid=uuid).first()
    )
    return EmpleadoResponse(data=empleado)


@empleado.post(
    "/empleados",
    response_model=EmpleadoResponse,
    status_code=200,
    response_model_exclude=_empleado_exclude,
)
def create_empleado(empleado: NewEmpleado, db: Session = Depends(get_db)):
    new_empleado: Empleado = Empleado(
        nombre=empleado.nombre,
        apellidos=empleado.apellidos,
        pin=empleado.pin,
        comercio_id=1,
    )
    db.add(new_empleado)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicatedPinError()
    empleado_schema = EmpleadoSchema.from_orm(new_empleado)
    response = EmpleadoResponse(data=empleado_schema)
    return response


"""
@user.get('/users')
def main() -> str:
    return 'Hello world 2'

@user.get('/users')
def main() -> str:
    return 'Hello world 2'

@user.get('/users')
def main() -> str:
    return 'Hello world 2'
"""
