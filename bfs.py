from queue import Queue

RECT_SIZE = 64
PLAYER_SIZE = 64
SPEED = 3
SCREEN_X = 512
SCREEN_Y = 512
GOAl_X = 384
GOAl_Y = 384

# maze_draft = [
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0]
# ]
maze_draft = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]


def create_empty_maze():
    maze_coords = [[] for _ in range(8)]
    cor_x = 0
    cor_y = 0
    new_arr = []
    for rows in range(0, 8):
        for columns in range(0, 8):
            # maze_coords[rows][columns] = (cor_x, cor_y)
            new_arr.append((cor_x, cor_y))
            cor_x += RECT_SIZE
        maze_coords[rows] = new_arr.copy()
        new_arr.clear()
        cor_y += RECT_SIZE
        cor_x = 0
    return maze_coords

def create_maze_from_draft(_maze_draft):
    maze_coordinates = []
    cor_x = 0
    cor_y = 0
    for rows in range(0, 8):
        for columns in range(0, 8):
            if _maze_draft[rows][columns] == 1:
                maze_coordinates.append((cor_x, cor_y))
            cor_x += RECT_SIZE
        cor_y += RECT_SIZE
        cor_x = 0
    return maze_coordinates


def bfs(coords, maze):
    min_way = 0  # minimum number of steps to reach the goal
    q = Queue()
    visited = []
    doable = False
    node_r, node_c = 1, 1  # row and column of the first element element
    q.put(coords[node_r][node_c])
    while True:
        elem = q.get()
        visited.append(elem)
        if elem == (GOAl_X, GOAl_Y):
            doable = True
            return doable, min_way
        for r in range(0, 8):  # find row and column of the current element taken from the queue
            for c in range(0, 8):
                if elem == coords[r][c]:
                    node_r = r
                    node_c = c
        if 0 <= node_r - 1 < 8 and coords[node_r - 1][node_c] not in visited and coords[node_r - 1][node_c] not in maze:
            q.put(coords[node_r - 1][node_c])
        if 0 <= node_r + 1 < 8 and coords[node_r + 1][node_c] not in visited and coords[node_r + 1][node_c] not in maze:
            q.put(coords[node_r + 1][node_c])
        if 0 <= node_c - 1 < 8 and coords[node_r][node_c - 1] not in visited and coords[node_r][node_c - 1] not in maze:
            q.put(coords[node_r][node_c - 1])
        if 0 <= node_c + 1 < 8 and coords[node_r][node_c + 1] not in visited and coords[node_r][node_c + 1] not in maze:
            q.put(coords[node_r][node_c + 1])
        if q.empty():
            min_way = -1
            return doable, min_way
        min_way += 1


coordinates = create_empty_maze()  # coordinates of each block of the maze
maze = create_maze_from_draft(maze_draft)  # coordinates of walls of the maze
result, path = bfs(coordinates, maze)
print(result)
print(path)
