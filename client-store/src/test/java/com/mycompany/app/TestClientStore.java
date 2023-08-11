package com.mycompany.app;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Iterator;

import org.apache.arrow.flight.Action;
import org.apache.arrow.flight.FlightClient;
import org.apache.arrow.flight.Location;
import org.apache.arrow.flight.Result;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.flight.FlightDescriptor;
import org.apache.arrow.flight.FlightStream;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.types.pojo.ArrowType;
import org.apache.arrow.vector.types.pojo.Field;
import org.apache.arrow.vector.types.pojo.Schema;
import org.junit.jupiter.api.Test;

public class TestClientStore {

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

    @Test
    public void testDoExchange() throws Exception {
        // Create a new root allocator
        final RootAllocator allocator = new RootAllocator(Long.MAX_VALUE);

        // Connect to the Flight server
        try (FlightClient client = FlightClient.builder(allocator, Location.forGrpcInsecure("localhost", 5050)).build()) {
            // Define the descriptor
            FlightDescriptor descriptor = FlightDescriptor.command("do_exchange".getBytes(StandardCharsets.UTF_8));

            // Create a schema for the data
            Schema schema = new Schema(Arrays.asList(Field.nullable("data", new ArrowType.Int(32, true))));

            // Create a VectorSchemaRoot with sample data
            VectorSchemaRoot root = VectorSchemaRoot.create(schema, allocator);
            root.allocateNew();
            IntVector dataVector = (IntVector) root.getVector("data");
            dataVector.allocateNew();
            dataVector.set(0, 0);
            dataVector.set(1, 1);
            dataVector.set(2, 2);
            root.setRowCount(3);

            // Perform the exchange
            try (FlightClient.ExchangeReaderWriter exchange = client.doExchange(descriptor)) {
              // Read and process the response from the server
                exchange.getWriter().start(root);
                exchange.getWriter().putNext();
                exchange.getWriter().completed();

                FlightStream reader = exchange.getReader();
                VectorSchemaRoot responseRoot = reader.getRoot();
                reader.next();
                IntVector responseDataVector = (IntVector) responseRoot.getVector("data");
                assertEquals(3, responseRoot.getRowCount());
                assertEquals(0, responseDataVector.get(0)); // Update these values based on the expected response
                assertEquals(2, responseDataVector.get(1));
                assertEquals(4, responseDataVector.get(2));
            }
        }
    }
}





