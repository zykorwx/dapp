import uuid as _uuid
from typing import List

import pytest
from requests import Response
from requests.auth import HTTPBasicAuth
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

EMPLEADOS_TO_CREATE = {
    "000001": {"nombre": "Saul", "apellidos": "Pineda", "pin": "000001"},
    "000002": {"nombre": "Enrique", "apellidos": "Torres", "pin": "000002"},
}

auth = HTTPBasicAuth(username="5a25c9f25c334f4197df4d2aafca5fd9", password="")


# Helpers functions
def _request_add_empleado(payload: dict) -> Response:
    aux = client.post("/empleados", json=payload, auth=auth)
    print(aux)
    return aux


def _validate_response_empleado(empleado: dict) -> None:
    data = EMPLEADOS_TO_CREATE[empleado["pin"]]
    nombre_completo = f'{data["nombre"]} {data["apellidos"]}'
    assert empleado["nombre_completo"] == nombre_completo
    assert empleado["pin"] == data["pin"]
    assert empleado["activo"]
    assert _uuid.UUID(empleado["id"])


def _get_all_empleados() -> List[dict]:
    empleados_response: Response = client.get("/empleados", auth=auth)
    return empleados_response.json()["data"]


# POST new empleado
def test_add_empleado(add_comercio):
    """Debe agregar un nuevo empleado con los datos correctos"""
    response: Response = _request_add_empleado(EMPLEADOS_TO_CREATE["000001"])
    data = response.json()
    assert response.status_code == 200
    assert data["rc"] == 0
    assert data["msg"] == "Ok"
    _validate_response_empleado(data["data"])


def test_duplicated_pin():
    """Debe regresar Duplicated PIN cuando ya existe el pin/comercio"""
    response: Response = _request_add_empleado(EMPLEADOS_TO_CREATE["000001"])
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == -1003
    assert data["msg"] == "Duplicated PIN"


def test_incomplete_data():
    """Debe regresar Incomplete data cuando faltan datos basicos"""
    response: Response = _request_add_empleado(
        {"nombre": "Saul", "apellidos": "Pineda"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == -1004
    assert data["msg"] == "Incomplete data"


# GET all empleados
def test_get_all_empleados():
    _request_add_empleado(EMPLEADOS_TO_CREATE["000002"])
    response: Response = client.get("/empleados", auth=auth)
    data = response.json()
    assert response.status_code == 200
    assert data["rc"] == 0
    assert data["msg"] == "Ok"
    for empleado in data["data"]:
        _validate_response_empleado(empleado)


def test_get_empleados():
    """Debe regresar Please enter a valid id cuando sea PUT/DELETE"""

    # PUT
    response: Response = client.put("/empleados", auth=auth)
    data = response.json()
    assert response.status_code == 200
    assert data["rc"] == -1001
    assert data["msg"] == "Please enter a valid id"

    # DELETE
    response: Response = client.delete("/empleados", auth=auth)
    data = response.json()
    assert response.status_code == 200
    assert data["rc"] == -1001
    assert data["msg"] == "Please enter a valid id"


# GET empleado
def test_get_empleado():
    """Debe regresar un empleado o regresar Invalid id"""
    empleados_data: List[dict] = _get_all_empleados()
    uuid: str = empleados_data[0]["id"]
    # Debe regresar el empleado
    response: Response = client.get(f"/empleados/{uuid}", auth=auth)
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == 0
    assert data["msg"] == "Ok"
    _validate_response_empleado(data["data"])


def test_get_empleado_no_exists_uuid():
    """Debe regresar Invalid id si el uuid es valido pero no existe"""
    response: Response = client.get(
        f"/empleados/{str(_uuid.uuid4())}", auth=auth
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == -1002
    assert data["msg"] == "Invalid id"


def test_get_empleado_invalid_uuid():
    """Debe regresar Invalid id si el uuid no es valido"""
    response: Response = client.get("/empleados/NO VALIDO", auth=auth)
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == -1002
    assert data["msg"] == "Invalid id"


# DELETE empleados
def test_delete_empleado():
    """Debe remover un empleado si existe o regresar Invalid id"""
    empleados_data: List[dict] = _get_all_empleados()
    uuid = empleados_data[0]["id"]
    # Debe regresar ok si se removio el emplado
    response: Response = client.delete(f"/empleados/{uuid}", auth=auth)
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == 0
    assert data["msg"] == "Ok"

    # Debe regresar Invalid id si no existe el uuid
    response: Response = client.delete(f"/empleados/{uuid}", auth=auth)
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == -1002
    assert data["msg"] == "Invalid id"


def test_delete_empleado_invalid_uuid():
    """Debe regresar Invalid id si el uuid no es valido"""
    response: Response = client.delete("/empleados/NO VALIDO", auth=auth)
    assert response.status_code == 200
    data = response.json()
    assert data["rc"] == -1002
    assert data["msg"] == "Invalid id"


# Update empleados
def test_update_empleado_ok():
    """Debe actualizar un empleado"""
    empleados_data: List[dict] = _get_all_empleados()
    uuid: str = empleados_data[0]["id"]
    # Debe regresar el empleado
    response: Response = client.put(
        f"/empleados/{uuid}",
        json={
            "nombre": "Leonardo",
            "apellidos": "Pineda",
            "pin": "123123",
            "activo": None,
        },
        auth=auth,
    )
    data = response.json()
    empleado = data["data"]

    assert response.status_code == 200
    assert data["rc"] == 0
    assert data["msg"] == "Ok"
    assert empleado["nombre_completo"] == "Leonardo Pineda"
    assert empleado["pin"] == "123123"
    assert empleado["activo"]
    assert _uuid.UUID(empleado["id"])


def test_update_empleado_invalid():
    """Debe regresar invalid data cuando faltan datos

    En este test no se evnia el campo 'activo'
    """
    empleados_data: List[dict] = _get_all_empleados()
    uuid: str = empleados_data[0]["id"]
    # Debe regresar el empleado
    response: Response = client.put(
        f"/empleados/{uuid}",
        json={
            "nombre": "Leonardo",
            "apellidos": "Pineda",
            "pin": "123123",
        },
        auth=auth,
    )
    data = response.json()

    assert response.status_code == 200
    assert data["rc"] == -1004
    assert data["msg"] == "Incomplete data"


def test_update_empleado_duplicated_pin():
    """Debe regresar Duplicated PIN cuando el pin ya existe"""
    _request_add_empleado(EMPLEADOS_TO_CREATE["000001"])
    empleados_data: List[dict] = _get_all_empleados()
    uuid: str = empleados_data[0]["id"]
    # Debe regresar el empleado
    response: Response = client.put(
        f"/empleados/{uuid}",
        json={
            "nombre": "Leonardo",
            "apellidos": "Pineda",
            "pin": "000001",
            "activo": None,
        },
        auth=auth,
    )
    data = response.json()

    assert response.status_code == 200
    assert data["rc"] == -1003
    assert data["msg"] == "Duplicated PIN"


def test_update_empleado_activo():
    """Debe regresar el campo en False solo cuando activo sea un string '0'"""
    empleados_data: List[dict] = _get_all_empleados()
    uuid: str = empleados_data[0]["id"]

    def do_put(activo_value) -> dict:
        """Funcion de ayuda para no repetir codigo"""
        response: Response = client.put(
            f"/empleados/{uuid}",
            json={
                "nombre": "Leonardo",
                "apellidos": "Pineda",
                "pin": "123123",
                "activo": activo_value,
            },
            auth=auth,
        )
        data = response.json()
        empleado = data["data"]
        assert response.status_code == 200
        assert data["rc"] == 0
        assert data["msg"] == "Ok"
        assert empleado["nombre_completo"] == "Leonardo Pineda"
        assert empleado["pin"] == "123123"
        assert _uuid.UUID(empleado["id"])
        return empleado

    # enviar activo con "0" debe regresar False
    empleado = do_put("0")
    assert not empleado["activo"]

    # enviar activo con 0 debe regresar True
    empleado = do_put(0)
    assert empleado["activo"]

    # enviar activo con null debe regresar True
    empleado = do_put(None)
    assert empleado["activo"]


# Authentications
def test_authentication():
    """Debe regresar un codigo 401 cuando no este authenticado

    Los distintos mensajes que debe regresar son:
      - Cuando no envia la auth:
        -- "Authentication credentials were not provided."
      - Cuando envia la auth pero no un token valido:
        -- "API Key invalido"
      - Cuando envia la auth y token valido pero no existe el api_key:
        -- "API Key invalida"
    """
    invalid_token = HTTPBasicAuth(
        username="5a25c9f25c334f4197df4d2aafca5fd", password=""
    )
    not_exists_token = HTTPBasicAuth(
        username="5a25c9f25c334f4197df4d2aafca5fd8", password=""
    )

    # No auth
    response: Response = client.get("/empleados")
    data = response.json()
    assert response.status_code == 401
    assert data["rc"] == -401
    assert data["msg"] == "Authentication credentials were not provided."

    # Token invalido
    response: Response = client.get("/empleados", auth=invalid_token)
    data = response.json()
    assert response.status_code == 401
    assert data["rc"] == -401
    assert data["msg"] == "API Key invalido"

    # Token no encontrado
    response: Response = client.get("/empleados", auth=not_exists_token)
    data = response.json()
    assert response.status_code == 401
    assert data["rc"] == -401
    assert data["msg"] == "API Key invalida"
