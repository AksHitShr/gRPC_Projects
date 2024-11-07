## Labyrinth Game

### Assumption: The server can only serve a single client at a time. Once a game is over, restart server to play again.

## Components

### `client/client.py`

This file contains the client-side implementation of the game. It provides a command-line interface for the player to interact with the game. The client communicates with the server using gRPC calls.

Main features:
- Get labyrinth information
- Get player status
- Register player moves
- Cast Revelio spell to reveal specific tile types
- Cast Bombarda spell to destroy walls

### `server/server.py`

This file implements the server-side logic of the game. It handles client requests, manages the game state, and enforces game rules.

Main features:
- Load and manage the labyrinth layout
- Track player position, score, and health
- Process player moves and update game state
- Implement spell effects (Revelio and Bombarda)

### `protofiles/labyrinth.proto`

This file defines the Protocol Buffers messages and gRPC service used for client-server communication.

## Game Assumptions

1. The labyrinth is a 2D grid loaded from a file (`labyrinth.txt`).
2. The player starts at the top-left corner (0, 0).
3. The goal is to reach the bottom-right corner.
4. Tile types:
   - 0: Empty tile
   - 1: Coin tile
   - 2: Wall tile
5. The player has 3 health points and 3 spells at the start.
6. Moving into a wall reduces health by 1.
7. Collecting a coin increases the score by 1.
8. The game ends when the player reaches the goal, runs out of health, or chooses to quit.
9. Trying to move out of bounds reduces a health point and does not change position (assuming a wall boundary surrounding the grid).
10. Assuming exactly 3 tiles are taken as input for casting the Bombarda spell. Same point can be repeated in input (makes no change, once a tile has been converted to an empty tile).

## Implementation Details

1. The server loads the labyrinth layout from a file (`labyrinth.txt`).
2. The client provides a text-based interface for game interactions.
3. Moves are processed on the server, which updates the game state accordingly.
4. The Revelio spell reveals tiles of a specific type in a 3x3 area around the target position.
5. The Bombarda spell destroys (converts to empty) 3 specified tiles.
6. Spells are limited and decrease the player's remaining spell count.
7. The server tracks the player's position, score, health, and remaining spells.
8. Out-of-bounds moves are treated as failures and reduce player health.

## Running the Game

1. Start the server:
   ```
   python server/server.py
   ```

2. Run the client:
   ```
   python client/client.py
   ```

3. Follow the on-screen prompts to play the game.

Note: Ensure that all required dependencies (gRPC, protobuf) are installed before running the game.

