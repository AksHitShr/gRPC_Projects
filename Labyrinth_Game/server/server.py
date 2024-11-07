import grpc
from concurrent import futures
import labyrinth_pb2
import labyrinth_pb2_grpc

class LabyrinthGameServicer(labyrinth_pb2_grpc.LabyrinthGameServicer):
    def __init__(self):
        self.labyrinth = self.load_labyrinth("labyrinth.txt")
        self.width = len(self.labyrinth[0])
        self.height = len(self.labyrinth)
        self.player_position = (0, 0)  # Start at top-left corner
        self.player_score = 0
        self.player_health = 3
        self.remaining_spells = 3
        self.print_current_tiles()

    def load_labyrinth(self, file_path):
        # Load the labyrinth from a file
        # 0 = empty, 1 = coin, 2 = wall
        with open(file_path, "r") as f:
            return [list(map(int, line.strip().split())) for line in f]

    def GetLabyrinthInfo(self, request, context):
        print("GetLabyrinthInfo")
        return labyrinth_pb2.LabyrinthInfo(width=self.width, height=self.height)

    def GetPlayerStatus(self, request, context):
        print("GetPlayerStatus")
        return labyrinth_pb2.PlayerStatus(
            score=self.player_score,
            health=self.player_health,
            currentPosition=labyrinth_pb2.Position(x=self.player_position[0], y=self.player_position[1]),
            remainingSpells=self.remaining_spells
        )
    
    def print_current_tiles(self):
        with open("current_labyrinth.txt", "w") as file:
            for lst in self.labyrinth:
                file.write(" ".join(map(str, lst)) + "\n")
            file.write("Row: "+str(self.player_position[1])+ " ," + "Column: " +str(self.player_position[0]) + "\n")


    def RegisterMove(self, request, context):
        print("RegisterMove")
        direction = request.direction
        x, y = self.player_position
        new_position = self.move_player(x, y, direction)
        if new_position == (x, y):
            self.player_health -= 1 # reduce health when going out of bounds
            if self.player_health <= 0:
                return labyrinth_pb2.MoveResponse(status="death")
            print(f"Updated Position (col,row): {self.player_position}")
            return labyrinth_pb2.MoveResponse(status="failure")
        else:
            self.player_position = new_position
            resp = self.handle_move_result(x,y)
            print(f"Updated Position (col,row): {self.player_position}")
            return resp

    def move_player(self, x, y, direction):
        if direction == "up" and y > 0:
            return (x, y - 1)
        elif direction == "down" and y < self.height - 1:
            return (x, y + 1)
        elif direction == "left" and x > 0:
            return (x - 1, y)
        elif direction == "right" and x < self.width - 1:
            return (x + 1, y)
        return (x, y)  # Move failed

    def handle_move_result(self,a,b):
        x, y = self.player_position
        if self.labyrinth[y][x] == 1:  # Coin tile
            self.player_score += 1
            self.labyrinth[y][x] = 0  # Turn into an empty tile
            self.print_current_tiles()
            return labyrinth_pb2.MoveResponse(status="success")
        elif self.labyrinth[y][x] == 2:  # Wall tile
            self.player_health -= 1
            self.player_position=(a,b)
            self.print_current_tiles()
            if self.player_health <= 0:
                return labyrinth_pb2.MoveResponse(status="death")
            return labyrinth_pb2.MoveResponse(status="failure")
        elif self.player_position == (self.width - 1, self.height - 1):  # Bottom-right corner
            self.print_current_tiles()
            return labyrinth_pb2.MoveResponse(status="victory")
        self.print_current_tiles()
        return labyrinth_pb2.MoveResponse(status="success")

    def Revelio(self, request, context):
        print("Revelio")
        if self.remaining_spells==0:
            return
        else:
            self.remaining_spells-=1
        x, y = request.targetPosition.x, request.targetPosition.y
        tile_type = request.tileType
        for i in range(max(0, x - 1), min(self.width, x + 2)):
            for j in range(max(0, y - 1), min(self.height, y + 2)):
                if str(self.labyrinth[j][i]) == tile_type:
                    yield labyrinth_pb2.Position(x=i, y=j)

    def Bombarda(self, request_iterator, context):
        print("Bombarda")
        if self.remaining_spells==0:
            return
        else:
            self.remaining_spells-=1
        for target_position in request_iterator:
            x, y = target_position.x, target_position.y
            self.labyrinth[y][x] = 0  # making tile empty
        self.print_current_tiles()
        return labyrinth_pb2.EmptyResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    labyrinth_pb2_grpc.add_LabyrinthGameServicer_to_server(LabyrinthGameServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server Started!")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
