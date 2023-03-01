from queue import Queue

RECT_SIZE = 64
PLAYER_SIZE = 64
SPEED = 3
SCREEN_X = 512
SCREEN_Y = 512
GOAL_X = 384
GOAL_Y = 384

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
    # new_arr = []
    for rows in range(8):
        for _ in range(8):
            # maze_coords[rows][columns] = (cor_x, cor_y)
            # new_arr.append((cor_x, cor_y))
            maze_coords[rows].append((cor_x, cor_y))
            # maze_coords[rows] += [(cor_x, cor_y)]
            cor_x += RECT_SIZE
        # maze_coords[rows] = new_arr.copy()
        # new_arr.clear()
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
    # min_way = 0  # minimum number of steps to reach the goal
    q = Queue()
    # visited = []
    visited = set()
    # doable = False
    node_r, node_c = 1, 1  # row and column of the first element element
    q.put((coords[node_r][node_c], node_r, node_c, 0))

    while not q.empty():
        temp = q.get()
        (elem, r, c, dist) = temp
        # visited.append(elem)
        if elem in visited:
            continue
        visited.add(elem)
        if elem == (GOAL_X, GOAL_Y):
            # doable = True
            # return doable, dist
            return dist
        # for r in range(0, 8):  # find row and column of the current element taken from the queue
        #     for c in range(0, 8):
        #         if elem == coords[r][c]:
        #             node_r = r
        #             node_c = c
        # if 0 <= r - 1 < 8 and coords[r - 1][c] not in visited and coords[r - 1][c] not in maze:
        #     q.put(coords[r - 1][c])
        # if 0 <= r + 1 < 8 and coords[r + 1][c] not in visited and coords[r + 1][c] not in maze:
        #     q.put(coords[r + 1][c])
        # if 0 <= c - 1 < 8 and coords[r][c - 1] not in visited and coords[r][c - 1] not in maze:
        #     q.put(coords[r][c - 1])
        # if 0 <= c + 1 < 8 and coords[r][c + 1] not in visited and coords[r][c + 1] not in maze:
        #     q.put(coords[r][c + 1])

        nexts = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for (dr, dc) in nexts:
            newr = r + dr
            newc = c + dc
            if 0 <= newc < 8 and 0 <= newr < 8 and coords[newr][newc] not in visited and coords[newr][newc] not in maze:
                q.put((coords[newr][newc], newr, newc, dist+1))

        # if q.empty():
            # min_way = -1
            # return doable, min_way
            # return -1
        # min_way += 1

    return -1

def main():
    coordinates = create_empty_maze()  # coordinates of each block of the maze
    maze = create_maze_from_draft(maze_draft)  # coordinates of walls of the maze
    # result, path = bfs(coordinates, maze)
    path = bfs(coordinates, maze)
    # print(result)
    print(path)

if __name__ == "__main__":
    main()
