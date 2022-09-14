using JsonSubTypes;
using Newtonsoft.Json;

namespace pippy.Server {
    [JsonConverter(typeof(JsonSubtypes), "Type")]
    [JsonSubtypes.KnownSubType(typeof(HeartbeatRequest), "heartbeat")]
    internal interface IRequest {
        [JsonProperty("type")]
        string Type { get; }

        IResponse GenerateResponse();
    }
}
