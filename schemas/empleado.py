import datetime as _dt
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, root_validator


class EmpleadoSchema(BaseModel):
    id: Optional[str]
    uuid: Optional[str]
    nombre: str
    apellidos: str
    nombre_completo: Optional[str]
    pin: str
    fecha_creacion: Optional[_dt.datetime]
    activo: Optional[bool]

    @root_validator
    def compute_nombre_completo(cls, values):
        if values["nombre_completo"]:
            return values
        values["nombre_completo"] = f"{values['nombre']} {values['apellidos']}"
        return values

    @root_validator
    def compute_uuid(cls, values):
        values["id"] = str(UUID(values["uuid"]))
        return values

    class Config:
        orm_mode = True


class NewEmpleado(BaseModel):
    nombre: str
    apellidos: str
    pin: str


class _BaseResponse(BaseModel):
    rc: Optional[int] = 0
    msg: Optional[str] = "Ok"

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }


class EmpleadoResponse(_BaseResponse):
    data: Optional[EmpleadoSchema]


class EmpleadosResponse(_BaseResponse):
    data: Optional[List[EmpleadoSchema]]
