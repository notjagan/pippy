using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;

namespace pippy.Server {
    internal static class Server {
        private static void Main() {
            using var server = new ResponseSocket();
            server.Bind("tcp://*:7271");
            while (true) {
                try {
                    var message = server.ReceiveFrameString();

                    IRequest? request = null;
                    string? errorMessage = null;
                    try {
                        request = JsonConvert.DeserializeObject<IRequest>(message);
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

                    server.SendFrame(JsonConvert.SerializeObject(response));
                } catch (Exception ex) {
                    Console.WriteLine("Unexpected error during server loop:");
                    Console.WriteLine(ex.Message);
                }
            }
        }
    }
}
