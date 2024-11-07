import grpc
from grpc import RpcError
import labyrinth_pb2
import labyrinth_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = labyrinth_pb2_grpc.LabyrinthGameStub(channel)
        print("Note: x ordinate is along the x-axis, y ordinate is along y-axis")
        while True:
            print("Labyrinth Game Options:")
            print("Press '1' to Get Labyrinth Info")
            print("Press '2' to Get Player Status")
            print("Press '3' to Register Move")
            print("Press '4' to Cast Revelio Spell")
            print("Press '5' to Cast Bombarda Spell")
            print("Press '6' to Quit")
            
            choice = input("Enter your choice: ")
            try:
                if choice == '1':
                    labyrinth_info = stub.GetLabyrinthInfo(labyrinth_pb2.EmptyRequest())
                    print(f"Labyrinth Size(width x height): {labyrinth_info.width}x{labyrinth_info.height}")
                elif choice == '2':
                    player_status = stub.GetPlayerStatus(labyrinth_pb2.EmptyRequest())
                    print(f"Player Status: Score = {player_status.score}, Health = {player_status.health}, Position = ({player_status.currentPosition.x}, {player_status.currentPosition.y}), Number of Remaining Spells: {player_status.remainingSpells}")
                elif choice == '3':
                    dir = input("Enter direction (up, down, left, right): ")
                    move_response = stub.RegisterMove(labyrinth_pb2.MoveRequest(direction=dir))
                    print(f"Move Status: {move_response.status}")
                    if move_response.status=='death':
                        print("You are dead! Game Over...")
                        break
                    elif move_response.status=='victory':
                        player_status = stub.GetPlayerStatus(labyrinth_pb2.EmptyRequest())
                        print(f"You Win! Final Score: {player_status.score}")
                        print("Game Over...")
                        break
                elif choice == '4':
                    target_x = int(input("Enter target X position: "))
                    target_y = int(input("Enter target Y position: "))
                    tile_type = input("Enter tile type to reveal ('1' for coin/'2' for wall): ")
                    request = labyrinth_pb2.RevelioRequest(
                        targetPosition=labyrinth_pb2.Position(x=target_x, y=target_y),
                        tileType=tile_type
                    )
                    response_stream = stub.Revelio(request)
                    tot = 0
                    for tile in response_stream:
                        print(f"Tile at ({tile.x}, {tile.y}) is of type {tile_type}\n") 
                        tot+=1
                elif choice == '5':
                    num_positions = 3
                    positions = []
                    for i in range(num_positions):
                        x = int(input(f"Enter X position for point {i}: "))
                        y = int(input(f"Enter Y position for point {i}: "))
                        positions.append((x, y))
                    
                    def generate_positions(target_positions):
                        for position in target_positions:
                            yield labyrinth_pb2.Position(x=position[0], y=position[1])

                    stub.Bombarda(generate_positions(positions))
                    print(f"Bombarda Spell Cast!\n")
                elif choice == '6':
                    print("Exiting game...")
                    break
                else:
                    print("Invalid choice! Please try again.")
                print()
                print()
            except RpcError:
                print("Server Error!")
                break

if __name__ == "__main__":
    run()
