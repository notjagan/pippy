from pathlib import Path
from pippy.messages.request import Request


class MaxComboRequest(Request[int]):
    """Request to calculate maximum combo attainable on a beatmap."""

    @classmethod
    @property
    def request_type(cls):
        return 'max_combo'

    def __init__(self, beatmap_path: Path):
        self.beatmap_path = beatmap_path

    def _process_response(self, data):
        return data['max_combo']

    def to_dict(self):
        return super().to_dict() | {
            'beatmap_path': str(self.beatmap_path.absolute())
        }
