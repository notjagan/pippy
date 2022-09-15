import dataclasses
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


@dataclasses.dataclass
class ScoreInfo:
    """Data class containing metrics for an individual score."""
    count_300: int
    count_100: int
    count_50: int
    count_miss: int
    max_combo: int

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
