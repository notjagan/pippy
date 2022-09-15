from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Generic, TypeVar

from pippy.utils import RequestProcessingError

T = TypeVar('T')


class Request(ABC, Generic[T]):
    """Abstract class representing a request to the pippy server."""

    @classmethod
    @abstractproperty
    def request_type(cls) -> str:
        """Type name associated with request class."""
        raise NotImplementedError()

    @abstractmethod
    def _process_response(self, data: dict[str, Any]) -> T:
        """Helper method to convert a response to the desired return type."""
        raise NotImplementedError()

    def process_response(self, data: dict[str, Any]) -> T:
        """Processes a pippy server response and deserializes the encoded object."""
        if data['type'] == 'error':
            raise RequestProcessingError(data['message'])
        elif data['type'] == self.request_type:
            return self._process_response(data)
        else:
            raise RequestProcessingError("Unexpected message type from pippy server")

    def to_dict(self) -> dict[str, Any]:
        """Produces a JSON-serializable dictionary encoding relevant fields."""
        return { 'type': self.request_type }
