using Newtonsoft.Json;
using osu.Game.Rulesets.Difficulty;

namespace pippy.Server.Performance {
    internal class PerformanceResponse : IResponse {
        public string Type { get; } = "performance";

        [JsonProperty("attributes")]
        public readonly PerformanceAttributes PerformanceAttributes;

        public PerformanceResponse(PerformanceAttributes attributes) {
            PerformanceAttributes = attributes;
        }
    }
}
