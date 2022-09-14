using Newtonsoft.Json;
using osu.Game.Rulesets.Difficulty;

namespace pippy.Server.Performance {
    internal class DifficultyResponse : IResponse {
        public string Type { get; } = "difficulty";/

        [JsonProperty("attributes")]
        public DifficultyAttributes Attributes;

        public DifficultyResponse(DifficultyAttributes attributes) {
            Attributes = attributes;
        }
    }
}
