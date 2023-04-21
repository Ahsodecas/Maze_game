from bfs import bfs, create_maze_map
import sys, pygame, time
import math
import random

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
GOAl_X = 384
GOAl_Y = 384

pygame.init()
clock = pygame.time.Clock()
# create the screen
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))  # width, height

maze_draft = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


def add_random_wall(coordinates_of_walls: list[(int, int)]):
    """
    Selects random x and y coordinates of blocks of the maze and tries to add a wall there.
    Checks whether adding is possible using bfs function.
    :param coordinates_of_walls: List of coordinates of left upper corner of each wall.
    :return: no
    """
    # random.randrange(start, stop, step)
    row = random.randrange(0, SCREEN_X - RECT_SIZE, RECT_SIZE)
    column = random.randrange(0, SCREEN_Y - RECT_SIZE, RECT_SIZE)
    if (row, column) != (PLAYER_X, PLAYER_Y) and (row, column) != (GOAl_X, GOAl_Y):
        if (row, column) not in coordinates_of_walls:
            coordinates_of_walls.append((row, column))


# smoke test(?)
def maze_generator(maze_map: list[(int, int)], coordinates_of_walls: list[(int, int)]):
    """
    Generates a maze by adding coordinates of walls to coordinates_of_walls, and checking if the maze is doable.
    :param maze_map: List of coordinates of each block of the whole maze
    :param coordinates_of_walls: List of coordinates of left upper corner of each wall.
    :return: no
    """
    while True:
        add_random_wall(coordinates_of_walls)
        if bfs(maze_map, coordinates_of_walls) == -1:
            coordinates_of_walls.pop()
            break


def maze_draw(coordinates_of_walls):
    """
    Draws one black square at the coordinates from coordinates_of_walls with size of sides RECT_SIZE.
    :param coordinates_of_walls: List of coordinates of left upper corner of each wall.
    :return: no
    """
    for coordinate in coordinates_of_walls:
        (x, y) = coordinate
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, RECT_SIZE, RECT_SIZE))


def main():
    maze_map = create_maze_map()  # coordinates of each block of maze
    coordinates_of_walls = []  # coordinates of the walls
    maze_generator(maze_map, coordinates_of_walls)
    print(bfs(maze_map, coordinates_of_walls))
    running = True
    while running:
        clock.tick(60)
        screen.fill((100, 100, 100))
        maze_draw(coordinates_of_walls)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


if __name__ == "__main__":
    main()
