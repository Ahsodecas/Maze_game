import sys, pygame, time
import math
from bfs import bfs, create_empty_maze
from generator import maze_generator

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
GENERATE_MAZE = True
ICON_IMAGE = "open-book.png"
GOAL_IMAGE = "library.png"
PLAYER_IMAGE = "sunflower_big.png"
TITLE = "Game"

pygame.init()
clock = pygame.time.Clock()
# create the screen
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))  # width, height
# title
pygame.display.set_caption(TITLE)
# icon
icon = pygame.image.load(ICON_IMAGE)
icon.convert()
pygame.display.set_icon(icon)
# library = destination
goalIm = pygame.image.load(GOAL_IMAGE)
goalIm.convert()
# game over text
game_over = pygame.font.Font('freesansbold.ttf', 32)
# maze
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


class Coords:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # This is operator overloading - if you define __add__ or __str___ or __gt__ for a custom class,
    # you will be able to add, print or use > on your class instances
    # It tells the interpreter than "when you see me doing Coords + Coords I mean to use this function".
    def __add__(self, other_coords):
        return Coords(self.x + other_coords.x, self.y + other_coords.y)

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)


class Player:

    def __init__(self, image, coordinates):
        self.player_image = pygame.image.load(image)
        self.player_image.convert()
        self.player_coords = coordinates

    # move is difference between old and new coordinates
    def move_player(self, move):
        self.player_coords += move

    def redraw_player(self):
        screen.blit(self.player_image, (self.player_coords.x, self.player_coords.y))


class Maze:

    def __init__(self, goal_coords, maze_draft, player_to_maze):
        # change scree color
        screen.fill((100, 100, 100))
        self.maze_draft = maze_draft
        self.goal_coords = goal_coords
        if GENERATE_MAZE == True:
            coordinates = []
            maze_generator(create_empty_maze(), coordinates)
            self.maze_coords = coordinates
        else:
            self.maze_coords = self.create_maze_from_draft()
        self.maze_draw()
        self.goal_draw()
        # self.player = Player(player_image, player_start_coords)
        self.player = player_to_maze

    # coordinates of top left corner of each rectangle
    def create_maze_from_draft(self):
        maze_coordinates = []
        cor_x = 0
        cor_y = 0
        for rows in range(0, 8):
            for columns in range(0, 8):
                if self.maze_draft[rows][columns] == 1:
                    maze_coordinates.append((cor_x, cor_y))
                cor_x += RECT_SIZE
            cor_y += RECT_SIZE
            cor_x = 0
        return maze_coordinates

    def maze_draw(self):
        for coordinates in self.maze_coords:
            (x, y) = coordinates
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, RECT_SIZE, RECT_SIZE))

    def goal_draw(self):
        screen.blit(goalIm, (self.goal_coords.x, self.goal_coords.y))

    def is_goal_collision(self):
        # distance between objects:
        distance = math.sqrt(math.pow(self.player.player_coords.x - self.goal_coords.x, 2) + math.pow(self.player.player_coords.y - self.goal_coords.y, 2))
        if distance <= 20:
            return True
        else:
            return False

    def is_valid_move(self, player_coordinates):
        # is_wall_collision
        for coordinates in self.maze_coords:
            (x, y) = coordinates
            if (x < player_coordinates.x < x + RECT_SIZE) and (y < player_coordinates.y < y + RECT_SIZE):
                return False
            if (x < player_coordinates.x + PLAYER_SIZE - 1 < x + RECT_SIZE) and (y < player_coordinates.y < y + RECT_SIZE):
                return False
            if (x < player_coordinates.x + PLAYER_SIZE - 1 < x + RECT_SIZE) and (y < player_coordinates.y + PLAYER_SIZE - 1 < y + RECT_SIZE):
                return False
            if (x < player_coordinates.x < x + RECT_SIZE) and (y < player_coordinates.y + PLAYER_SIZE - 1 < y + RECT_SIZE):
                return False
        # boundaries of the screen
        if player_coordinates.x < 0:
            return False
        if player_coordinates.x > (SCREEN_X - PLAYER_SIZE):
            return False
        if player_coordinates.y < 0:
            return False
        if player_coordinates.y > (SCREEN_Y - PLAYER_SIZE):
            return False
        return True


def move_type(prev_move, event):
    coords_change = Coords(0, 0)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            coords_change.x = SPEED
        if event.key == pygame.K_LEFT:
            coords_change.x = -SPEED
        if event.key == pygame.K_UP:
            coords_change.y = -SPEED
        if event.key == pygame.K_DOWN:
            coords_change.y = SPEED
        return coords_change
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            coords_change.x = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            coords_change.y = 0
        return coords_change
    return prev_move


def game_over_text():
    text = game_over.render("Game over", True, (255, 255, 255))
    screen.blit(text, (170, 220))


def main():
    # game loop
    running = True
    move = Coords(0, 0)
    # create a player
    player_initial_coordinates = Coords(RECT_SIZE, RECT_SIZE)
    player = Player(PLAYER_IMAGE, player_initial_coordinates)
    goal_coords = Coords(GOAl_X, GOAl_Y)
    maze = Maze(goal_coords, maze_draft, player)
    while running:
        clock.tick(60)
        screen.fill((100, 100, 100))
        maze.maze_draw()
        maze.goal_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check the type of keys pressed
            move = move_type(move, event)
        # check if the move is valid
        if maze.is_valid_move(maze.player.player_coords + move):
            maze.player.move_player(move)
        maze.player.redraw_player()
        # check if the goal is reached
        if maze.is_goal_collision():
            screen.fill((100, 100, 100))
            game_over_text()
        pygame.display.update()


        
if __name__ == "__main__":
    main()
