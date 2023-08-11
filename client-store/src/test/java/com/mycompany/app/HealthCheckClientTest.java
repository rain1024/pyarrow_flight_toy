package com.mycompany.app;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.nio.charset.StandardCharsets;
import java.util.Iterator;

import org.apache.arrow.flight.Action;
import org.apache.arrow.flight.FlightClient;
import org.apache.arrow.flight.Location;
import org.apache.arrow.flight.Result;
import org.apache.arrow.memory.RootAllocator;
import org.junit.Test;

public class HealthCheckClientTest {

    @Test
    public void testHealthCheckAction() throws InterruptedException {
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

                // Assert that the health status is as expected
                assertEquals("OK", healthStatus);
            }
        }
    }
}





