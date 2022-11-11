import datetime as _dt
from typing import Any, List, Optional, Union
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, root_validator


class EmpleadoSchema(BaseModel):
    id: Optional[str]
    uuid: Optional[UUID]
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
        values["id"] = str(values["uuid"])
        return values

    class Config:
        orm_mode = True


class NewEmpleado(BaseModel):
    nombre: str
    apellidos: str
    pin: str


class UpdateEmpleado(BaseModel):
    nombre: str
    apellidos: str
    pin: str
    activo: Any = "NO_EXISTS"

    @root_validator
    def compute_activo(cls, values):
        """Valida si existe el campo activo
        Se tiene que usar el tipo Any por que si se usa el tipo str
        cuando se envia int 0 se transforma a "0" y no se desea eso,
        la unica forma que sea false debe ser con "0" desde la peticion.

        Se usa el NO_EXISTS como default, para identificar cuando no se envia
        el campo activo, ya que como el campo es Any acepta cualquier cosa
        hasta los nulos
        """

        if values["activo"] == "NO_EXISTS":
            raise RequestValidationError()
        return values


class BaseResponse(BaseModel):
    rc: Optional[int] = 0
    msg: Optional[str] = "Ok"

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }


class EmpleadoResponse(BaseResponse):
    data: Optional[EmpleadoSchema]


class EmpleadosResponse(BaseResponse):
    data: Optional[List[EmpleadoSchema]]
