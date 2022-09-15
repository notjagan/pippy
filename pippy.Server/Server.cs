using NetMQ.Sockets;
using Newtonsoft.Json;

namespace pippy.Server {
    internal static class Server {
        private static void Main() {
            Console.WriteLine("Starting server on port 7271.");
            using var server = new ResponseSocket();
            server.Bind("tcp://*:7271");
            while (true) {
                IRequest request;
                try {
                    request = server.Receive<IRequest>();
                    Console.WriteLine("Received request of type {0}.", request.GetType());
                } catch (JsonSerializationException ex) {
                    var message = String.Format("Invalid request body: {0}", ex.Message);
                    server.Send(new ErrorResponse(message));
                    continue;
                }

                try {
                    var response = request.GenerateResponse();
                    server.Send(response);
                } catch (Exception ex) {
                    Console.WriteLine("Error encountered while sending response:");
                    Console.WriteLine(ex.Message);
                    var message = String.Format("Unknown error while sending response: {0}", ex.Message);
                    server.Send(new ErrorResponse(message));
                }
            }
        }
    }
}
