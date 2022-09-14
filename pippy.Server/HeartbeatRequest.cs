namespace pippy.Server {
    internal class HeartbeatRequest : IRequest {
        public string Type { get; } = "heartbeat";

        public IResponse GenerateResponse() => new HeartbeatResponse();
    }
}
