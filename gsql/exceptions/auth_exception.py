class AuthException(Exception):
    def __init__(self, message="Authentication failed") -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
