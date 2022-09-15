using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using osu.Game.Rulesets.Osu.Difficulty;
using System.Reflection;

namespace pippy.Server {

    static class ResponseSocketExtensions {

        private static readonly OverrideContractResolver Resolver = new(new Dictionary<MemberInfo, JsonProperty> {
            {
                typeof(OsuDifficultyAttributes).GetProperty("DrainRate")!,
                new JsonProperty { PropertyName = "drain_rate" }
            },
            {
                typeof(OsuDifficultyAttributes).GetProperty("HitCircleCount")!,
                new JsonProperty { PropertyName = "hit_circle_count" }
            },
            {
                typeof(OsuDifficultyAttributes).GetProperty("SliderCount")!,
                new JsonProperty { PropertyName = "slider_count" }
            },
            {
                typeof(OsuDifficultyAttributes).GetProperty("SpinnerCount")!,
                new JsonProperty { PropertyName = "spinner_count" }
            }
        });
        private static readonly JsonSerializerSettings Settings = new() { ContractResolver = Resolver };

        public static void Send(this ResponseSocket server, IResponse response) {
            server.SendFrame(JsonConvert.SerializeObject(response, Settings));
            
        }

        public static T Receive<T>(this ResponseSocket server) {
            return JsonConvert.DeserializeObject<T>(server.ReceiveFrameString(), Settings)!;
        }
    }
}
