class BaseException(Exception):
    rc: int = -1000
    msg: str = "Error"

    def to_dict(self) -> dict:
        return {
            "rc": self.rc,
            "msg": self.msg,
        }


class NoEmpleadoError(BaseException):
    rc = -1001
    msg = "Please enter a valid id"


class InvalidEmpleadoError(BaseException):
    rc = -1002
    msg = "Invalid id"


class DuplicatedPinError(BaseException):
    rc = -1003
    msg = "Duplicated PIN"
