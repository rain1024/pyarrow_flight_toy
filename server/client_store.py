import click
import pyarrow.flight as flight
import pyarrow as pa
import pandas as pd

@click.command()
@click.option('--server', default="grpc://0.0.0.0:5050", help='Flight server URL')
@click.option('--action', type=click.Choice(['health_check', 'do_exchange']), default='health_check', help='Choose action')
def main(server, action):
    """Perform an action on the Flight server."""
    if action == 'health_check':
        health_check(server)
    elif action == 'do_exchange':
        do_exchange(server)

def health_check(server):
    """Perform a health check on the Flight server."""
    client = flight.FlightClient(server)
    action = flight.Action("health_check", b"")
    results = client.do_action(action)

    for result in results:
        print("Health Status:", result.body.to_pybytes().decode("utf-8"))

def do_exchange(server):
    """Perform a data exchange on the Flight server."""
    client = flight.FlightClient(server)

    # Create a FlightDescriptor for the do_exchange command
    descriptor = flight.FlightDescriptor.for_command("do_exchange")

    # Send the command and get a FlightInfo response
    flight_info = client.get_flight_info(descriptor)

    # Check if the action is supported by the server
    if not flight_info.actions[0].type == flight.ActionType.COMMAND:
        print("Server does not support do_exchange command.")
        return

    # Create a FlightStreamWriter to send any necessary data (if needed)
    writer, metadata_reader = client.do_exchange(descriptor)

    # Close the FlightStreamWriter to indicate the end of data
    writer.close()

    # Read and process the response metadata
    response = metadata_reader.read_all()
    response_payload = response[0].column(0)[0].as_py()
    print("Exchange Response:", response_payload)

if __name__ == '__main__':
    main()
