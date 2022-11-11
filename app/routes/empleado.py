from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.config.exceptions import DuplicatedPinError, InvalidEmpleadoError
from app.models.empleado import Empleado
from app.schemas.empleado import (
    BaseResponse,
    EmpleadoResponse,
    EmpleadoSchema,
    EmpleadosResponse,
    NewEmpleado,
    UpdateEmpleado,
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
    """Regresa todos los empleados"""
    empleados: List[EmpleadoSchema] = []
    for empleado in db.query(Empleado).all():
        empleados.append(EmpleadoSchema.from_orm(empleado))
    response = EmpleadosResponse(data=empleados)
    return response


@empleado.get(
    "/empleados/{uuid}",
    response_model=EmpleadoResponse,
    response_model_exclude=_empleado_exclude,
)
def get_empleado(uuid: str, db: Session = Depends(get_db)):
    """Obtiene un empleado por su UUID"""
    try:
        empleado_from_db: Union[Empleado, None] = (
            db.query(Empleado).filter_by(uuid=uuid).first()
        )
    except StatementError:
        raise InvalidEmpleadoError()

    if not empleado_from_db:
        raise InvalidEmpleadoError()

    empleado: EmpleadoSchema = EmpleadoSchema.from_orm(empleado_from_db)
    return EmpleadoResponse(data=empleado)


@empleado.delete("/empleados/{uuid}", response_model=BaseResponse)
def delete_empleado(uuid: str, db: Session = Depends(get_db)):
    """Remueve un empleado por su UUID"""
    try:
        deletes = db.query(Empleado).filter_by(uuid=uuid).delete()
        db.commit()
    except StatementError:
        raise InvalidEmpleadoError()

    if not deletes:
        raise InvalidEmpleadoError()

    return BaseResponse()


@empleado.post(
    "/empleados",
    response_model=EmpleadoResponse,
    status_code=200,
    response_model_exclude=_empleado_exclude,
)
def create_empleado(empleado: NewEmpleado, db: Session = Depends(get_db)):
    """Crea un nuevo empleado"""
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


@empleado.put(
    "/empleados/{uuid}",
    response_model=EmpleadoResponse,
    response_model_exclude=_empleado_exclude,
)
def update_empleado(
    uuid: str, empleado: UpdateEmpleado, db: Session = Depends(get_db)
):
    """Edita los datos de un empleado por su UUID"""
    try:
        empleado_from_db: Union[Empleado, None] = (
            db.query(Empleado).filter_by(uuid=uuid).first()
        )
    except StatementError:
        raise InvalidEmpleadoError()

    if not empleado_from_db:
        raise InvalidEmpleadoError()

    empleado_from_db.nombre = empleado.nombre
    empleado_from_db.apellidos = empleado.apellidos
    empleado_from_db.pin = empleado.pin
    # La unica forma en que activo sea false es que venga 0 como string
    # Esto es por que asi estaba en el antiguo sistema y se debe respetar
    empleado_from_db.activo = empleado.activo != "0"
    db.add(empleado_from_db)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicatedPinError()

    empleado: EmpleadoSchema = EmpleadoSchema.from_orm(empleado_from_db)
    return EmpleadoResponse(data=empleado)
