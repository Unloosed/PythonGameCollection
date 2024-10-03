import pygame
import heapq
import os

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Path to resource directory
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "a_star_maze")

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Grid settings
GRID_ROWS, GRID_COLS = 20, 20
CELL_WIDTH = SCREEN_WIDTH // GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT // GRID_ROWS

class GridNode:
    """Class representing a node in the grid for the A* algorithm."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g_cost = float('inf')  # Cost from start to this node
        self.h_cost = 0  # Heuristic cost from this node to end
        self.f_cost = float('inf')  # Total cost (g_cost + h_cost)
        self.neighbors = []
        self.previous = None
        self.is_wall = False

    def add_neighbors(self, grid):
        """Add neighboring nodes to the node's neighbors list."""
        self.neighbors = []
        if self.row < GRID_ROWS - 1:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < GRID_COLS - 1:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1])

    def reset(self):
        """Reset node attributes for a new pathfinding run."""
        self.g_cost = float('inf')
        self.h_cost = 0
        self.f_cost = float('inf')
        self.previous = None

    def __lt__(self, other):
        """Less than comparison based on f_cost for priority queue."""
        return self.f_cost < other.f_cost

def heuristic(node_a, node_b):
    """Heuristic function for A* (Manhattan distance)."""
    return abs(node_a.row - node_b.row) + abs(node_a.col - node_b.col)

def a_star_search(grid, start_node, end_node):
    """A* search algorithm to find the shortest path from start_node to end_node."""
    for row in grid:
        for node in row:
            node.reset()
            node.add_neighbors(grid)

    open_set = []
    heapq.heappush(open_set, (0, start_node))
    start_node.g_cost = 0
    start_node.f_cost = heuristic(start_node, end_node)

    while open_set:
        current_node = heapq.heappop(open_set)[1]

        if current_node == end_node:
            path = []
            while current_node.previous:
                path.append(current_node)
                current_node = current_node.previous
            path.append(start_node)  # Include the start node in the path
            return path

        for neighbor in current_node.neighbors:
            if not neighbor.is_wall:
                tentative_g_cost = current_node.g_cost + 1

                if tentative_g_cost < neighbor.g_cost:
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = heuristic(neighbor, end_node)
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.previous = current_node
                    heapq.heappush(open_set, (neighbor.f_cost, neighbor))

    return []

def draw_grid(window, grid, path, star_image):
    """Draw the grid on the window."""
    for row in grid:
        for node in row:
            color = COLOR_WHITE
            if node.is_wall:
                color = COLOR_BLACK
            pygame.draw.rect(window, color, (node.col * CELL_WIDTH, node.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            pygame.draw.rect(window, COLOR_BLACK, (node.col * CELL_WIDTH, node.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
            if node in path:
                window.blit(star_image, (node.col * CELL_WIDTH, node.row * CELL_HEIGHT))

def handle_mouse_click(grid):
    """Handle mouse click events to place or remove walls."""
    pos = pygame.mouse.get_pos()
    row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            grid[row][col].is_wall = True
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button
            grid[row][col].is_wall = False

def draw_path_length(window, path_length):
    """Draw the path length on the window."""
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Path Length: {path_length}", True, COLOR_BLACK)
    window.blit(text, (10, 10))

def reset_walls(grid):
    """Reset all walls in the grid."""
    for row in grid:
        for node in row:
            node.is_wall = False

def start_a_star_maze():
    """Main function to run the game."""
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("A* Pathfinding Game")

    # Load and scale the star image
    star_image = pygame.image.load(os.path.join(RESOURCE_DIR, "star.png"))
    star_image = pygame.transform.scale(star_image, (CELL_WIDTH, CELL_HEIGHT))

    grid = [[GridNode(row, col) for col in range(GRID_COLS)] for row in range(GRID_ROWS)]
    for row in grid:
        for node in row:
            node.add_neighbors(grid)

    start_node = grid[0][0]
    end_node = grid[GRID_ROWS - 1][GRID_COLS - 1]
    start_node.is_wall = False
    end_node.is_wall = False

    path = []
    path_length = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path = a_star_search(grid, start_node, end_node)
                    path_length = len(path) if path else 0
                if event.key == pygame.K_r:
                    reset_walls(grid)
                    path = []
                    path_length = 0

        handle_mouse_click(grid)

        window.fill(COLOR_WHITE)
        draw_grid(window, grid, path, star_image)
        draw_path_length(window, path_length)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    start_a_star_maze()
