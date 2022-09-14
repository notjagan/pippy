from pippy.messages.request import Request
from pippy.messages.difficulty import DifficultyAttributes
from pippy.utils import Mod, ScoreStatistics


class PerformanceAttributes:
    """Data class containing performance statistics on a given play."""

    def __init__(
        self,
        aim: float,
        speed: float,
        accuracy: float,
        flashlight: float,
        effective_miss_count: float,
        pp: float
    ):
        self.aim = aim
        self.speed = speed
        self.accuracy = accuracy
        self.flashlight = flashlight
        self.effective_miss_count = effective_miss_count
        self.pp = pp


class PerformanceRequest(Request[PerformanceAttributes]):
    """Request to calculate performance for a given play."""

    @classmethod
    @property
    def request_type(cls):
        return 'performance'

    def __init__(
        self,
        difficulty_attributes: DifficultyAttributes,
        score_statistics: ScoreStatistics,
        mods: list[Mod]
    ):
        self.difficulty_attributes = difficulty_attributes
        self.score_statistics = score_statistics
        self.mods = mods

    def _process_response(self, data):
        performance_attributes = data['attributes']
        return PerformanceAttributes(
            aim=performance_attributes['aim'],
            speed=performance_attributes['speed'],
            accuracy=performance_attributes['accuracy'],
            flashlight=performance_attributes['flashlight'],
            effective_miss_count=performance_attributes['effective_miss_count'],
            pp=performance_attributes['pp'],
        )

    def to_dict(self):
        return super().to_dict() | {
            'attributes': self.difficulty_attributes.to_dict(),
            'statistics': self.score_statistics.to_dict() | {
                'mods': [mod.value for mod in self.mods]
            }
        }
