#!/bin/bash

# Install required packages
pip install grpcio grpcio-tools

# Generate Python code from proto file
python -m grpc_tools.protoc -I./protofiles --python_out=./client --grpc_python_out=./client ./protofiles/labyrinth.proto
python -m grpc_tools.protoc -I./protofiles --python_out=./server --grpc_python_out=./server ./protofiles/labyrinth.proto

echo "Build completed successfully!"