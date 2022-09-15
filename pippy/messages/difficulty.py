from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from pippy.messages.request import Request
from pippy.utils import Mod


@dataclass
class DifficultyAttributes:
    """Data class containing difficulty information for a beatmap."""
    star_rating: float
    max_combo: int
    aim_strain: float
    speed_strain: float
    slider_factor: float
    approach_rate: float
    overall_difficulty: float
    drain_rate: float
    hit_circle_count: float
    slider_count: float
    spinner_count: float
    flashlight_rating: float | None=None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if data['flashlight_rating'] is None:
            data.pop('flashlight_rating')
        return data


class DifficultyRequest(Request[DifficultyAttributes]):
    """Request to calculate difficulty attributes for a given beatmap."""

    @classmethod
    @property
    def request_type(cls):
        return 'difficulty'

    def __init__(self, beatmap_path: Path, mods: list[Mod]):
        self.beatmap_path = beatmap_path
        self.mods = mods

    def _process_response(self, data):
        attributes = data['attributes']
        return DifficultyAttributes(**attributes)

    def to_dict(self):
        return super().to_dict() | {
            'beatmap_path': str(self.beatmap_path.absolute()),
            'mods': [mod.value for mod in self.mods]
        }
