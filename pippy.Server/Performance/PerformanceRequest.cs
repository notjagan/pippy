using Newtonsoft.Json;
using osu.Game.Rulesets.Difficulty;
using osu.Game.Rulesets.Osu.Difficulty;

namespace pippy.Server.Performance {
    internal class PerformanceRequest : IRequest {
        public string Type { get; } = "performance";

        [JsonProperty("attributes")]
        public readonly OsuDifficultyAttributes DifficultyAttributes;

        [JsonProperty("score_info")]
        public readonly ScoreInfoWrapper ScoreInfo;

        public PerformanceRequest(OsuDifficultyAttributes attributes, ScoreInfoWrapper scoreInfo) {
            DifficultyAttributes = attributes;
            ScoreInfo = scoreInfo;
        }

        public IResponse GenerateResponse() {
            var calculator = new OsuPerformanceCalculator();
            var performanceAttributes = calculator.Calculate(ScoreInfo.ScoreInfo, DifficultyAttributes);
            return new PerformanceResponse(performanceAttributes);
        }
    }
}
