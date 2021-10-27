class UnexpectedException(Exception):
    def __init__(self, message="An unexpected exception has occured") -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
