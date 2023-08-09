import pyarrow as pa
import pyarrow.flight

# Connect to the Flight server
client = pa.flight.connect("grpc://0.0.0.0:8080")

# List existing datasets
for flight in client.list_flights():
    descriptor = flight.descriptor
    print("Path:", descriptor.path[0].decode('utf-8'), "Rows:", flight.total_records, "Size:", flight.total_bytes)
    print("=== Schema ===")
    print(flight.schema)
    print("==============")
    print("")

# Upload a new dataset
ticket = pa.flight.Ticket(b'')

# Call the do_get method with the ticket to retrieve the data
reader = client.do_get(ticket)

# Read the data into a PyArrow table
table = reader.read_all()

# Print the table or do something else with the data
print(table)