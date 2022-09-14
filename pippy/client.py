from abc import ABC, abstractmethod, abstractproperty
from types import NoneType
from typing import Any, Callable, Concatenate, Generic, TypeVar, ParamSpec

import zmq

T = TypeVar('T')
P = ParamSpec('P')
RequestArgs = Concatenate['PippyClient', P]


class RequestProcessingError(Exception):
    """Exception class for failure during communication with pippy server"""


class Request(ABC, Generic[T]):
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


class HeartbeatRequest(Request[NoneType]):
    @classmethod
    @property
    def request_type(cls):
        return 'heartbeat'

    def _process_response(self, _: dict[str, Any]):
        return None

    def to_dict(self):
        return super().to_dict()


def client_method(func: Callable[RequestArgs[P], Request[T]]) -> Callable[RequestArgs[P], T]:
    """Decorator for methods that return a request to be processed by the client."""
    def wrapper(client: 'PippyClient', *args: P.args, **kwargs: P.kwargs) -> T:
        request = func(client, *args, **kwargs)
        return client.process_request(request)
    return wrapper


class PippyClient:
    def __init__(self, port: int=7271):
        """Creates a new pippy client."""
        self.context = zmq.Context()
        self.port = port
        self.socket: zmq.Socket = self.context.socket(zmq.REQ)

    def start(self):
        """Connects to the pippy server."""
        self.socket.connect(f'tcp://localhost:{self.port}')

    def stop(self):
        """Disconnects from the pippy server."""
        self.socket.disconnect(f'tcp://localhost:{self.port}')

    def __enter__(self):
        """Connects to the pippy server."""
        self.start()
        return self

    def __exit__(self, *_):
        """Disconnects from the pippy server."""
        self.stop()
        return False
    
    def process_request(self, request: Request[T]) -> T:
        """Sends a request to the pippy server and decodes the ensuing response."""
        message = request.to_dict()
        self.socket.send_json(message)
        poller = zmq.Poller()
        poller.register(self.socket)
        response = None
        if not poller.poll(1000):
            raise RequestProcessingError("No response from pippy server")
        response = self.socket.recv_json()
        if not isinstance(response, dict):
            raise RequestProcessingError("Non-dictionary response from pippy server")
        return request.process_response(response)

    @client_method
    def heartbeat(self) -> HeartbeatRequest:
        """Sends a request to ensure the pippy server is alive."""
        return HeartbeatRequest()
