from types import NoneType
from typing import Any
from pippy.messages.request import Request


class HeartbeatRequest(Request[NoneType]):
    """Request to ensure connection with server is alive."""

    @classmethod
    @property
    def request_type(cls):
        return 'heartbeat'

    def _process_response(self, _: dict[str, Any]):
        return None

    def to_dict(self):
        return super().to_dict()
