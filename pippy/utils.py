from enum import Enum
from typing import Any


class RequestProcessingError(Exception):
    """Exception class for failure during communication with pippy server"""


class Mod(Enum):
    """Enum representing difficulty modifiers."""
    Easy = 'EZ'
    NoFail = 'NF'
    HalfTime = 'HT'
    HardRock = 'HR'
    SuddenDeath = 'SD'
    Perfect = 'PF'
    DoubleTime = 'DT'
    NightCore = 'NC'
    Hidden = 'HD'
    Flashlight = 'FL'
    Relax = 'RX'
    Autopilot = 'AP'
    SpunOut = 'SO'
    Auto = 'AT'
    Cinema = 'CM'
    ScoreV2 = 'SV2'
    TargetPractice = 'TP'


class ScoreStatistics:
    """Data class containing metrics for an individual score."""

    def __init__(
        self,
        count_300: int,
        count_100: int,
        count_50: int,
        count_miss: int,
        max_combo: int
    ):
        self.count_300 = count_300
        self.count_100 = count_100
        self.count_50 = count_50
        self.count_miss = count_miss
        self.max_combo = max_combo

    def to_dict(self) -> dict[str, Any]:
        return {
            'count_300': self.count_300,
            'count_100': self.count_100,
            'count_50': self.count_50,
            'count_miss': self.count_miss,
            'max_combo': self.max_combo
        }
