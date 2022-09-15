using Newtonsoft.Json;

namespace pippy.Server {
    internal class ErrorResponse : IResponse {
        public string Type { get; } = "error";

        [JsonProperty("message", NullValueHandling = NullValueHandling.Ignore)]
        public string? Message { get; } = null;

        public ErrorResponse(string? message) {
            Message = message;
        }
    }
}
