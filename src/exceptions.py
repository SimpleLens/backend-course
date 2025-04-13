
class NabronirovalException(Exception):
    detail = ""

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NabronirovalException):
    detail = "Сущность не найдена"

class AllRoomsAreBooked(NabronirovalException):
    detail = "Все номера забронированы"
