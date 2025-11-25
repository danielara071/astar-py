import math
import heapq
import des
class AStarError(Exception):
    """Custom exception for A* pathfinding errors."""
    pass


def heuristic(a, b):
    """Octile distance heuristic (optimal for diagonal movement)."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)


def get_neighbors(pos, grid):
    x, y = pos
    rows, cols = len(grid), len(grid[0])

    # Cardinal directions (N,S,E,W)
    cardinals = [
        (1, 0, 1), (-1, 0, 1),
        (0, 1, 1), (0, -1, 1)
    ]

    # Diagonal directions
    diagonals = [
        (1, 1, math.sqrt(2)),
        (1, -1, math.sqrt(2)),
        (-1, 1, math.sqrt(2)),
        (-1, -1, math.sqrt(2))
    ]

    # Cardinal moves (easy)
    for dx, dy, cost in cardinals:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
            yield (nx, ny, cost)

    # Diagonal moves (corner-cut checked)
    for dx, dy, cost in diagonals:
        nx, ny = x + dx, y + dy

        # Skip out of bounds
        if not (0 <= nx < rows and 0 <= ny < cols):
            continue

        # Skip if diagonal destination is blocked
        if grid[nx][ny] == 1:
            continue

        # Adjacent cardinal cells required for safe diagonal
        adj1_x, adj1_y = x + dx, y
        adj2_x, adj2_y = x, y + dy

        # If either adjacent side is outside the grid -> treat it as blocked
        if not (0 <= adj1_x < rows and 0 <= adj1_y < cols):
            continue
        if not (0 <= adj2_x < rows and 0 <= adj2_y < cols):
            continue

        # If either adjacent cardinal cell is blocked, do NOT allow the diagonal
        if grid[adj1_x][adj1_y] == 1:
            continue
        if grid[adj2_x][adj2_y] == 1:
            continue

        yield (nx, ny, cost)



def reconstruct_path(came_from, current):
    """Rebuild the path once the goal is found."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def astar(grid, start, goal):
    """
    A* search algorithm with diagonal movement.

    Parameters:
        grid: 2D list (0 = free, 1 = obstacle)
        start: (row, col)
        goal: (row, col)

    Returns:
        List of positions making up the path, or None if unreachable.
    """

    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # --- Error handling ---
    if rows == 0 or cols == 0:
        raise AStarError("Grid is empty.")

    sx, sy = start
    gx, gy = goal

    if not (0 <= sx < rows and 0 <= sy < cols):
        raise AStarError("Start position is outside the grid.")
    if not (0 <= gx < rows and 0 <= gy < cols):
        raise AStarError("Goal position is outside the grid.")

    if grid[sx][sy] == 1:
        raise AStarError("Start position is on an obstacle.")
    if grid[gx][gy] == 1:
        raise AStarError("Goal position is on an obstacle.")

    # --- A* setup ---
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    visited = set()

    # --- Main loop ---
    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for nx, ny, move_cost in get_neighbors(current, grid):
            neighbor = (nx, ny)
            tentative_g = g_score[current] + move_cost

            if neighbor in visited:
                continue

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))



def print_grid(grid, path=[]):
    ROW = len(grid)
    COL = len(grid[0])

    path_set = set(path)

    for r in range(ROW):
        row_str = ""
        for c in range(COL):
            if (r, c) in path_set:   #  (row, col)
                row_str += "[P]"
            elif grid[r][c] == 1:
                row_str += "[X]"
            else:
                row_str += "[ ]"
        print(row_str)
    print("\n")

def find_path(start, dest):
    size = des.size
    obs = des.obstacles
    grid = [[0 for _ in range(size.n)] for _ in range(size.m)]
    for o in obs:
        grid[o[0]][o[1]] = 1
    sol = astar(grid, start, dest)
    return sol

def main():
    #1 is blocked, 0 not blocked

    size = des.size
    obs = des.obstacles
    grid = [[0 for _ in range(size.n)] for _ in range(size.m)]
    for o in obs:
        grid[o[0]][o[1]] = 1
    # print_grid(grid)
    # start and finish
    src = (0,0)
    dest = (10, 10)

    # Run the A* search algorithm
    sol = astar(grid, src, dest)
    print_grid(grid, sol) 
    print(sol)

if __name__ == "__main__":
    main()