class MainException(Exception):
    """
    Base class for other exceptions.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnauthorizedAccess(MainException):
    """
    Exception raised when the jwt token is invalid or expired.
    """

    def __init__(self, message):
        super().__init__(message)


class InvalidFileFormat(MainException):
    """
    Exception raised when the file format is not supported.
    """

    def __init__(self, format: str):
        super().__init__(f"The file format {format} is not supported.")


class S3ObjectNotFound(MainException):
    """
    Exception raised when the bucket is not found.
    """

    def __init__(self, message):
        super().__init__(f"The S3 object not found: {message}")


class S3Exeption(MainException):
    """
    Exception raised when the error occurs in the S3 bucket.
    """

    def __init__(self, message):
        super().__init__(f"An error occurred in the S3 bucket: {message}")
