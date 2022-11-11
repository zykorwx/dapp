from fastapi import HTTPException
from fastapi.responses import JSONResponse

from .exceptions import BaseException


# HANDLER ERRORS
def http_exception_handler(_, exc: HTTPException):
    """Cambia la salida del error al formato estandar"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "rc": exc.status_code * -1,
            "msg": exc.detail,
        },
    )


def validation_exception_handler(_, exc: HTTPException):
    """Cambia la salida del error al formato estandar cuando faltan datos"""
    return JSONResponse(
        status_code=200,
        content={
            "rc": -1004,
            "msg": "Incomplete data",
        },
    )


def exception_handler(_, exc: Exception):
    """Cambia la salida del error al formato estandar cuando faltan datos"""
    return JSONResponse(
        status_code=200,
        content={
            "rc": -654,
            "msg": str(exc),
        },
    )


def custom_exception_handler(_, exc: BaseException):
    """Manejo de errores personalizado"""
    return JSONResponse(
        status_code=200,
        content=exc.to_dict(),
    )
