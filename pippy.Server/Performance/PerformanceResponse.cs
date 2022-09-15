using Newtonsoft.Json;
using osu.Game.Rulesets.Difficulty;

namespace pippy.Server.Performance {
    internal class PerformanceResponse : IResponse {
        public string Type { get; } = "performance";

        [JsonProperty("pp")]
        public readonly double PerformancePoints;

        public PerformanceResponse(double performancePoints) {
            PerformancePoints = performancePoints;
        }
    }
}
