class ArgumentException(Exception):
    def __init__(self, arglist, message="Invalid number of arguments provided") -> None:
        super().__init__(message)
        self.message = message
        self.arglist = arglist
