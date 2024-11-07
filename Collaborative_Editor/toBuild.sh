#!/bin/bash

# Install required packages
go get google.golang.org/protobuf/cmd/protoc-gen-go
go get google.golang.org/grpc
go get "github.com/gorilla/websocket"

# Update PATH
export PATH="$PATH:$(go env GOPATH)/bin"

source ~/.zshrc

# Generate Go code from proto file
protoc --go_out=. --go-grpc_out=. protofiles/document.proto

echo "Build completed successfully!"