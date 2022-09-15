import dataclasses
from os import PathLike
from pathlib import Path

from pippy.client import PippyClient
from pippy.messages.difficulty import DifficultyAttributes
from pippy.utils import Mod, ScoreInfo


class PerformanceCalculator:
    """Class to calculate performance attributes of plays on an individual map."""

    def __init__(self, beatmap_path: Path, mods: list[Mod]):
        self.client = PippyClient()
        self.client.start()
        self.beatmap_path = beatmap_path
        self.mods = mods

    def _get_beatmap_attributes(self):
        """Helper method to calculate difficulty attributes for the stored map."""
        self.difficulty_attributes = self.client.get_difficulty_attributes(
            self.beatmap_path,
            self.mods
        )
        self.max_combo = self.client.get_max_combo(self.beatmap_path)

    @property
    def mods(self) -> list[Mod]:
        """Difficulty modifiers used for performance calculation."""
        return self._mods

    @mods.setter
    def mods(self, value: list[Mod]):
        """Sets difficulty modifiers and recalculates difficulty attributes."""
        self._mods = value
        self._get_beatmap_attributes()

    def __del__(self):
        """Override to ensure client is disconnected before object deletion."""
        self.client.stop()
        del self

    @classmethod
    def from_beatmap_path(
        cls,
        beatmap_path: str | PathLike,
        mods: list[Mod] | None=None
    ) -> 'PerformanceCalculator':
        """Constructs a new calculator from a path-like beatmap and a list of mods."""
        if mods is None:
            mods = []
        return PerformanceCalculator(Path(beatmap_path), mods)

    def calculate_pp(self, score_info: ScoreInfo, fc=False) -> float:
        """Calculates total pp value for a given play."""
        score_info = dataclasses.replace(score_info)
        if fc:
            score_info.count_300 += score_info.count_miss
            score_info.count_miss = 0
            score_info.max_combo = self.max_combo
        return self.client.get_pp(
            self.difficulty_attributes,
            score_info,
            self.mods
        )
