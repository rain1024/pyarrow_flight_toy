package com.mycompany.app;
import org.apache.arrow.flight.*;
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.VectorSchemaRoot;

public class ArrowClient {
    public static void main(String[] args) {
        Location location = Location.forGrpcInsecure("localhost", 8080);
        BufferAllocator allocator = new RootAllocator(Long.MAX_VALUE);

        try (FlightClient client = FlightClient.builder()
                .allocator(allocator)
                .location(location)
                .build()) {

            // Create a Ticket object for the data you want to retrieve
            byte[] ticketBytes = "".getBytes(); // Requesting 'data1'
            Ticket ticket = new Ticket(ticketBytes);

            // Retrieve the data stream for the given ticket
            try (FlightStream stream = client.getStream(ticket)) {
                while (stream.next()) {
                    VectorSchemaRoot root = stream.getRoot();
                    try {
                        System.out.println(root);
                    } finally {
                        root.close(); // Close the root to release the memory
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            allocator.close();
        }
    }
}
