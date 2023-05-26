import sys, pygame, time
import math
from bfs import bfs, create_maze_map
from generator import maze_generator

RECT_SIZE = 64
PLAYER_SIZE = 64
SPEED = 4
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
GOAL_IMAGE = "kdj.png"
PLAYER_IMAGE = "sunfish.png"
BACKGROUND_IMAGE = "background_space.png"
TITLE = "Capture the Squid"
GAME_OVER_TEXT = "You reached your ⬛⬛..."

pygame.init()
clock = pygame.time.Clock()
# create the screen
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))  # width, height
# title
pygame.display.set_caption(TITLE)
# icon
icon = pygame.image.load(ICON_IMAGE)
icon.convert()
# background
backgroundIm = pygame.image.load(BACKGROUND_IMAGE)
backgroundIm.convert()
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

    def __add__(self, other_coords):
        return Coords(self.x + other_coords.x, self.y + other_coords.y)

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)


class Player:

    def __init__(self, image: str, coordinates: Coords):
        self.player_image = pygame.image.load(image)
        self.player_image.convert()
        self.player_coords = coordinates

    # move is difference between old and new coordinates
    def move_player(self, move: Coords):
        """
        Adds move, change in coordinates, to player's coordinates.
        :param move: of type Coords, keeps the needed x and y coordinates of change
        :return: void
        """
        self.player_coords += move

    def redraw_player(self):
        """
        Redraws the player image at player coordinates on the screen.
        :return: void
        """
        screen.blit(self.player_image, (self.player_coords.x, self.player_coords.y))

    def rotate_player(self, angle: int):
        """
        Rotates the player's image by the given angle.
        Checks if the movement is to the left, the image is mirrored with respect to y-axis.
        :param angle: The angle of image rotation.
        :return: void
        """
        self.player_image = pygame.transform.rotate(self.player_image, angle)
        if angle == 180:
            self.player_image = pygame.transform.flip(self.player_image, False, True)

    def reload_player_image(self):
        """
        Reloads the player's image with the initial one
        in order to cancel all previous modifications of the image (rotation, flipping) during the movement.
        :return: void
        """
        self.player_image = pygame.image.load(PLAYER_IMAGE)
        self.player_image.convert()


class Maze:

    def __init__(self, goal_coords: Coords, maze_draft: list[int], player_to_maze: Player):
        """
        Fills the screen with background color(grey).
        Initialises self.maze_draft and self.goal_coords with given values.
        Checks if the task is to use generated maze of maze_draft.
        Initialises self.maze_coords, which is the coordinates of left upper corner of each wall.
        Draws walls, and then draws the goal.
        Initialises self.player with the given value.
        :param goal_coords: Coordinates of goal's left upper corner of type Coords.
        :param maze_draft: The list of 0's and 1's which represent road and walls, respectively.
        :param player_to_maze: The player of type Player.
        """
        # change screen color
        screen.fill((100, 100, 100))
        self.maze_draft = maze_draft
        self.goal_coords = goal_coords
        if GENERATE_MAZE:
            coordinates = []
            maze_generator(create_maze_map(), coordinates)
            self.maze_coords = coordinates
        else:
            self.maze_coords = self.create_maze_from_draft()
        self.maze_draw()
        self.goal_draw()
        # self.player = Player(player_image, player_start_coords)
        self.player = player_to_maze

    # coordinates of top left corner of each rectangle
    def create_maze_from_draft(self) -> list[(int, int)]:
        """
        Uses maze_draft, which is the list of 0's and 1's which represent road and walls, respectively.
        For each value 1, stores in the list maze_coordinates the appropriate coordinates of left upper corner of each wall.
        :return: List of coordinates of left upper corner of each wall.
        """
        maze_coordinates = []
        cor_x = 0
        cor_y = 0
        for rows in range(0, BLOCKS):
            for columns in range(0, BLOCKS):
                if self.maze_draft[rows][columns] == 1:
                    maze_coordinates.append((cor_x, cor_y))
                cor_x += RECT_SIZE
            cor_y += RECT_SIZE
            cor_x = 0
        return maze_coordinates

    def maze_draw(self):
        """
        Uses the list maze_coords of coordinates of left upper corner of each wall,
        and draws one grey square at this position with size of sides RECT_SIZE.
        :return: void
        """
        for coordinates in self.maze_coords:
            (x, y) = coordinates
            pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(x, y, RECT_SIZE, RECT_SIZE))

    def goal_draw(self):
        """
        Draws the goal image at goal coordinates on the screen.
        :return: void
        """
        screen.blit(goalIm, (self.goal_coords.x, self.goal_coords.y))

    def is_goal_collision(self) -> bool:
        """
        Calculates the distance from top left corner of player to top left corner of goal
        Checks if the distance is less than 30.
        If it is true, then it is considered as collision, True is returned, otherwise - False.
        :return: True or False
        """
        # distance between objects:
        distance = math.sqrt(math.pow(self.player.player_coords.x - self.goal_coords.x, 2) + math.pow(self.player.player_coords.y - self.goal_coords.y, 2))
        if distance <= 30:
            return True
        else:
            return False

    def is_valid_move(self, player_coordinates: Coords) -> bool:
        """
        Checks whether it is valid to move player to player_coordinates.
        Invalid moves are collisions with walls or the edge of the screen
        :param player_coordinates: New potential coordinates to move the player,
         that have to be checked
        :return: True if the move i valid, False if the move is invalid
        (collision with walls or the edge of the screen)
        """
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


def move_type(prev_move, event, angle: int) -> (int, int):
    """
    Checks the type of pressed or held button.
    For appropriate buttons(down, up, right, left) sets the coords_change for x- and y-axis of the player.
    The change SPEED is fixed, sign indicates the direction of appropriate movement.
    According to the direction of movement sets the appropriate angle of PLAYER_IMAGE rotation.
    If movement button is held, the change in coordinates is set to 0.
    :param prev_move: the change of coordinates after the previous event.
    :param event: type of user's action (the type of pressed button)
    :param angle: the angle at which the PLAYER_IMAGE has to be converted(passed angle = 0)
    :return: the appropriate angle, change in coordinate coords_change if a movement button was pressed or released,
    prev_move if the button is held.
    """
    coords_change = Coords(0, 0)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            coords_change.x = SPEED
            angle = 0
        if event.key == pygame.K_LEFT:
            coords_change.x = -SPEED
            angle = 180
        if event.key == pygame.K_UP:
            coords_change.y = -SPEED
            angle = 90
        if event.key == pygame.K_DOWN:
            coords_change.y = SPEED
            angle = 270
        return coords_change, angle
    if event.type == pygame.KEYUP:
        angle = 0
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            coords_change.x = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            coords_change.y = 0
        return coords_change, angle
    return prev_move, angle


def game_over_text():
    """
    Prints the final text after the player has reached the goal.
    :return: void
    """
    text = game_over.render(GAME_OVER_TEXT, True, (255, 255, 255))
    screen.blit(text, (100, 220))


def main():
    # game loop
    running = True
    move = Coords(0, 0)
    # create a player
    player_initial_coordinates = Coords(RECT_SIZE, RECT_SIZE)
    player = Player(PLAYER_IMAGE, player_initial_coordinates)
    goal_coords = Coords(GOAl_X, GOAl_Y)
    maze = Maze(goal_coords, maze_draft, player)
    angle = 0
    while running:
        clock.tick(60)
        # screen.fill((100, 100, 100))
        screen.blit(backgroundIm, (0, 0))
        maze.maze_draw()
        maze.goal_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check the type of keys pressed
            move, angle = move_type(move, event, angle)
        # check if the move is valid
        if maze.is_valid_move(maze.player.player_coords + move):
            maze.player.move_player(move)
            maze.player.rotate_player(angle)
        maze.player.redraw_player()
        maze.player.reload_player_image()
        # check if the goal is reached
        if maze.is_goal_collision():
            screen.fill((0, 0, 0))
            game_over_text()
        pygame.display.update()


if __name__ == "__main__":
    main()
