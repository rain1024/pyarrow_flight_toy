import pyarrow as pa
import pyarrow.flight as flight
import pathlib
import pandas as pd


class FlightServer(pa.flight.FlightServerBase):
    def __init__(self, location="grpc://0.0.0.0:5050",
                 repo=pathlib.Path("./datasets"), **kwargs):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._repo = repo

    def list_actions(self, context):
        return [flight.ActionType("health_check", "Check the system's health")]

    def get_flight_info(self, context, descriptor):
        if descriptor.type == flight.ActionType.COMMAND:
            if descriptor.command == "do_exchange":
                # Create a FlightInfo object for the do_exchange command
                return flight.FlightInfo(
                    flight.FlightDescriptor.for_command("do_exchange"),
                    [flight.FlightEndpoint(self._location)],
                    [flight.ActionType("do_exchange", "Perform a data exchange")]
                )
        raise flight.FlightUnavailableError("Unknown action!")

    def do_action(self, context, action):
        if action.type == "health_check":
            # Perform the health check logic here
            # Return the status of the system
            health_status = "OK"
            return iter([flight.Result(health_status.encode("utf-8"))])
        raise flight.FlightUnavailableError("Unknown action!")
    
    def do_exchange(self, context, descriptor, reader, writer):
        # Extract the transaction data from the reader
        transaction_data = self._read_transaction_data(reader)

        # Process the exchange transaction and update inventory
        response_payload = self._process_exchange(transaction_data)

        # Create a FlightStreamWriter to send the response
        with flight.FlightStreamWriter(writer) as flight_writer:
            # Write the response payload to the stream
            response_record = pa.RecordBatch.from_pandas(pd.DataFrame({"response": [response_payload]}))
            flight_writer.write_table(pa.Table.from_batches([response_record]))
    
    def _read_transaction_data(self, reader):
        return [1, 2, 3]

    def _process_exchange(self, transaction_data):
        # In this example, simply return the array [1, 2, 3, 4]
        response_payload = pa.array([1, 2, 3, 4])
        return response_payload

def serve():
    location = "grpc://0.0.0.0:5050"
    server = FlightServer(location)
    print("Server is running on:", location)
    server.serve()

if __name__ == "__main__":
    serve()
