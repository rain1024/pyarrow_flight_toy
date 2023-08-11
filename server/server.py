# server.py

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

    def do_action(self, context, action):
        if action.type == "health_check":
            health_status = "OK"
            return iter([flight.Result(health_status.encode("utf-8"))])
        raise flight.FlightUnavailableError("Unknown action!")

    def do_exchange(self, context, descriptor, reader, writer):
        print("Server received descriptor command:", descriptor.command)
        
        print(reader)
        print(writer)
        # Read the incoming data
        incoming_table = reader.read_all()
        print('\n+ Incoming Table\n', incoming_table)

        # Process the data
        processed_data = self._process_exchange(incoming_table)

        # Create a DataFrame from the processed data
        response_df = pd.DataFrame({"data": processed_data})

        # Convert the DataFrame to a RecordBatch
        record_batch = pa.RecordBatch.from_pandas(response_df)

        # Convert the RecordBatch to a Table
        table = pa.Table.from_batches([record_batch])
        print('\n+ Result Table\n', table)

        print('\nreader.schema', reader.schema)
        print('\ntable.schema', table.schema)

        # Initialize the writer with the schema
        writer.begin(table.schema)

        # Write the Table to the client
        writer.write_table(table)
        writer.close()

        # Close the writer
        writer.close()

    def _process_exchange(self, incoming_table):
        # Convert the incoming table to a Pandas DataFrame
        incoming_df = incoming_table.to_pandas()

        # Double the values in the "data" column
        incoming_df["data"] = incoming_df["data"] * 2

        # Return the modified "data" column
        return incoming_df["data"]

def serve():
    location = "grpc://0.0.0.0:5050"
    server = FlightServer(location)
    print("Server is running on:", location)
    server.serve()

if __name__ == "__main__":
    serve()
