# Real-time Collaborative Document

This project implements a real-time collaborative document editor using gRPC for server-client communication and WebSockets for client-browser interaction.

## Implementation Overview

The system consists of three main components:

1. gRPC Server (Go)
2. gRPC Client (Go)
3. Web Client (HTML/JavaScript)

## Commands to Run
### To run the server:
> go run server.go

### To run the logger:
> go run logger.go

### To run the client:
> go run client.go 'PORT'

### gRPC Server

The server maintains the current state of the document and handles updates from multiple clients. It uses a simple concurrency model with a mutex to ensure thread-safe access to the shared document state.

### gRPC Client

The gRPC client acts as a bridge between the web client and the gRPC server. It maintains WebSocket connections with browsers and translates WebSocket messages to gRPC calls and vice versa.

### Web Client

The web client provides a simple textarea for users to edit the document. It uses WebSocket to communicate changes to the gRPC client.

## Features

- Real-time collaborative editing
- Conflict resolution using a simple last-write-wins approach
- Support for multiple clients
- Logging of all document changes

## Quirks and Limitations

1. **Conflict Resolution**: The current implementation uses a simple last-write-wins approach. This can lead to unexpected results if multiple users edit the same part of the document simultaneously.

2. **Error Handling**: The error handling is basic and may not cover all edge cases, especially network-related issues.

3. **Security**: The current implementation does not include any authentication or authorization mechanisms. All clients have full access to edit the document.

4. **Offline Support**: There is no offline support or local caching. If a client loses connection, they may lose unsaved changes.

5. **Undo/Redo**: The system does not support undo/redo operations. Each change is final and immediately propagated to all clients.

6. **Rich Text**: The editor only supports plain text. There's no support for rich text formatting.

7. **Persistence**: The document is only kept in memory and is not persisted to a database. If the server restarts, all changes are lost.
