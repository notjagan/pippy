using Newtonsoft.Json;
using osu.Game.Rulesets.Difficulty;
using osu.Game.Rulesets.Osu;
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
            var calculator = new OsuPerformanceCalculator(new OsuRuleset(), DifficultyAttributes, ScoreInfo.ScoreInfo);
            var performanceAttributes = calculator.Calculate();
            return new PerformanceResponse(performanceAttributes);
        }
    }
}
