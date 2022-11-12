from typing import Union
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.models.comercio import Comercio

security = HTTPBasic(auto_error=False)


def get_auth(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Comercio:
    """Funcion de authentication, se usa el username para recibir el api_key
    El api key se debe enviar como un uuid.hex para que se haga la convercion
    """

    # En caso de no enviar la authenticacion se debe sobre escribir para
    # que regrese el mismo codigo de error y mensaje en en la anterior API
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )

    # Se convierte el string a un UUID valido
    user_id = credentials.username
    try:
        api_key = UUID(user_id)
    except ValueError:
        raise HTTPException(
            detail="API Key invalido", status_code=status.HTTP_401_UNAUTHORIZED
        )

    # Se intenta obtener el comercio usando el api_key
    comercio: Union[Comercio, None] = (
        db.query(Comercio).filter_by(api_key=api_key).first()
    )

    if not comercio:
        raise HTTPException(
            detail="API Key invalida", status_code=status.HTTP_401_UNAUTHORIZED
        )

    return comercio
