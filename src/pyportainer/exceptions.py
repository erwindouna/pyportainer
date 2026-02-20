"""Asynchronous Python client for Python Portainer."""


class PortainerError(Exception):
    """Generic exception for Portainer errors."""


class PortainerConnectionError(PortainerError):
    """Exception raised for connection errors."""


class PortainerTimeoutError(PortainerError):
    """Exception raised for timeout errors."""


class PortainerAuthenticationError(PortainerError):
    """Exception raised for authentication errors."""


class PortainerNotFoundError(PortainerError):
    """Exception raised when a resource is not found."""
