from os import PathLike
from pathlib import Path

from pippy.client import PippyClient
from pippy.messages.difficulty import DifficultyAttributes
from pippy.messages.performance import PerformanceAttributes
from pippy.utils import Mod, ScoreInfo


class PerformanceCalculator:
    """Class to calculate performance attributes of plays on an individual map."""

    def __init__(self, beatmap_path: Path, mods: list[Mod]):
        self.client = PippyClient()
        self.client.start()
        self.beatmap_path = beatmap_path
        self.mods = mods

    def _get_difficulty_attributes(self) -> DifficultyAttributes:
        """Helper method to calculate difficulty attributes for the stored map."""
        return self.client.get_difficulty_attributes(
            self.beatmap_path,
            self.mods
        )

    @property
    def mods(self) -> list[Mod]:
        """Difficulty modifiers used for performance calculation."""
        return self._mods

    @mods.setter
    def mods(self, value: list[Mod]):
        """Sets difficulty modifiers and recalculates difficulty attributes."""
        self._mods = value
        self.difficulty_attributes = self._get_difficulty_attributes()

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

    def calculate_performance(self, score_info: ScoreInfo) -> PerformanceAttributes:
        """Calculates performance attributes for a given play."""
        return self.client.get_performance_attributes(
            self.difficulty_attributes,
            score_info,
            self.mods
        )

    def calculate_pp(self, score_info: ScoreInfo) -> float:
        """Calculates total pp value for a given play."""
        performance_attributes = self.calculate_performance(score_info)
        return performance_attributes.pp
