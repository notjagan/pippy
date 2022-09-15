from pippy.messages.request import Request


class HeartbeatRequest(Request[None]):
    """Request to ensure connection with server is alive."""

    @classmethod
    @property
    def request_type(cls):
        return 'heartbeat'

    def _process_response(self, _):
        return None
