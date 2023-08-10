import pyarrow.flight as flight

# Connect to the Flight server using the constructor
client = flight.FlightClient("grpc://0.0.0.0:5050")

# Define the action
action = flight.Action("health_check", b"")

# Perform the action
results = client.do_action(action)

# Process the results
for result in results:
    print("Health Status:", result.body.to_pybytes().decode("utf-8")) 