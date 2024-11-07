package main

import (
	"log"
	"net"
	"sync"
	"time"
	"context"
	"strconv"

	document "env/protofiles/doc"
	"google.golang.org/grpc"
)

type server struct {
	document.UnimplementedDocumentServiceServer
	mu       sync.Mutex
	clients  map[string]document.DocumentService_StreamDocumentServer
	document string
	logStream document.DocumentService_StreamLogsServer
}

func (s *server) GetFullDocument(ctx context.Context, _ *document.Empty) (*document.FullDocumentResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	log.Printf("Sending full doc to new client/ Reloaded Client. Doc: %s",s.document)
	return &document.FullDocumentResponse{
		FullText: s.document,
	}, nil
}

func (s *server) StreamDocument(stream document.DocumentService_StreamDocumentServer) error {
	clientID := "client_"+ strconv.Itoa(len(s.clients))

	s.mu.Lock()
	s.clients[clientID] = stream
	s.mu.Unlock()

	defer func() {
		s.mu.Lock()
		delete(s.clients, clientID)
		s.mu.Unlock()
	}()

	for {
		update, err := stream.Recv()
		if err != nil {
			return err
		}
		log.Printf("Received update from Client: %s",update.ClientId)
		logMessage := time.Now().Format(time.RFC3339) + " Client: " + update.ClientId + " updated doc - Change: " + update.Change + " Type: " + update.Changetype + " Position: " + strconv.Itoa(int(update.Position))
		s.sendLogMessage(logMessage)

		s.mu.Lock()
		s.applyUpdate(update)
		s.broadcastUpdate(update, clientID)
		s.mu.Unlock()
	}
}

func (s *server) StreamLogs(stream document.DocumentService_StreamLogsServer) error {
	// Register the log stream
	s.mu.Lock()
	s.logStream = stream
	s.mu.Unlock()

	for {
		_, err := stream.Recv()
		if err != nil {
			log.Printf("Logger client disconnected: %v", err)
			return err
		}
	}
}

func (s *server) sendLogMessage(logMessage string) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.logStream != nil {
		logMsg := &document.LogMessage{Logstring: logMessage}
		if err := s.logStream.Send(logMsg); err != nil {
			log.Printf("Error sending log message: %v", err)
		}
	}
}

func (s *server) applyUpdate(update *document.DocumentUpdate) {
    position := int(update.Position)
    change := update.Change
	change_len := len(change)
    changeType := update.Changetype

    if changeType == "add" {
        s.document = s.document[:position] + change + s.document[position:]
    } else if changeType == "delete" {
		s.document=s.document[:position]+ s.document[position+change_len:]
    }
}

func (s *server) broadcastUpdate(update *document.DocumentUpdate, senderID string) {
	log.Println(senderID)
	for clientID, stream := range s.clients {
		if clientID==senderID{
			continue
		}
		if err := stream.Send(update); err != nil {
			log.Printf("Error sending update to client %s: %v", clientID, err)
		}
	}
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	document.RegisterDocumentServiceServer(s, &server{
		clients:  make(map[string]document.DocumentService_StreamDocumentServer),
		document: "",
	})

	log.Println("Server started on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}