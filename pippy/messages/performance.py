from pippy.messages.request import Request
from pippy.messages.difficulty import DifficultyAttributes
from pippy.utils import Mod, ScoreInfo


class PerformanceRequest(Request[float]):
    """Request to calculate performance for a given play."""

    @classmethod
    @property
    def request_type(cls):
        return 'performance'

    def __init__(
        self,
        difficulty_attributes: DifficultyAttributes,
        score_info: ScoreInfo,
        mods: list[Mod]
    ):
        self.difficulty_attributes = difficulty_attributes
        self.score_info = score_info
        self.mods = mods

    def _process_response(self, data):
        return data['pp']

    def to_dict(self):
        return super().to_dict() | {
            'attributes': self.difficulty_attributes.to_dict(),
            'score_info': self.score_info.to_dict() | {
                'mods': [mod.value for mod in self.mods]
            }
        }
