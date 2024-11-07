## gRPC based Projcts

### Please refer to Readme's inside the folders for more information about running the files.

### Collaborative Editor: Implemented a eal-time collaborative document editor in Go, accessible via a web browser and utilizing WebSockets for seamless communication. The editor uses gRPC to relay live changes from any client to the server, which in turn synchronizes updates across all connected clients, ensuring real-time consistency.

### Labyrinth Game: Created a Labyrinth game with gRPC, enabling player moves and game status updates between the server and clients. The server maintains the game status of each player, makes their moves (that it receives) and sends back its outcome.

### Distributed KNN Algorithm: Distributed the samples/points dataset equally across multiple servers. Each client sends its query sample/point to each of the servers for local KNN calculation. Then, each server returns its local K-Nearest Neighbours and the global KNN is found by client after receiving all local nearest neighbours. gRPC is used for client-server communication.
