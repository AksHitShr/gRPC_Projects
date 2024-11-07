package main

import (
	"context"
	"log"
	"os"

	"google.golang.org/grpc"

	document "env/protofiles/doc" // Adjust the import path as needed
)

func main() {
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Did not connect: %v", err)
	}
	defer conn.Close()

	c := document.NewDocumentServiceClient(conn)

	// Create or open the log file
	logFile, err := os.OpenFile("logs.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatalf("Could not open log file: %v", err)
	}
	defer logFile.Close()

	// Stream logs from the server
	stream, err := c.StreamLogs(context.Background())
	if err != nil {
		log.Fatalf("Could not stream logs: %v", err)
	}

	// Receive log messages in a separate goroutine
	go func() {
		for {
			msg, err := stream.Recv()
			if err != nil {
				log.Fatalf("Error receiving log message: %v", err)
			}

			// Append the received message to the log file
			if _, err := logFile.WriteString(msg.GetLogstring() + "\n"); err != nil {
				log.Fatalf("Could not write to log file: %v", err)
			}

			log.Printf("Appended log message: %s", msg.GetLogstring())
		}
	}()

	// Prevent the main function from exiting
	select {}
}
