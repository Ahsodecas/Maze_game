from bfs import bfs, create_empty_maze
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


def add_random_wall(coordinates):
    # random.randrange(start, stop, step)
    row = random.randrange(0, SCREEN_X - RECT_SIZE, RECT_SIZE)
    column = random.randrange(0, SCREEN_Y - RECT_SIZE, RECT_SIZE)
    if (row, column) != (PLAYER_X, PLAYER_Y) and (row, column) != (GOAl_X, GOAl_Y):
        if (row, column) not in coordinates:
            coordinates.append((row, column))


def maze_generator(coordinates_of_maze, coordinates):
    while True:
        add_random_wall(coordinates)
        if bfs(coordinates_of_maze, coordinates) == -1:
            coordinates.pop()
            break


def maze_draw(coordinates):
    for coordinate in coordinates:
        (x, y) = coordinate
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, RECT_SIZE, RECT_SIZE))


def main():
    coordinates_of_maze = create_empty_maze()  # coordinates of each block of maze
    coordinates = []  # coordinates of the walls
    maze_generator(coordinates_of_maze, coordinates)
    print(bfs(coordinates_of_maze, coordinates))
    running = True
    while running:
        clock.tick(60)
        screen.fill((100, 100, 100))
        maze_draw(coordinates)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


if __name__ == "__main__":
    main()
