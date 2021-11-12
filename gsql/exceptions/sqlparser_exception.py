

class SQLStatmentException(Exception):
    def __init__(self, message="Invalid SQL statement") -> None:
        super().__init__(message)
        self.message = message