class LayeredArchitectureException(Exception):
    """Base exception for the layered architecture."""

    def __init__(
        self,
        code: str,
        details: str,
        message: str | None = None,
        key: str | None = None,
    ) -> None:
        """Initialize the exception.

        :param code: The error code
        :type code: str
        :param details: The error details
        :type details: str
        :param message: Optional error message
        :type message: str | None
        :param key: Optional key associated with the error
        :type key: str | None
        """
        self.code = code
        self.details = details
        self.message = message
        self.key = key
        super().__init__(details)


class NotFoundError(LayeredArchitectureException):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        message: str | None = None,
        key: str | None = None,
    ) -> None:

        details = f"{resource_type.capitalize()} {resource_id} not found"
        super().__init__(
            code="not_found",
            details=details,
            message=message,
            key=key,
        )
