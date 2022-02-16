# ----------------------------------------------------------------------------------------------------------------------
# Vax-Man by Alex Burky (https://github.com/alexburky)
#
# - Developed for the Electronic Arts Software Engineering Virtual Experience Program
# - Adapted version of Pacman in Python using PyGame, from https://github.com/hbokmann/Pacman
# ----------------------------------------------------------------------------------------------------------------------
import sys
import pygame
import random
import time

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

# Set the icon
icon = pygame.image.load('images/vLogo.png')
pygame.display.set_icon(icon)

# Initialize pygame audio
pygame.mixer.init()
munch1 = pygame.mixer.Sound('audio/munch_1.wav')
munch2 = pygame.mixer.Sound('audio/munch_2.wav')

# Variable indicating whether the intro music has finished playing
gameStart = False

# How often should ghosts double? (seconds)
doubleTime = 30.0


# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        # wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall = Wall(item[0], item[1] + 100, item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    # gate.add(Wall(282, 242, 42, 2, white))
    gate.add(Wall(282, 342, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    # This class represents the bar at the bottom that the player controls


class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, rectangle, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the sprite sheet
        self.sheet = pygame.image.load(filename).convert()
        self.imageRect = rectangle
        self.image = pygame.Surface(self.imageRect.size).convert()
        self.image.blit(self.sheet, (0, 0), self.imageRect)

        # Variable to keep track of animation (which direction is being faced?)
        self.animationTop = 54

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

        # Timer to determine when to double ghosts
        self.t0 = time.time()

        # Variable used to determine the ghost's direction
        self.direction = random.randint(0, 3)
        self.isGhost = False
        self.currentFrame = 0

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y, dirFlag):
        self.change_x += x
        self.change_y += y

        # Adjust the animation based on which way the player is facing
        if dirFlag is True:
            if x > 0:
                self.direction = 0
                self.animationTop = 54
            if x < 0:
                self.direction = 1
                self.animationTop = 354
            if y > 0:
                self.direction = 2
                self.animationTop = 204
            if y < 0:
                self.direction = 3
                self.animationTop = 504

    # Find a new position for the player
    def update(self, walls, gate):

        # Get the old position, in case we need to go back to it
        old_x = self.rect.left
        new_x = old_x + self.change_x
        prev_x = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        prev_y = old_y + self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
            self.direction = random.randint(0, 3)
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y
                self.direction = random.randint(0, 3)

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y

        # Animate the sprites
        if self.isGhost:
            if self.currentFrame == 1:
                self.currentFrame = 0
            else:
                self.currentFrame = 1
        else:
            if new_x != old_x or new_y != old_y:
                if self.currentFrame == 1:
                    self.currentFrame = 0
                else:
                    self.currentFrame = 1

        self.imageRect.top = self.animationTop + (50 * self.currentFrame)
        self.image.blit(self.sheet, (0, 0), self.imageRect)


# Ghost class inherits from Player
class Ghost(Player):
    def __init__(self, x, y, rectangle, filename):
        super(Ghost, self).__init__(x, y, rectangle, filename)
        self.isGhost = True
        self.animationTop = 4 + (self.direction * 100)
        self.imageRect.top = self.animationTop

    # Keep track of how long this ghost has been alive
    def getElapsedTime(self):

        # Hold the timer until the game starts
        if gameStart is False:
            self.t0 = time.time()

        t1 = time.time()
        t_elapsed = t1 - self.t0
        if t_elapsed > doubleTime:
            self.t0 = time.time()

        return t_elapsed

    # Function to move ghosts and keep track of their orientation
    def changespeed(self):

        ghostSpeed = 10

        if self.direction == 0:
            self.change_x = ghostSpeed
            self.change_y = 0
            self.animationTop = 4
        elif self.direction == 1:
            self.change_x = 0
            self.change_y = ghostSpeed
            self.animationTop = 104
        elif self.direction == 2:
            self.change_x = -ghostSpeed
            self.change_y = 0
            self.animationTop = 204
        elif self.direction == 3:
            self.change_x = 0
            self.change_y = -ghostSpeed
            self.animationTop = 304


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606 x 706 sized screen
screen = pygame.display.set_mode([606, 706])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'

# Set the title of the window
pygame.display.set_caption('Vax-Man')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("fonts/emulogic.ttf", 24)

tfont = pygame.font.Font("fonts/CrackMan.TTF", 48)

# default locations for Pacman and monstas
w = 303 - 16  # Width
p_h = (7 * 60) + 19    # Pacman height
m_h = (4 * 60) + 19    # Monster height
b_h = (3 * 60) + 19    # Binky height
i_w = 303 - 16 - 32    # Inky width
c_w = 303 + (32 - 16)  # Clyde width


def startGame():
    global gameStart
    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    # Lists for each of the individual monsters
    blinky_list = pygame.sprite.RenderPlain()
    clyde_list = pygame.sprite.RenderPlain()
    inky_list = pygame.sprite.RenderPlain()
    pinky_list = pygame.sprite.RenderPlain()

    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    # Variable to track which sound effect to play
    munch = 0

    # Set the player's movement speed
    pacmanSpeed = 30

    # Create the player paddle object
    pacRect = pygame.Rect((17*50) + 1, (1*50) + 4, 36, 36)
    blinkyRect = pygame.Rect((0*50) + 1, (0*50) + 4, 36, 36)
    clydeRect = pygame.Rect((3*50) + 1, (0*50) + 4, 36, 36)
    inkyRect = pygame.Rect((2*50) + 1, (0*50) + 4, 36, 36)
    pinkyRect = pygame.Rect((1*50) + 1, (0*50) + 4, 36, 36)

    Pacman = Player(w, p_h + 100, pacRect, "images/spritesheet.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    # Add an initial ghost to each list
    blinky_list.add(Ghost(17, 559 + 100, blinkyRect, "images/spritesheet.png"))
    pinky_list.add(Ghost(17, 19 + 100, pinkyRect, "images/spritesheet.png"))
    inky_list.add(Ghost(557, 559 + 100, inkyRect, "images/spritesheet.png"))
    clyde_list.add(Ghost(557, 19 + 100, clydeRect, "images/spritesheet.png"))

    # Draw the grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26 + 100

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

    score = 0
    bll = len(block_list)
    done = False
    startedMoving = False

    # Play the start-game music
    pygame.mixer.music.load('audio/game_start.wav')
    pygame.mixer.music.play(0)

    while done == False:
        # Play the intro music and hold the game until it finishes
        if pygame.mixer.music.get_busy() is False and gameStart is False:
            gameStart = True
            pygame.mixer.music.load('audio/siren_1.wav')
            pygame.mixer.music.play(-1, 0.0)

        # Multiply ghosts if certain time has elapsed (30 seconds by default)
        for blinky in blinky_list:
            if blinky.getElapsedTime() > doubleTime:
                blinky_list.add(Ghost(blinky.rect.left, blinky.rect.top, blinkyRect, "images/spritesheet.png"))

        for pinky in pinky_list:
            if pinky.getElapsedTime() > doubleTime:
                pinky_list.add(Ghost(pinky.rect.left, pinky.rect.top, pinkyRect, "images/spritesheet.png"))

        for inky in inky_list:
            if inky.getElapsedTime() > doubleTime:
                inky_list.add(Ghost(inky.rect.left, inky.rect.top, inkyRect, "images/spritesheet.png"))

        for clyde in clyde_list:
            if clyde.getElapsedTime() > doubleTime:
                clyde_list.add(Ghost(clyde.rect.left, clyde.rect.top, clydeRect, "images/spritesheet.png"))

        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if gameStart:
                if event.type == pygame.KEYDOWN:
                    startedMoving = True
                    if event.key == pygame.K_LEFT:
                        Pacman.changespeed(-pacmanSpeed, 0, True)
                    if event.key == pygame.K_RIGHT:
                        Pacman.changespeed(pacmanSpeed, 0, True)
                    if event.key == pygame.K_UP:
                        Pacman.changespeed(0, -pacmanSpeed, True)
                    if event.key == pygame.K_DOWN:
                        Pacman.changespeed(0, pacmanSpeed, True)

                if event.type == pygame.KEYUP and startedMoving is True:
                    if event.key == pygame.K_LEFT:
                        Pacman.changespeed(pacmanSpeed, 0, False)
                    if event.key == pygame.K_RIGHT:
                        Pacman.changespeed(-pacmanSpeed, 0, False)
                    if event.key == pygame.K_UP:
                        Pacman.changespeed(0, pacmanSpeed, False)
                    if event.key == pygame.K_DOWN:
                        Pacman.changespeed(0, -pacmanSpeed, False)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        if gameStart:
            Pacman.update(wall_list, gate)

            # Update all Pinkies
            for pinky in pinky_list:
                pinky.changespeed()
                pinky.update(wall_list, False)
            # Update all Blinkies
            for blinky in blinky_list:
                blinky.changespeed()
                blinky.update(wall_list, False)
            # Update all Inkies
            for inky in inky_list:
                inky.changespeed()
                inky.update(wall_list, False)
            # Update all Clydes
            for clyde in clyde_list:
                clyde.changespeed()
                clyde.update(wall_list, False)

        # See if the Pacman block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)
            if munch == 0:
                pygame.mixer.Sound.play(munch1)
                munch = 1
            else:
                pygame.mixer.Sound.play(munch2)
                munch = 0

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)

        blinky_list.draw(screen)
        pinky_list.draw(screen)
        inky_list.draw(screen)
        clyde_list.draw(screen)

        text = font.render(str(score*10), True, white)
        screen.blit(text, [10, 10 + 40])
        scoreLabel = font.render("Score", True, white)
        screen.blit(scoreLabel, [10, 10])

        title = tfont.render("VAX-MAN", True, yellow)
        screen.blit(title, [170, 25])

        if score == bll:
            pygame.mixer.music.load('audio/intermission.wav')
            pygame.mixer.music.play(-1, 0.0)
            doNext("Victory!", 200, all_sprites_list, block_list, blinky_list, inky_list, pinky_list,
                   clyde_list, pacman_collide, wall_list, gate)

        blinky_hit_list = pygame.sprite.spritecollide(Pacman, blinky_list, True)
        pinky_hit_list = pygame.sprite.spritecollide(Pacman, pinky_list, True)
        inky_hit_list = pygame.sprite.spritecollide(Pacman, inky_list, True)
        clyde_hit_list = pygame.sprite.spritecollide(Pacman, clyde_list, True)

        # Tally up how many ghosts there are to determine whether or not the game is over
        nGhosts = 0
        nGhosts += len(blinky_list)
        nGhosts += len(inky_list)
        nGhosts += len(pinky_list)
        nGhosts += len(clyde_list)

        ghostLabel = font.render("Ghosts", True, white)
        screen.blit(ghostLabel, [450, 10])
        ghostText = font.render(str(nGhosts), True, white)
        screen.blit(ghostText, [450, 50])

        if nGhosts >= 128:
            pygame.mixer.music.load('audio/death_1.wav')
            pygame.mixer.music.play(0)
            doNext("Game Over", 195, all_sprites_list, block_list, blinky_list, inky_list, pinky_list, clyde_list,
                   pacman_collide, wall_list, gate)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, blinky_list, inky_list, pinky_list, clyde_list, pacman_collide,
           wall_list, gate):
    global gameStart
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit(1)
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del blinky_list
                    del inky_list
                    del pinky_list
                    del clyde_list
                    del pacman_collide
                    del wall_list
                    del gate
                    gameStart = False
                    startGame()

        # Grey background
        w = pygame.Surface((400, 300))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again:", True, white)
        text3 = font.render("press ENTER", True, white)
        screen.blit(text2, [135, 303])
        screen.blit(text3, [160, 333])
        text4 = font.render("To quit:", True, white)
        text5 = font.render("press Escape", True, white)
        screen.blit(text4, [200, 383])
        screen.blit(text5, [150, 413])

        pygame.display.flip()

        clock.tick(10)


startGame()

pygame.quit()
sys.exit()
