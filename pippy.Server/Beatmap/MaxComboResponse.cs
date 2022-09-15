using Newtonsoft.Json;

namespace pippy.Server.Beatmap {
    internal class MaxComboResponse : IResponse {
        public string Type { get; } = "max_combo";

        [JsonProperty("max_combo")]
        public readonly int MaxCombo;

        public MaxComboResponse(int maxCombo) {
            MaxCombo = maxCombo;
        }
    }
}
