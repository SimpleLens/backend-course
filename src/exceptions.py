
from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = ""

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NabronirovalException):
    detail = "Сущность не найдена"

class HotelNotFoundException(NabronirovalException):
    detail = "Отель не найден"

class RoomNotFoundException(NabronirovalException):
    detail = "Комната не найдена"

class DatesAreNotSuitableException(NabronirovalException):
    detail = "Дата выезда не может быть раньше даты заезда"


class AllRoomsAreBooked(NabronirovalException):
    detail = "Все номера забронированы"

class ObjectAlreadyExists(NabronirovalException):
    detail = "Подобный объект уже существует"

class UserAlreadyExistsException(NabronirovalException):
    detail = "Подобный пользователь уже существует"

class UserDoesNotExistException(NabronirovalException):
    detail = "Пользователя не существует"

class PasswordIsIncorrectException(NabronirovalException):
    detail = "Пароль неверный"


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code= self.status_code, detail = self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class DatesAreNotSuitableHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Дата выезда не может быть раньше даты заезда"

class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Комната не найдена"

class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Все комнаты заняты"

class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Подобный пользователь уже существует"

class UserDoesNotExistHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователя не существует"

class PasswordIsIncorrectHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пароль неверный"