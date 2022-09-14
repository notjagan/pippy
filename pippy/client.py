from os import PathLike
from typing import Callable, Concatenate, TypeVar, ParamSpec

import zmq

from pippy.messages import DifficultyRequest, HeartbeatRequest, Request
from pippy.messages.difficulty import DifficultyAttributes
from pippy.messages.performance import PerformanceRequest
from pippy.utils import Mod, RequestProcessingError, ScoreStatistics

T = TypeVar('T')
P = ParamSpec('P')
RequestArgs = Concatenate['PippyClient', P]


def client_method(
    func: Callable[RequestArgs[P], Request[T]]
) -> Callable[RequestArgs[P], T]:
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
        # ensure connection is alive
        self.heartbeat()

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
        if not poller.poll(5000):
            raise RequestProcessingError("No response from pippy server")
        response = self.socket.recv_json()
        if not isinstance(response, dict):
            raise RequestProcessingError("Non-dictionary response from pippy server")
        return request.process_response(response)

    @client_method
    def heartbeat(self) -> HeartbeatRequest:
        """Sends a request to ensure the pippy server is alive."""
        return HeartbeatRequest()

    @client_method
    def get_difficulty_attributes(
        self,
        beatmap_path: str | bytes | PathLike,
        mods: list[Mod] | None=None
    ) -> DifficultyRequest:
        """Obtains difficulty information for a beatmap with the given mods."""
        if isinstance(beatmap_path, bytes):
            beatmap_path_str = beatmap_path.decode()
        else:
            beatmap_path_str = str(beatmap_path)
        if mods is None:
            mods = []
        return DifficultyRequest(beatmap_path_str, mods)

    @client_method
    def get_performance_attributes(
        self,
        difficulty_attributes: DifficultyAttributes,
        score_statistics: ScoreStatistics,
        mods: list[Mod] | None = None
    ) -> PerformanceRequest:
        """Obtains performance statistics for a play on a given map."""
        if mods is None:
            mods = []
        return PerformanceRequest(difficulty_attributes, score_statistics, mods)
