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


class PortainerWatcherError(PortainerError):
    """Exception raised for errors in the PortainerImageWatcher."""


class PortainerWatcherTimeoutError(PortainerWatcherError):
    """Exception raised when the PortainerImageWatcher times out."""


class PortainerWatcherConnectionError(PortainerWatcherError):
    """Exception raised when the PortainerImageWatcher encounters a connection error."""


class PortainerWatcherAuthenticationError(PortainerWatcherError):
    """Exception raised when the PortainerImageWatcher encounters an authentication error."""


class PortainerWatcherNotFoundError(PortainerWatcherError):
    """Exception raised when the PortainerImageWatcher cannot find a resource."""
