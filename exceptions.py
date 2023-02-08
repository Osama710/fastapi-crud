# exceptions.py
class ItemException(Exception):
    ...


class ItemNotFoundError(ItemException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Car Info Not Found"


class ItemAlreadyExistError(ItemException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Car Info Already Exists"
