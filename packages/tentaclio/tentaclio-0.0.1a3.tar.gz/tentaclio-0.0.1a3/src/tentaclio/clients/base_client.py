"""Base defines a common contract for connecting, closing, managing context for clients."""
import abc
from typing import ContextManager, Iterable, TypeVar, Union, cast

from typing_extensions import Protocol

from tentaclio import protocols, urls


T = TypeVar("T")

__all__ = ["Streamer"]


class Streamer(Protocol):
    """Interface for stream-based connections."""

    # Stream methods:

    @abc.abstractmethod
    def get(self, writer: protocols.ByteWriter, **params) -> None:
        """Read the contents from the stream and write them the the ByteWriter."""
        ...

    @abc.abstractmethod
    def put(self, reader: protocols.ByteReader, **params) -> None:
        """Write the contents of the reader into the client stream."""
        ...


class BaseClient(ContextManager[T], metaclass=abc.ABCMeta):
    """Abstract base class for clients, wrapping a connection.

    Offers context managing, connecting and closing functionalities.
    """

    url: urls.URL
    conn: protocols.Closable
    allowed_schemes: Iterable[str] = []
    closed: bool = True

    def __init__(self, url: Union[urls.URL, str]) -> None:
        """Create a new client based on a URL object or a string containing a url."""
        if isinstance(url, str):
            url = urls.URL(url)
        self.url = url
        if self.url.scheme not in self.allowed_schemes:
            raise ValueError(
                f"Allowed schemes for {type(self).__name__} are {self.allowed_schemes}; "
                f"found '{self.url.scheme}'"
            )

    # Context manager:

    def __enter__(self) -> T:
        """Connect to the resource when entering the context."""
        self.conn = self.connect()
        return cast(T, self)

    def __exit__(self, *args) -> None:
        """Close the connection when leaving the context."""
        self.close()

    # Connection methods:

    def connect(self) -> protocols.Closable:
        """Connect to the resource when entering the context."""
        self.closed = False
        return self._connect()

    @abc.abstractmethod
    def _connect(self) -> protocols.Closable:
        """Connect to the resource. This method needs to be overwritten by child classes."""
        ...

    def close(self) -> None:
        """Close the client connection."""
        if not self.closed:
            self.conn.close()
            self.closed = True
