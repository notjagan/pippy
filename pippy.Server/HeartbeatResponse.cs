namespace pippy.Server {
    internal class HeartbeatResponse : IResponse {
        public string Type { get; } = "heartbeat";
    }
}
