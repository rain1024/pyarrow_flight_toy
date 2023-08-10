package com.mycompany.app;
import org.apache.arrow.flight.*;
import org.apache.arrow.memory.RootAllocator;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;

public class HealthCheckClient {
    public static void main(String[] args) throws InterruptedException {
        // Create a new root allocator
        final RootAllocator allocator = new RootAllocator(Long.MAX_VALUE);

        // Connect to the Flight server
        try (FlightClient client = FlightClient.builder(allocator, Location.forGrpcInsecure("localhost", 5050)).build()) {
            // Define the action
            Action action = new Action("health_check", new byte[0]);

            // Perform the action
            Iterator<Result> results = client.doAction(action);

            // Process the results
            while (results.hasNext()) {
              Result result = results.next();
              byte[] bytes = result.getBody();
              String healthStatus = new String(bytes, StandardCharsets.UTF_8);
              System.out.println("Health Status: " + healthStatus); // Output: OK
            }
        }
    }
}
