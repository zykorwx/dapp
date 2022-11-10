from typing import Any

from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from config.db import session
from config.exceptions import DuplicatedPinError
from models.empleado import Empleado
from schemas.empleado import (EmpleadoResponse, EmpleadoSchema,
                              EmpleadosResponse, NewEmpleado)

empleado = APIRouter()


@empleado.get('/empleados', response_model=EmpleadosResponse)
def get_empleados():
    return session.query(Empleado).all()


@empleado.get('/empleados/{uuid}', response_model=EmpleadoResponse)
def get_empleado(uuid: str) -> Any:
    return session.get(Empleado).filter_by(uuid=uuid).first()


@empleado.post(
    '/empleados',
    response_model=EmpleadoResponse,
    status_code=200,
    response_model_exclude={'data': {'nombre', 'apellidos', 'uuid'}})
def create_empleado(empleado: NewEmpleado):
    new_empleado: Empleado = Empleado(
        nombre=empleado.nombre,
        apellidos=empleado.apellidos,
        pin=empleado.pin,
        comercio_id=1,
    )
    session.add(new_empleado)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicatedPinError()
    empleado_schema = EmpleadoSchema.from_orm(new_empleado)
    response = EmpleadoResponse()
    response.data = empleado_schema
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