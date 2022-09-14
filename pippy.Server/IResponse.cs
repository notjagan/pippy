using Newtonsoft.Json;

namespace pippy.Server {
    internal interface IResponse {
        [JsonProperty("type")]
        string Type { get; }
    }
}
