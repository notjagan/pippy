using JsonSubTypes;
using Newtonsoft.Json;
using pippy.Server.Beatmap;
using pippy.Server.Performance;

namespace pippy.Server {
    [JsonConverter(typeof(JsonSubtypes), "Type")]
    [JsonSubtypes.KnownSubType(typeof(HeartbeatRequest), "heartbeat")]
    [JsonSubtypes.KnownSubType(typeof(DifficultyRequest), "difficulty")]
    [JsonSubtypes.KnownSubType(typeof(PerformanceRequest), "performance")]
    [JsonSubtypes.KnownSubType(typeof(MaxComboRequest), "max_combo")]
    internal interface IRequest {
        [JsonProperty("type")]
        string Type { get; }

        IResponse GenerateResponse();
    }
}
