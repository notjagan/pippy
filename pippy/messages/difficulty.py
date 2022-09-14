from pathlib import Path
from typing import Any
from pippy.messages.request import Request
from pippy.utils import Mod


class DifficultyAttributes:
    """Data class containing difficulty information for a beatmap."""

    def __init__(
        self,
        star_rating: float,
        max_combo: int,
        aim_difficulty: float,
        speed_difficulty: float,
        speed_note_count: float,
        flashlight_difficulty: float,
        slider_factor: float,
        approach_rate: float,
        overall_difficulty: float,
        drain_rate: float,
        hit_circle_count: float,
        slider_count: float,
        spinner_count: float
    ):
        self.star_rating = star_rating
        self.max_combo = max_combo
        self.aim_difficulty = aim_difficulty
        self.speed_difficulty = speed_difficulty
        self.speed_note_count = speed_note_count
        self.flashlight_difficulty = flashlight_difficulty
        self.slider_factor = slider_factor
        self.approach_rate = approach_rate
        self.overall_difficulty = overall_difficulty
        self.drain_rate = drain_rate
        self.hit_circle_count = hit_circle_count
        self.slider_count = slider_count
        self.spinner_count = spinner_count

    def to_dict(self) -> dict[str, Any]:
        return {
            'star_rating': self.star_rating,
            'max_combo': self.max_combo,
            'aim_difficulty': self.aim_difficulty,
            'speed_difficulty': self.speed_difficulty,
            'speed_note_count': self.speed_note_count,
            'flashlight_difficulty': self.flashlight_difficulty,
            'slider_factor': self.slider_factor,
            'approach_rate': self.approach_rate,
            'overall_difficulty': self.overall_difficulty,
            'drain_rate': self.drain_rate,
            'hit_circle_count': self.hit_circle_count,
            'slider_count': self.slider_count,
            'spinner_count': self.spinner_count
        }


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
        return DifficultyAttributes(
            star_rating=attributes['star_rating'],
            max_combo=attributes['max_combo'],
            aim_difficulty=attributes['aim_difficulty'],
            speed_difficulty=attributes['speed_difficulty'],
            speed_note_count=attributes['speed_note_count'],
            flashlight_difficulty=attributes['flashlight_difficulty'],
            slider_factor=attributes['slider_factor'],
            approach_rate=attributes['approach_rate'],
            overall_difficulty=attributes['overall_difficulty'],
            drain_rate=attributes['drain_rate'],
            hit_circle_count=attributes['hit_circle_count'],
            slider_count=attributes['slider_count'],
            spinner_count=attributes['spinner_count']
        )

    def to_dict(self):
        return super().to_dict() | {
            'beatmap_path': str(self.beatmap_path.absolute()),
            'mods': [mod.value for mod in self.mods]
        }
