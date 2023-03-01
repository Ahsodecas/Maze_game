import sys, pygame, time
import math

pygame.init()
clock = pygame.time.Clock()
RECT_SIZE = 64
PLAYER_SIZE = 64
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
# player
playerIm = pygame.image.load("sunflower_big.png")
playerIm.convert()
player_coordinates = player_x, player_y = (RECT_SIZE, RECT_SIZE)
# change in player's position when a key is pressed
x_change = 0
y_change = 0
# library = destination
goalIm = pygame.image.load("library.png")
goalIm.convert()
goal_x = 384
goal_y = 384
# game over text
game_over = pygame.font.Font('freesansbold.ttf', 32)
# maze
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
# coordinates of top left corner of each rectangle
maze_coordinates = []
cor_x = 0
cor_y = 0
for rows in range(0, 8):
    for columns in range(0, 8):
        if maze[rows][columns] == 1:
            maze_coordinates.append((cor_x, cor_y))
        cor_x += RECT_SIZE
    cor_y += RECT_SIZE
    cor_x = 0


def maze_draw():
    for coordinates in maze_coordinates:
        (x, y) = coordinates
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, RECT_SIZE, RECT_SIZE))


def move_player(x, y):
    # blit = draw
    screen.blit(playerIm, (x, y))


def goal(x, y):
    screen.blit(goalIm, (x, y))


def is_goal_collision(playerx, playery, objectx, objecty):
    # distance between objects:
    distance = math.sqrt(math.pow(playerx - objectx, 2) + math.pow(playery - objecty, 2))
    if distance <= 30:
        return True
    else:
        return False


def is_wall_collision(playerx, playery):
    for coordinates in maze_coordinates:
        (x, y) = coordinates
        if (x < playerx < x + RECT_SIZE) and (y < playery < y + RECT_SIZE):
            return True
        if (x < playerx + PLAYER_SIZE - 1 < x + RECT_SIZE) and (y < playery < y + RECT_SIZE):
            return True
        if (x < playerx + PLAYER_SIZE - 1 < x + RECT_SIZE) and (y < playery + PLAYER_SIZE - 1 < y + RECT_SIZE):
            return True
        if (x < playerx < x + RECT_SIZE) and (y < playery + PLAYER_SIZE - 1 < y + RECT_SIZE):
            return True
    return False


def game_over_text():
    text = game_over.render("Game over", True, (255, 255, 255))
    screen.blit(text, (170, 220))


# game loop
running = True
while running:
    clock.tick(60)
    # change scree color
    screen.fill((100, 100, 100))
    goal(goal_x, goal_y)
    maze_draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # move the player with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_change = 3
            if event.key == pygame.K_LEFT:
                x_change = -3
            if event.key == pygame.K_UP:
                y_change = -3
            if event.key == pygame.K_DOWN:
                y_change = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_change = 0
    # boundaries with walls
    if not is_wall_collision(player_x + x_change, player_y + y_change):
        player_x += x_change
        player_y += y_change
    # boundaries of the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= (screen_x - PLAYER_SIZE):
        player_x = screen_x - PLAYER_SIZE
    if player_y <= 0:
        player_y = 0
    elif player_y >= (screen_y - PLAYER_SIZE):
        player_y = screen_y - PLAYER_SIZE

    move_player(player_x, player_y)
    if is_goal_collision(player_x, player_y, goal_x, goal_y):
        screen.fill((100, 100, 100))
        game_over_text()
    pygame.display.update()
