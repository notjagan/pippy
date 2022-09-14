using Newtonsoft.Json;
using osu.Game.Rulesets.Osu.Difficulty;

namespace pippy.Server.Performance {
    internal class DifficultyResponse : IResponse {
        public string Type { get; } = "difficulty";

        [JsonProperty("attributes")]
        public OsuDifficultyAttributes DifficultyAttributes;

        public DifficultyResponse(OsuDifficultyAttributes attributes) {
            DifficultyAttributes = attributes;
        }
    }
}
