using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using osu.Game.Rulesets.Osu.Difficulty;
using System.Reflection;

namespace pippy.Server {
    internal static class Server {
        private static void Main() {
            var resolver = new OverrideContractResolver(new Dictionary<MemberInfo, JsonProperty> {
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
            var settings = new JsonSerializerSettings { ContractResolver = resolver };

            using var server = new ResponseSocket();
            server.Bind("tcp://*:7271");
            while (true) {
                try {
                    var message = server.ReceiveFrameString();

                    IRequest? request = null;
                    string? errorMessage = null;
                    try {
                        request = JsonConvert.DeserializeObject<IRequest>(message, settings);
                    } catch (JsonSerializationException) {
                        errorMessage = "Invalid request body";
                    } catch (Exception ex) {
                        errorMessage = "Unknown error while deserializing request";
                        Console.WriteLine("Error encountered while deserializing request:");
                        Console.WriteLine(ex.Message);
                    }

                    IResponse response;
                    if (request is null) {
                        response = new ErrorResponse(errorMessage);
                    } else {
                        response = request.GenerateResponse();
                    }

                    server.SendFrame(JsonConvert.SerializeObject(response, settings));
                } catch (Exception ex) {
                    Console.WriteLine("Unexpected error during server loop:");
                    Console.WriteLine(ex.Message);
                }
            }
        }
    }
}
