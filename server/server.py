import pyarrow as pa
import pyarrow.flight as flight
import pathlib

class FlightServer(pa.flight.FlightServerBase):
    def __init__(self, location="grpc://0.0.0.0:5050",
                 repo=pathlib.Path("./datasets"), **kwargs):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._repo = repo

    def list_actions(self, context):
        return [flight.ActionType("health_check", "Check the system's health")]

    def do_action(self, context, action):
        if action.type == "health_check":
            # Perform the health check logic here
            # Return the status of the system
            health_status = "OK"
            return iter([flight.Result(health_status.encode("utf-8"))])
        raise flight.FlightUnavailableError("Unknown action!")

def serve():
    location = "grpc://0.0.0.0:5050"
    server = FlightServer(location)
    print("Server is running on:", location)
    server.serve()

if __name__ == "__main__":
    serve()
