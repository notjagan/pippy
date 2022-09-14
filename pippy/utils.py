from enum import Enum


class RequestProcessingError(Exception):
    """Exception class for failure during communication with pippy server"""


class Mod(Enum):
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
