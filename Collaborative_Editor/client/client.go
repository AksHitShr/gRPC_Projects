package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"

	document "env/protofiles/doc"
	"google.golang.org/grpc"
	websocket "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var conn_status = "CONNECTED"

type client struct {
	id     string
	conn   *websocket.Conn
	stream document.DocumentService_StreamDocumentClient
	grpcClient  document.DocumentServiceClient
	mu     sync.Mutex
	text   string
}

func (c *client) getFullDocument() error {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	response, err := c.grpcClient.GetFullDocument(ctx, &document.Empty{})
	if err != nil {
		return fmt.Errorf("failed to get existing full document from server! : %v", err)
	}

	c.mu.Lock()
	c.text = response.FullText
	c.mu.Unlock()

	if err := c.conn.WriteMessage(websocket.TextMessage, []byte(response.FullText)); err != nil {
		return fmt.Errorf("WebSocket write error: %v", err)
	}

	log.Println("Retrieved and updated full document!")
	return nil
}


func (c *client) readWebSocket() {
	defer c.conn.Close()

	for {
		_, message, err := c.conn.ReadMessage()
		if err != nil {
			log.Println("WebSocket read error:", err)
			return
		}

		c.mu.Lock()
		oldText := c.text
		newText := string(message)
		position, changeType, change := diffTexts(oldText, newText)
		c.text = newText
		c.mu.Unlock()

		update := &document.DocumentUpdate{
			ClientId: c.id,
			Position: int32(position),
			Change:   change,
			Changetype: changeType,
		}

		if err := c.stream.Send(update); err != nil {
			log.Println("Error sending update to server:", err)
			return
		}

		fmt.Printf("Sent update to server: %+v\n", update)
	}
}

func (c *client) readGRPC() {
	log.Println(c.text)
	for {
		update, err := c.stream.Recv()
		if err != nil {
			conn_status="DISCONNECTED"
			if err := c.conn.WriteMessage(websocket.TextMessage, []byte(fmt.Sprintf("status:%s", conn_status))); err != nil {
				log.Println("WebSocket write error:", err)
				return
			}
			log.Println("Error receiving update from server:", err)
			return
		}

		fmt.Printf("Received update from server: %+v\n", update)

		c.mu.Lock()
		position := int(update.Position)
		change := update.Change
		change_len := len(change)
		changeType := update.Changetype

		if changeType == "add" {
			c.text = c.text[:position] + change + c.text[position:]
		} else if changeType == "delete" {
			c.text=c.text[:position]+c.text[position+change_len:]
		}
		c.mu.Unlock()

		if err := c.conn.WriteMessage(websocket.TextMessage, []byte(c.text)); err != nil {
			log.Println("WebSocket write error:", err)
			return
		}
	}
}

func findLongestCommonPrefix(s1, s2 string) int {
    minLen := len(s1)
    if len(s2) < minLen {
        minLen = len(s2)
    }
    for i := 0; i < minLen; i++ {
        if s1[i] != s2[i] {
            return i
        }
    }
    return minLen
}

func findLongestCommonSuffix(s1, s2 string, prefixLen int) int {
    i := 1
    maxLen := len(s1) - prefixLen
    if len(s2)-prefixLen < maxLen {
        maxLen = len(s2) - prefixLen
    }
    for i <= maxLen {
        if s1[len(s1)-i] != s2[len(s2)-i] {
            return i - 1
        }
        i++
    }
    return maxLen
}

func diffTexts(oldText, newText string) (int, string, string) {
    prefixLen := findLongestCommonPrefix(oldText, newText)
    suffixLen := findLongestCommonSuffix(oldText, newText, prefixLen)
    if len(oldText) > len(newText) {
        deletedText := oldText[prefixLen : len(oldText)-suffixLen]
        return prefixLen, "delete", deletedText
    } else {
        addedText := newText[prefixLen : len(newText)-suffixLen]
        return prefixLen, "add", addedText
    }
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Please provide a port number")
	}

	port, err := strconv.Atoi(os.Args[1])
	if err != nil {
		log.Fatal("Invalid port number")
	}

	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	
	if err != nil {
		conn_status="DISCONNECTED"
		log.Fatalf("Failed to connect to gRPC server: %v", err)
	}
	defer conn.Close()

	grpcClient := document.NewDocumentServiceClient(conn)
	stream, err := grpcClient.StreamDocument(context.Background())
	if err != nil {
		log.Fatalf("Failed to create stream: %v", err)
	}

	c := &client{
		id:     fmt.Sprintf("client_%d", port),
		stream: stream,
		grpcClient: grpcClient,
	}

	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println("WebSocket error:", err)
			return
		}

		c.conn = conn

		if err := c.conn.WriteMessage(websocket.TextMessage, []byte(fmt.Sprintf("status:%s", conn_status))); err != nil {
			log.Println("WebSocket write error:", err)
			return
		}

		if err := c.getFullDocument(); err != nil {
			log.Println("Error getting full document:", err)
			return
		}

		go c.readWebSocket()
		go c.readGRPC()
	})

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "index.html")
	})

	log.Printf("Starting WebSocket server on :%d\n", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}