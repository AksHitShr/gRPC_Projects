
## Distributed KNN using gRPC

## Components

### 1. Client (`client/client.py`)

The client script is responsible for:
- Connecting to multiple KNN servers
- Sending query requests to each server
- Aggregating results from all servers
- Determining the global k-nearest neighbors

Key features:
- Parallel querying of servers using threads
- Aggregation of results using a max-heap for efficiency
- Thread-safe operations using a mutex lock

### 2. Server (`server/server.py`)

The server script:
- Loads a subset of the dataset from a CSV file
- Implements the KNN service defined in the proto file
- Computes k-nearest neighbors for incoming queries

Key features:
- Configurable port and dataset file via command-line arguments
- Euclidean distance calculation for KNN

### 3. Dataset (`dataset/subset1.csv`, `dataset/subset2.csv`)

- partition.py: File to divide a dataset.csv file (each line is a point in n-dimensional space) into required number of subset.csv files.

- CSV files will be created as subsets of the complete dataset. Each server loads one of these subsets (passed as command line argument when running server).

### 4. Proto file (`protofiles/knn.proto`)

Defines the gRPC service and message types for client-server communication.

## Implementation Details

1. **Distributed Computing**: The system distributes the dataset across multiple servers, allowing for parallel processing of KNN queries.

2. **gRPC Communication**: Client-server communication is implemented using gRPC, providing efficient serialization and deserialization of messages.

3. **Parallel Querying**: The client queries all servers concurrently using threads, improving overall query performance.

4. **Result Aggregation**: The client uses a max-heap to efficiently aggregate results from all servers and determine the global k-nearest neighbors.

5. **Configurable Servers**: Servers can be started with different ports and dataset files, allowing for flexible deployment.

## Assumptions and Limitations

1. **Data Format**: The dataset is assumed to be in CSV format with comma-separated float values.

2. **Fixed Dimensionality**: The system assumes that all data points (including the query point) have the same number of dimensions.

3. **Euclidean Distance**: The current implementation uses Euclidean distance for KNN calculations. Other distance metrics would require modifications.

4. **Insecure Communication**: The current setup uses insecure gRPC channels. For production use, secure channels should be implemented.

5. **In-Memory Processing**: The entire dataset subset is loaded into memory on each server.

6. **No Data Updates**: The current implementation doesn't support dynamic updates to the dataset. Restarting the server is required to load new data.

## Usage

1. Divide dataset.csv file into multiple subset files, one per server:
   ```
   python partition.py dataset.csv <x>
   ```

2. Start multiple server instances, each with a different port and dataset file:
   ```
   python server/server.py 50051 dataset/subset1.csv
   python server/server.py 50052 dataset/subset2.csv
   ```

3. Run the client script to query the servers:
   ```
   python client/client.py
   ```