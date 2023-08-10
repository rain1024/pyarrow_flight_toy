# Getting Started with Arrow Flight

Introduction to Apache Arrow Flight
Apache Arrow Flight is a framework for high-performance data services. It's part of the Apache Arrow project, which provides a standardized, language-independent columnar memory format optimized for analytics. Arrow Flight builds on this foundation to enable efficient over-the-network data transfer, making it a powerful tool for building data servers and clients that can communicate with minimal overhead.

**Key Features**

1. Efficient Data Transfer: Arrow Flight uses Apache Arrow's columnar format to enable fast, efficient data serialization and deserialization. This reduces the overhead typically associated with data transfer, especially for large datasets.
2. gRPC-Based Communication: Arrow Flight relies on gRPC, a high-performance, open-source, and universal remote procedure call (RPC) framework. This allows for robust, scalable communication between Flight servers and clients.
3. Language Agnostic: Since Apache Arrow provides libraries for various programming languages (including C++, Java, Python, and more), Arrow Flight can be used to build servers and clients in different languages that can communicate seamlessly.
4. Custom Actions: Arrow Flight allows the definition of custom actions that clients can call on the server. This provides a flexible way to implement specific functionality tailored to your application's needs.
5. Authentication and Encryption: Arrow Flight supports pluggable authentication and encryption, allowing for secure data transfer and access control.
6. Integration with Popular Tools: Arrow Flight can be used with popular data processing and analytics tools, making it easier to build end-to-end data pipelines.

## Usage

```
mvn clean install
mvn compile
mvn exec:java -Dexec.mainClass="com.mycompany.app.ArrowClient"
mvn exec:java -Dexec.mainClass="com.mycompany.app.App"
mvn exec:java -Dexec.mainClass="com.mycompany.app.App2"
```