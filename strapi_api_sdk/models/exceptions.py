class StrapiExceptions(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AuthenticationError(StrapiExceptions):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UserError(StrapiExceptions):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ClientError(StrapiExceptions):
    def __init__(self, message: str) -> None:
        super().__init__(message)
