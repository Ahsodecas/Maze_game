from queue import Queue

RECT_SIZE = 64
PLAYER_SIZE = 64
SPEED = 3
BLOCKS = 8  # number of blocks on one size of the maze
SCREEN_X = 512
SCREEN_Y = 512
PLAYER_X = 64
PLAYER_Y = 64
PLAYER_R = 1
PLAYER_C = 1
GOAL_X = 384
GOAL_Y = 384


maze_draft = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]


def create_maze_map() -> list[list[(int, int)]]:
    """
    Creates list of lists of coordinates of left upper corner of each block of the maze.
    The maze consists of BLOCKS number of blocks.
    :return: List of lists of coordinates of left upper corner of each block of the maze.
    """
    maze_coords = [[] for _ in range(BLOCKS)]
    cor_x = 0
    cor_y = 0
    for rows in range(BLOCKS):
        for _ in range(BLOCKS):
            maze_coords[rows].append((cor_x, cor_y))
            # maze_coords[rows] += [(cor_x, cor_y)]
            cor_x += RECT_SIZE
        cor_y += RECT_SIZE
        cor_x = 0
    return maze_coords


def create_maze_from_draft(maze_draft: list[list[int]]) -> list[(int, int)]:
    """
    :param maze_draft: the list of 0's and 1's which represent road and walls, respectively.
    For each value 1, stores in the list maze_coordinates the appropriate coordinates of left upper corner of each wall.
    :return: List of coordinates of left upper corner of each wall.
    """
    maze_coordinates = []
    cor_x = 0
    cor_y = 0
    for rows in range(0, BLOCKS):
        for columns in range(0, BLOCKS):
            if maze_draft[rows][columns] == 1:
                maze_coordinates.append((cor_x, cor_y))
            cor_x += RECT_SIZE
        cor_y += RECT_SIZE
        cor_x = 0
    return maze_coordinates


def bfs(maze_map: list[(int, int)], coordinates_of_walls: list[(int, int)]) -> int:
    """
    Checks whether the current maze is doable using bfs algorithm.
    :param maze_map: List of coordinates of each block of the whole maze
    :param coordinates_of_walls: List of coordinates of left upper corner of each wall.
    :return: int dist - the minimum number of steps to reach the goal,
    -1 in case the maze is not doable
    """

    q = Queue()
    visited = set()
    node_r, node_c = PLAYER_R, PLAYER_C  # row and column of the first element element
    q.put((maze_map[node_r][node_c], node_r, node_c, 0))

    while not q.empty():
        temp = q.get()
        (elem, r, c, dist) = temp
        if elem in visited:
            continue
        visited.add(elem)
        if elem == (GOAL_X, GOAL_Y):
            return dist
        nexts = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for (dr, dc) in nexts:
            newr = r + dr
            newc = c + dc
            if 0 <= newc < BLOCKS and 0 <= newr < BLOCKS and maze_map[newr][newc] not in visited and maze_map[newr][newc] not in coordinates_of_walls:
                q.put((maze_map[newr][newc], newr, newc, dist+1))
    return -1


def main():
    maze_map = create_maze_map()  # coordinates of each block of the maze
    coordinates_of_walls = create_maze_from_draft(maze_draft)  # coordinates of walls of the maze
    path = bfs(maze_map, coordinates_of_walls)
    print(path)


if __name__ == "__main__":
    main()

