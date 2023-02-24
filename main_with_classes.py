import sys, pygame, time
import math

pygame.init()
clock = pygame.time.Clock()
RECT_SIZE = 64
PLAYER_SIZE = 64
speed = 3
# create the screen
screen_x = 512
screen_y = 512
screen = pygame.display.set_mode((screen_x, screen_y))  # width, height
# title
pygame.display.set_caption("Game")
# icon
icon = pygame.image.load("open-book.png")
icon.convert()
pygame.display.set_icon(icon)
# library = destination
goalIm = pygame.image.load("library.png")
goalIm.convert()
goal_x = 384
goal_y = 384
# game over text
game_over = pygame.font.Font('freesansbold.ttf', 32)
# maze
maze_draft = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 1],
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


class Player:

    def __init__(self, image, coordinates):
        self.player_image = pygame.image.load(image)
        self.player_image.convert()
        self.player_coords = coordinates

    # move is difference between old and new coordinates
    def move_player(self, _move):
        self.player_coords += _move
        screen.blit(self.player_image, (self.player_coords.x, self.player_coords.y))


class Maze:

    def __init__(self, goal_coords, maze_draft, player_to_maze):
        # change scree color
        screen.fill((100, 100, 100))
        self.maze_draft = maze_draft
        self.goal_coords = goal_coords
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
            if (x < player_coordinates.x < x + RECT_SIZE) and (y < player_coordinates.y - 1 < y + RECT_SIZE):
                return False
        # boundaries of the screen
        if player_coordinates.x < 0:
            return False
        if player_coordinates.x > (screen_x - PLAYER_SIZE):
            return False
        if player_coordinates.y < 0:
            return False
        if player_coordinates.y > (screen_y - PLAYER_SIZE):
            return False
        return True


def move_type(event):
    coords_change = Coords(0, 0)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            coords_change.x = speed
        if event.key == pygame.K_LEFT:
            coords_change.x = -speed
        if event.key == pygame.K_UP:
            coords_change.y = -speed
        if event.key == pygame.K_DOWN:
            coords_change.y = speed
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            coords_change.x = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            coords_change.y = 0
    return coords_change


def game_over_text():
    text = game_over.render("Game over", True, (255, 255, 255))
    screen.blit(text, (170, 220))


# game loop
running = True
# create a player
player_initial_coordinates = Coords(RECT_SIZE, RECT_SIZE)
player = Player("sunflower_big.png", player_initial_coordinates)
while running:
    clock.tick(60)
    goal_coords = Coords(goal_x, goal_y)
    player_start_coords = Coords(RECT_SIZE, RECT_SIZE)
    maze = Maze(goal_coords, maze_draft, player)
    move = Coords(0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check the type of keys pressed
        move = move_type(event)
    # check if the move is valid
    if maze.is_valid_move(maze.player.player_coords + move):
        maze.player.move_player(move)
    # check if the goal is reached
    if maze.is_goal_collision():
        screen.fill((100, 100, 100))
        game_over_text()
    pygame.display.update()
