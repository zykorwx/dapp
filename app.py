from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.exception_handler import (custom_exception_handler,
                                      exception_handler,
                                      http_exception_handler,
                                      validation_exception_handler)
from config.exceptions import BaseException
from routes.empleado import empleado

app = FastAPI()

# Include exceptions handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(BaseException, custom_exception_handler)
app.add_exception_handler(Exception, exception_handler)


# Include routes
app.include_router(empleado)
