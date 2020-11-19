# Loading Necessary Modules
import pygame
import random
import math
import time

# Initializing PyGame Module
pygame.init()


# Game Start, Game Pause, Game Result, Game Difficulty, Game Instructions
class Main_Screen:

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    orange = (255, 128, 0)
    grey = (211, 211, 211)
    yellow = (200, 200, 0)
    sky_blue = (135, 206, 250)

    # Value of "g"
    value_of_g = -4.6

    # Resolution
    res = [1200, 800]

    # Tanks Size
    tank_length_height = [90, 70]

    # Ground
    ground_length_height = [res[0], int(res[1] / 4.5)]
    ground_starting_ending_point = [(0, res[1] - (ground_length_height[1] / 2)), (res[0], res[1] - (ground_length_height[1] / 2))]

    # Middle Wall
    wall_length_height = [int(res[0] / 6), int(res[1] / 3)]
    wall_starting_ending_point = [(res[0] / 2 - (wall_length_height[0] / 2), res[1] - ground_length_height[1] - (wall_length_height[1] / 2)), (res[0] / 2 + (wall_length_height[0] / 2), res[1] - ground_length_height[1] - (wall_length_height[1] / 2))]

    # Tanks Position And Boundaries Data
    my_tank_x_y_position = [random.randrange(0, res[0] / 2 - wall_length_height[0] - tank_length_height[0]), res[1] - ground_length_height[1] - tank_length_height[1]]
    my_tank_right_left_boundary = [(res[0] / 2) - (wall_length_height[0] / 2) - tank_length_height[0], 0]

    enemy_tank_x_y_position = [random.randrange(res[0] / 2 + wall_length_height[0], res[0] - tank_length_height[0]), res[1] - ground_length_height[1] - tank_length_height[1]]
    enemy_tank_right_left_boundary = [res[0] - tank_length_height[0], res[0] / 2 + (wall_length_height[0] / 2)]
    enemy_tank_to_right_boundary_left_wall_distance = [0, 0]

    # Distance Between Two Tanks(From Their Middle)
    distance_between_tanks = 0

    # Tanks Health Bars
    my_health_bar = [[10, 30], [310, 30]]
    enemy_health_bar = [[res[0] - 310, 30], [res[0] - 10, 30]]
    my_health_percentage = enemy_health_percentage = '100%'

    # Shells Position Data
    my_shell_position = [0, 0]
    my_shell_new_position = [0, 0]
    my_shell_distance = [0, 0]
    my_shoot = True

    enemy_shell_position = [0, 0]
    enemy_shell_new_position = [0, 0]
    enemy_shell_distance = [0, 0]
    enemy_shoot = True

    shell_radius = 10

    # Tanks Movement
    my_tank_acceleration = enemy_tank_acceleration = 0
    my_tank_movement = enemy_tank_movement = 5
    enemy_motion = True
    enemy_moving_time = [0, 0]

    # Projectile Data
    pos = 0
    power = 0
    power_components = [0, 0]
    angle = 0
    time = 0

    # Sounds
    shell_fire_sound = pygame.mixer.Sound('Shell Fire.wav')
    shell_explosion_sound = pygame.mixer.Sound('Shell Explosion.wav')
    tank_sound = pygame.mixer.Sound('Tank Moving Sound.wav')
    menu_sound = pygame.mixer.Sound('Menu Sound.wav')

    # Images
    my_tank = pygame.image.load('Tank.png')
    enemy_tank = pygame.image.load('Enemy Tank.png')
    explosion = pygame.image.load('Explosion.png')

    # Fonts
    small_font = pygame.font.SysFont('ComicSansMS', 25, True, False)
    medium_font = pygame.font.SysFont('ComicSansMS', 45, True, False)
    large_font = pygame.font.SysFont('ComicSansMS', 75, True, False)

    # Game Difficulty
    game_difficulty = ['Easy', 'Medium', 'Hard']
    current_difficulty = game_difficulty[0]

    # Frames Per Second
    clock = pygame.time.Clock()
    FPS = 100

    game_finish = False
    game_pause = True

    intro = True

    # The Main Game Function(Game Starts From Here)
    def __init__(self):

        # Screen Drawing and Setting Screen Resolution
        self.game_display = pygame.display.set_mode((self.res[0], self.res[1]))
        pygame.display.set_caption("Tanks")
        pygame.display.set_icon(self.my_tank)
        self.game_display.fill(self.white)

        # Introduction Messages
        Messages.message_to_screen(self, "Welcome To Tanks", self.blue, "Large", -150, 0, 'Yes')
        Messages.message_to_screen(self, "Press 'S' For Settings", self.green, "Small", 0, 0, 'Yes')
        Messages.message_to_screen(self, "Press 'P' to play or 'Q' to exit", self.red, "Medium", 100, 0, 'Yes')

        pygame.display.update()

        # Introduction Screen Loop
        while self.intro:

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Press Event
                elif event.type == pygame.KEYDOWN:
                    pygame.mixer.Sound.play(self.menu_sound)

                    # To Play
                    if event.key == pygame.K_p:
                        self.intro = False
                        Game_Screen.game_main(self)

                    # To Quit
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

                    # For Settings
                    elif event.key == pygame.K_s:
                        Main_Screen.game_settings(self)

    # Game Pause Screen
    def game_paused(self):

        # For Game Pause
        while self.game_pause:
            # self.game_display.fill(self.white)
            Messages.message_to_screen(self, 'The Game Has Been Paused', self.red, "Large", -50, 0, 'Yes')
            Messages.message_to_screen(self, 'Press Any Key To Continue', self.blue, "Medium", 50, 0, 'Yes')
            Messages.message_to_screen(self, 'Or "Q" to Quit', self.blue, "Medium", 100, 0, 'Yes')

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                if event.type == pygame.KEYDOWN:

                    pygame.mixer.Sound.play(self.menu_sound)

                    # Pause Over Event
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    self.game_pause = False

            pygame.display.update()

    # Game Result Screen
    def game_result(self):

        self.game_display.fill(self.white)

        # When Game Won
        if self.enemy_health_bar[0] == self.enemy_health_bar[1]:
            Messages.message_to_screen(self, 'You Won :)', self.green, "Large", -50, 0, 'Yes')

        # When Game Over
        if self.my_health_bar[0] == self.my_health_bar[1]:
            Messages.message_to_screen(self, 'Game Over :(', self.red, "Large", -50, 0, 'Yes')

        Messages.message_to_screen(self, "Press 'P' To Play Again or 'Q' To Quit", self.blue, "Medium", 50, 0, 'Yes')
        Messages.message_to_screen(self, "Press 'S' For Settings", self.green, "Small", 125, 0, 'Yes')

        pygame.display.update()

        # Game Result Loop
        while self.game_finish:

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                if event.type == pygame.KEYDOWN:

                    pygame.mixer.Sound.play(self.menu_sound)

                    # To Play Again
                    if event.key == pygame.K_p:
                        self.game_finish = False
                        self.my_tank_x_y_position = [random.randrange(0, self.res[0] / 2 - self.wall_length_height[0] - self.tank_length_height[0]), self.res[1] - self.ground_length_height[1] - self.tank_length_height[1]]
                        self.enemy_tank_x_y_position = [random.randrange(self.res[0] / 2 + self.wall_length_height[0], self.res[0] - self.tank_length_height[0]), self.res[1] - self.ground_length_height[1] - self.tank_length_height[1]]
                        self.my_health_bar = [[10, 30], [310, 30]]
                        self.enemy_health_bar = [[self.res[0] - 310, 30], [self.res[0] - 10, 30]]
                        self.my_health_percentage = '100%'
                        self.enemy_health_percentage = '100%'
                        self.my_shell_position = [0, 0]
                        self.my_shell_new_position = [0, 0]
                        self.my_shell_distance = [0, 0]
                        self.my_shoot = True
                        self.enemy_shell_position = [0, 0]
                        self.enemy_shell_new_position = [0, 0]
                        self.enemy_shell_distance = [0, 0]
                        self.enemy_shoot = True
                        Game_Screen.game_main(self)

                    # To Quit
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                    # For Settings
                    elif event.key == pygame.K_s:
                        self.intro = True
                        Main_Screen.game_settings(self)
                        self.intro = False

    # Game Settings
    def game_settings(self):

        while self.intro:
            self.game_display.fill(self.white)
            Messages.message_to_screen(self, "Settings", self.blue, "Large", -350, 0, 'Yes')
            Messages.message_to_screen(self, "-------", self.black, "Large", -300, 0, 'Yes')
            Messages.message_to_screen(self, "D = Difficulty :", self.black, "Medium", -50, 15, 'No')

            if self.current_difficulty == self.game_difficulty[0]:
                Messages.message_to_screen(self, self.current_difficulty, self.green, "Medium", -50, 360, 'No')
            if self.current_difficulty == self.game_difficulty[1]:
                Messages.message_to_screen(self, self.current_difficulty, self.orange, "Medium", -50, 360, 'No')
            if self.current_difficulty == self.game_difficulty[2]:
                Messages.message_to_screen(self, self.current_difficulty, self.red, "Medium", -50, 360, 'No')

            Messages.message_to_screen(self, "H = Help", self.black, "Medium", 50, 15, 'No')
            Messages.message_to_screen(self, "Esc = Go Back", self.black, "Medium", 150, 15, 'No')

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                elif event.type == pygame.KEYDOWN:

                    pygame.mixer.Sound.play(self.menu_sound)

                    # To Change Difficulty
                    if event.key == pygame.K_d:
                        if self.current_difficulty == self.game_difficulty[0]:
                            self.current_difficulty = self.game_difficulty[1]
                        elif self.current_difficulty == self.game_difficulty[1]:
                            self.current_difficulty = self.game_difficulty[2]
                        elif self.current_difficulty == self.game_difficulty[2]:
                            self.current_difficulty = self.game_difficulty[0]

                    # To Check For Instructions
                    elif event.key == pygame.K_h:
                        Main_Screen.game_help(self)

                    # To Go Back
                    elif event.key == pygame.K_ESCAPE:
                        if self.my_health_bar[0] == self.my_health_bar[1] or self.enemy_health_bar[0] == self.enemy_health_bar[1]:
                            Main_Screen.game_result(self)
                        else:
                            Main_Screen.__init__(self)

            pygame.display.update()

    # Game Help
    def game_help(self):

        while self.intro:
            self.game_display.fill(self.white)

            # Instructions
            Messages.message_to_screen(self, "Instructions", self.blue, "Large", -350, 0, 'Yes')
            Messages.message_to_screen(self, "----------", self.black, "Large", -300, 0, 'Yes')
            Messages.message_to_screen(self, "1. The objective of the game is to destroy the enemy tank.", self.green, "Small", -150, 15, 'No')
            Messages.message_to_screen(self, "2. The tank to your left is your tank whereas the right one is controlled by computer.", self.green, "Small", -100, 15, 'No')
            Messages.message_to_screen(self, "3. Every time you got hit by the shell, your health will decrease by 10%.", self.green, "Small", -50, 15, 'No')
            Messages.message_to_screen(self, "4. To fire the shell, click anywhere on the screen in front of your tank.", self.green, "Small", 0, 15, 'No')
            Messages.message_to_screen(self, "5. The longer the fire line, the higher the shell power.", self.green, "Small", 50, 15, 'No')
            Messages.message_to_screen(self, "Esc = Go Back", self.black, "Medium", 150, 15, 'No')

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                if event.type == pygame.KEYDOWN:

                    pygame.mixer.Sound.play(self.menu_sound)

                    # To Go Back
                    if event.key == pygame.K_ESCAPE:
                        Main_Screen.game_settings(self)

            pygame.display.update()


# Game Main User Controlled Screen
class Game_Screen(Main_Screen):

    # For Controlling My Tank(Also The Main Game Loop As All Classes Are Executed From Here)
    def game_main(self):

        # Main Game Loop
        while not self.game_finish:

            # My Shell and Mouse Pointer Location (Updated Recursively at the rate of FPS)
            self.my_shell_position = [self.my_tank_x_y_position[0] + self.tank_length_height[0], self.my_tank_x_y_position[1] + 3]
            self.pos = pygame.mouse.get_pos()

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Press Event
                elif event.type == pygame.KEYDOWN:

                    # Left Movement Of My Tank
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if self.my_tank_x_y_position[0] - self.my_tank_movement < self.my_tank_right_left_boundary[1]:
                            self.my_tank_acceleration = 0
                        else:
                            self.my_tank_acceleration = -self.my_tank_movement

                    # Right Movement Of My Tank
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if self.my_tank_x_y_position[0] + self.my_tank_movement > self.my_tank_right_left_boundary[0]:
                            self.my_tank_acceleration = 0
                        else:
                            self.my_tank_acceleration = self.my_tank_movement

                    # For Game Pause
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        Main_Screen.game_paused(self)
                        self.game_pause = True

                # Key Release Event
                elif event.type == pygame.KEYUP:

                    # To Stop Left Movement Of My Tank
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.my_tank_acceleration = 0

                    # To Stop Right Movement Of My Tank
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.my_tank_acceleration = 0

                # Mouse Click Event
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # My Projectile Data Calculation
                    self.pos = pygame.mouse.get_pos()
                    self.power = ((((self.pos[1] - self.my_shell_position[1]) ** 2) + ((self.pos[0] - self.my_shell_position[0]) ** 2)) ** (1 / 2)) / 6

                    if self.my_shell_position[0] - self.pos[0] == 0:
                        self.angle = math.radians(90)
                    else:
                        self.angle = math.atan((self.my_shell_position[1] - self.pos[1]) / (self.my_shell_position[0] - self.pos[0]))
                        print(self.angle)
                        if self.angle < 0:
                            self.angle = -self.angle

                    self.power_components[0] = self.power * math.cos(self.angle)
                    self.power_components[1] = self.power * math.sin(self.angle)
                    Tank_Shot.my_shot(self)
                    self.my_shoot = True

            # Tank Boundary Restriction Handling
            if self.my_tank_x_y_position[0] + self.my_tank_acceleration < self.my_tank_right_left_boundary[1] or self.my_tank_x_y_position[0] + self.my_tank_acceleration > self.my_tank_right_left_boundary[0]:
                self.my_tank_acceleration = 0
            else:
                self.my_tank_x_y_position[0] += self.my_tank_acceleration
                if self.my_tank_acceleration != 0:
                    pygame.mixer.Sound.play(self.tank_sound)

            # Screen Drawing
            self.game_display.fill(self.sky_blue)
            self.game_display.blit(self.my_tank, (self.my_tank_x_y_position[0], self.my_tank_x_y_position[1]))
            self.game_display.blit(self.enemy_tank, (self.enemy_tank_x_y_position[0], self.enemy_tank_x_y_position[1]))
            Messages.message_to_screen(self, self.my_health_percentage, self.black, "Small", -350, 10, 'No')
            Messages.message_to_screen(self, self.enemy_health_percentage, self.black, "Small", -350, self.res[0] - 75, 'No')
            pygame.draw.line(self.game_display, self.blue, self.my_health_bar[0], self.my_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.red, self.enemy_health_bar[0], self.enemy_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.grey, self.ground_starting_ending_point[0], self.ground_starting_ending_point[1], self.ground_length_height[1])
            pygame.draw.line(self.game_display, self.grey, self.wall_starting_ending_point[0], self.wall_starting_ending_point[1], self.wall_length_height[1])
            pygame.draw.line(self.game_display, self.black, self.my_shell_position, self.pos, 1)

            pygame.display.update()
            self.clock.tick(self.FPS)


# Projectile Shots
class Tank_Shot(Game_Screen):

    # For Shooting My Tank Shell
    def my_shot(self):

        pygame.mixer.Sound.play(self.shell_fire_sound)

        # My Projectile Pathway Loop
        while self.my_shoot:

            # New Position of My Shell on a Projectile Pathway
            self.my_shell_distance[0] = round(self.power_components[0] * self.time)
            self.my_shell_distance[1] = round((self.power_components[1] * self.time) + (0.5 * self.value_of_g * (self.time ** 2)))
            self.my_shell_new_position[0] = self.my_shell_position[0] + self.my_shell_distance[0]
            self.my_shell_new_position[1] = self.my_shell_position[1] - self.my_shell_distance[1]

            # Screen Drawing
            self.game_display.fill(self.sky_blue)
            self.game_display.blit(self.my_tank, (self.my_tank_x_y_position[0], self.my_tank_x_y_position[1]))
            self.game_display.blit(self.enemy_tank, (self.enemy_tank_x_y_position[0], self.enemy_tank_x_y_position[1]))
            Messages.message_to_screen(self, self.my_health_percentage, self.black, "Small", -350, 10, 'No')
            Messages.message_to_screen(self, self.enemy_health_percentage, self.black, "Small", -350, self.res[0] - 75, 'No')
            pygame.draw.line(self.game_display, self.blue, self.my_health_bar[0], self.my_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.red, self.enemy_health_bar[0], self.enemy_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.grey, self.ground_starting_ending_point[0], self.ground_starting_ending_point[1], self.ground_length_height[1])
            pygame.draw.line(self.game_display, self.grey, self.wall_starting_ending_point[0], self.wall_starting_ending_point[1], self.wall_length_height[1])
            pygame.draw.circle(self.game_display, self.black, self.my_shell_new_position, self.shell_radius)

            # Projectile Data (for development purposes only)
            # print('angle:', math.degrees(self.angle))
            # print('power:', self.power)
            # print('my shell x distance:', self.my_shell_distance[0])
            # print('my shell y distance:', self.my_shell_distance[1])
            # print('my shell x new pos:', self.my_shell_new_position[0])
            # print('my shell y new pos:', self.my_shell_new_position[1])

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                elif event.type == pygame.KEYDOWN:

                    # For Game Pause
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        Main_Screen.game_paused(self)
                        self.game_pause = True

            # Shell Speed
            self.time += 0.3

            # Boundaries and Ground Shell Collision Detection
            if (self.my_shell_new_position[0] + self.shell_radius) >= self.res[0] or (self.my_shell_new_position[1] + self.shell_radius) >= (self.res[1] - self.ground_length_height[1]):
                self.my_shoot = False
                self.time = 0
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.my_shell_new_position[0] - 70, self.my_shell_new_position[1] - 70))
                    pygame.display.update()
                Computer_Controlled_Tank.enemy_tank_motion(self)
                self.enemy_motion = True
                self.my_shell_new_position = [0, 0]

            # Shell and Wall Collision Detection
            elif (self.my_shell_new_position[0] + self.shell_radius) >= ((self.res[0] / 2) - (self.wall_length_height[0] / 2)) and (self.my_shell_new_position[0] - self.shell_radius) <= ((self.res[0] / 2) + (self.wall_length_height[0] / 2)) and (self.my_shell_new_position[1] + self.shell_radius) >= (self.res[1] - self.ground_length_height[1] - self.wall_length_height[1]):
                self.my_shoot = False
                self.time = 0
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.my_shell_new_position[0] - 70, self.my_shell_new_position[1] - 70))
                    pygame.display.update()
                Computer_Controlled_Tank.enemy_tank_motion(self)
                self.enemy_motion = True
                self.my_shell_new_position = [0, 0]

            # Enemy Tank Shell Collision Detection
            elif (self.my_shell_new_position[0] + self.shell_radius) >= self.enemy_tank_x_y_position[0] and (self.my_shell_new_position[0] - self.shell_radius) <= (self.enemy_tank_x_y_position[0] + self.tank_length_height[0]) and (self.my_shell_new_position[1] + self.shell_radius) >= self.enemy_tank_x_y_position[1]:
                self.my_shoot = False
                self.time = 0
                if self.enemy_health_bar[0] != self.enemy_health_bar[1]:
                    self.enemy_health_bar[0][0] += 30
                    self.enemy_health_percentage = self.enemy_health_percentage.replace('%', '')
                    self.enemy_health_percentage = str(int(self.enemy_health_percentage) - 10)
                    self.enemy_health_percentage += '%'
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                if self.enemy_health_bar[0] == self.enemy_health_bar[1]:
                    self.game_finish = True
                    Main_Screen.game_result(self)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.my_shell_new_position[0] - 70, self.my_shell_new_position[1] - 70))
                    pygame.display.update()
                Computer_Controlled_Tank.enemy_tank_motion(self)
                self.enemy_motion = True
                self.my_shell_new_position = [0, 0]

            # My Tank Shell Collision Detection
            elif (self.my_shell_new_position[0] + self.shell_radius) >= self.my_tank_x_y_position[0] and (self.my_shell_new_position[0] - self.shell_radius) <= (self.my_tank_x_y_position[0] + self.tank_length_height[0]) and (self.my_shell_new_position[1] + self.shell_radius) >= (self.my_tank_x_y_position[1] + 15):
                self.my_shoot = False
                self.time = 0
                if self.my_health_bar[0] != self.my_health_bar[1]:
                    self.my_health_bar[1][0] -= 30
                    self.my_health_percentage = self.my_health_percentage.replace('%', '')
                    self.my_health_percentage = str(int(self.my_health_percentage) - 10)
                    self.my_health_percentage += '%'
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                if self.my_health_bar[0] == self.my_health_bar[1]:
                    self.game_finish = True
                    Main_Screen.game_result(self)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.my_shell_new_position[0] - 70, self.my_shell_new_position[1] - 70))
                    pygame.display.update()
                Computer_Controlled_Tank.enemy_tank_motion(self)
                self.enemy_motion = True
                self.my_shell_new_position = [0, 0]

            pygame.display.update()
            self.clock.tick(self.FPS)

    # For Shooting Enemy Tank Shell
    def enemy_shot(self):

        # Enemy Projectile Data Calculation
        self.distance_between_tanks = self.enemy_tank_x_y_position[0] - (self.my_tank_x_y_position[0] + (self.tank_length_height[0] / 2))

        # Setting Range According To The Difficulty
        if self.current_difficulty == self.game_difficulty[0]:  # For Easy
            self.distance_between_tanks = random.randrange(self.distance_between_tanks - (int(2.5 * self.tank_length_height[0])), self.distance_between_tanks + (int(2.5 * self.tank_length_height[0])))
        if self.current_difficulty == self.game_difficulty[1]:  # For Medium
            self.distance_between_tanks = random.randrange(self.distance_between_tanks - (int(1.75 * self.tank_length_height[0])), self.distance_between_tanks + (int(1.75 * self.tank_length_height[0])))
        if self.current_difficulty == self.game_difficulty[2]:  # For Hard
            self.distance_between_tanks = random.randrange(self.distance_between_tanks - (int(1.0 * self.tank_length_height[0])), self.distance_between_tanks + (int(1.0 * self.tank_length_height[0])))

        # Setting Angle And Power
        self.power = random.randrange(4900, 8100)
        self.angle_choice = random.randrange(0, 2)
        self.angle = (math.asin((self.distance_between_tanks * self.value_of_g) / self.power)) / 2
        if self.angle < 0:
            self.angle = -self.angle
        self.angle = math.radians(90 - math.degrees(self.angle))
        self.power = math.sqrt(self.power)

        self.power_components[0] = self.power * math.cos(self.angle)
        self.power_components[1] = self.power * math.sin(self.angle)

        pygame.mixer.Sound.play(self.shell_fire_sound)

        # Enemy Projectile Pathway Loop
        while self.enemy_shoot:

            # New Position Of Enemy Shell On A Projectile Pathway
            self.enemy_shell_distance[0] = round(self.power_components[0] * self.time)
            self.enemy_shell_distance[1] = round((self.power_components[1] * self.time) + (0.5 * self.value_of_g * (self.time ** 2)))
            self.enemy_shell_new_position[0] = self.enemy_shell_position[0] - self.enemy_shell_distance[0]
            self.enemy_shell_new_position[1] = self.enemy_shell_position[1] - self.enemy_shell_distance[1]

            # Screen Drawing
            self.game_display.fill(self.sky_blue)
            self.game_display.blit(self.my_tank, (self.my_tank_x_y_position[0], self.my_tank_x_y_position[1]))
            self.game_display.blit(self.enemy_tank, (self.enemy_tank_x_y_position[0], self.enemy_tank_x_y_position[1]))
            Messages.message_to_screen(self, self.my_health_percentage, self.black, "Small", -350, 10, 'No')
            Messages.message_to_screen(self, self.enemy_health_percentage, self.black, "Small", -350, self.res[0] - 75, 'No')
            pygame.draw.line(self.game_display, self.blue, self.my_health_bar[0], self.my_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.red, self.enemy_health_bar[0], self.enemy_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.grey, self.ground_starting_ending_point[0], self.ground_starting_ending_point[1], self.ground_length_height[1])
            pygame.draw.line(self.game_display, self.grey, self.wall_starting_ending_point[0], self.wall_starting_ending_point[1], self.wall_length_height[1])
            pygame.draw.circle(self.game_display, self.black, self.enemy_shell_new_position, self.shell_radius)

            # Projectile Data(for development purposes only)
            # print('enemy angle:', math.degrees(self.angle))
            # print('enemy power:', self.power)
            # print('enemy shell x distance:', self.enemy_shell_distance[0])
            # print('enemy shell y distance:', self.enemy_shell_distance[1])
            # print('enemy shell x new pos:', self.enemy_shell_new_position[0])
            # print('enemy shell y new pos:', self.enemy_shell_new_position[1])

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                elif event.type == pygame.KEYDOWN:

                    # For Game Pause
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        Main_Screen.game_paused(self)
                        self.game_pause = True

            # Shell Speed
            self.time += 0.3

            # Boundaries and Ground Shell Collision Detection
            if (self.enemy_shell_new_position[0] - self.shell_radius) <= 0 or (self.enemy_shell_new_position[1] + self.shell_radius) >= (self.res[1] - self.ground_length_height[1]):
                self.enemy_shoot = False
                self.time = 0
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.enemy_shell_new_position[0] - 70, self.enemy_shell_new_position[1] - 70))
                    pygame.display.update()
                self.enemy_shell_new_position = [0, 0]

            # Shell and Wall Collision Detection
            elif (self.enemy_shell_new_position[0] - self.shell_radius) <= ((self.res[0] / 2) + (self.wall_length_height[0] / 2)) and (self.enemy_shell_new_position[0] + self.shell_radius) >= ((self.res[0] / 2) - (self.wall_length_height[0] / 2)) and (self.enemy_shell_new_position[1] + self.shell_radius) >= (self.res[1] - self.ground_length_height[1] - self.wall_length_height[1]):
                self.enemy_shoot = False
                self.time = 0
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.enemy_shell_new_position[0] - 70, self.enemy_shell_new_position[1] - 70))
                    pygame.display.update()
                self.enemy_shell_new_position = [0, 0]

            # My Tank Shell Collision Detection
            elif (self.enemy_shell_new_position[0] - self.shell_radius) <= (self.my_tank_x_y_position[0] + self.tank_length_height[0]) and (self.enemy_shell_new_position[0] + self.shell_radius) >= self.my_tank_x_y_position[0] and (self.enemy_shell_new_position[1] + self.shell_radius) >= self.my_tank_x_y_position[1]:
                self.enemy_shoot = False
                self.time = 0
                if self.my_health_bar[0] != self.my_health_bar[1]:
                    self.my_health_bar[1][0] -= 30
                    self.my_health_percentage = self.my_health_percentage.replace('%', '')
                    self.my_health_percentage = str(int(self.my_health_percentage) - 10)
                    self.my_health_percentage += '%'
                shell_explosion_sound = pygame.mixer.Sound.play(self.shell_explosion_sound)
                if self.my_health_bar[0] == self.my_health_bar[1]:
                    self.game_finish = True
                    Main_Screen.game_result(self)
                for x in range(100):
                    self.game_display.blit(self.explosion, (self.enemy_shell_new_position[0] - 70, self.enemy_shell_new_position[1] - 70))
                    pygame.display.update()
                self.enemy_shell_new_position = [0, 0]

            pygame.display.update()
            self.clock.tick(self.FPS)


class Computer_Controlled_Tank(Game_Screen):

    # For Enemy Tank Motion
    def enemy_tank_motion(self):

        # Measuring Distance From Tank To Boundary And Tank To Wall
        self.enemy_tank_to_right_boundary_left_wall_distance[0] = self.res[0] - (self.enemy_tank_x_y_position[0] + self.tank_length_height[0])
        self.enemy_tank_to_right_boundary_left_wall_distance[1] = self.enemy_tank_x_y_position[0] - ((self.res[0] / 2) + (self.wall_length_height[0] / 2))

        # Moving Time Duration
        self.enemy_moving_time = time.time() + random.randrange(1, 8) / 10

        # Taking Decision Where To Move
        if self.enemy_tank_to_right_boundary_left_wall_distance[0] <= self.enemy_tank_to_right_boundary_left_wall_distance[1]:
            self.enemy_tank_acceleration = -self.enemy_tank_movement
        elif self.enemy_tank_to_right_boundary_left_wall_distance[0] >= self.enemy_tank_to_right_boundary_left_wall_distance[1]:
            self.enemy_tank_acceleration = self.enemy_tank_movement

        # Tank Motion Loop
        while self.enemy_motion:

            # Tank Motion
            if time.time() <= self.enemy_moving_time:

                # Left Motion
                if self.enemy_tank_acceleration < 0:
                    if (self.enemy_tank_x_y_position[0] + self.enemy_tank_acceleration) <= (self.enemy_tank_right_left_boundary[1] + 50):
                        self.enemy_tank_acceleration = 0
                    else:
                        self.enemy_tank_x_y_position[0] += self.enemy_tank_acceleration
                        if self.enemy_tank_acceleration != 0:
                            pygame.mixer.Sound.play(self.tank_sound)

                # Right Motion
                elif self.enemy_tank_acceleration > 0:
                    if (self.enemy_tank_x_y_position[0] + self.tank_length_height[0] + self.enemy_tank_acceleration) >= self.enemy_tank_right_left_boundary[0]:
                        self.enemy_tank_acceleration = 0
                    else:
                        self.enemy_tank_x_y_position[0] += self.enemy_tank_acceleration
                        if self.enemy_tank_acceleration != 0:
                            pygame.mixer.Sound.play(self.tank_sound)

            # Screen Drawing
            self.game_display.fill(self.sky_blue)
            self.game_display.blit(self.my_tank, (self.my_tank_x_y_position[0], self.my_tank_x_y_position[1]))
            self.game_display.blit(self.enemy_tank, (self.enemy_tank_x_y_position[0], self.enemy_tank_x_y_position[1]))
            Messages.message_to_screen(self, self.my_health_percentage, self.black, "Small", -350, 10, 'No')
            Messages.message_to_screen(self, self.enemy_health_percentage, self.black, "Small", -350, self.res[0] - 75, 'No')
            pygame.draw.line(self.game_display, self.blue, self.my_health_bar[0], self.my_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.red, self.enemy_health_bar[0], self.enemy_health_bar[1], 20)
            pygame.draw.line(self.game_display, self.grey, self.ground_starting_ending_point[0], self.ground_starting_ending_point[1], self.ground_length_height[1])
            pygame.draw.line(self.game_display, self.grey, self.wall_starting_ending_point[0], self.wall_starting_ending_point[1], self.wall_length_height[1])

            # Handling Loop Break After Tank Moving Time Duration And Setting Enemy Shell Position
            if time.time() >= self.enemy_moving_time:
                self.enemy_tank_acceleration = 0
                self.enemy_shell_position = [self.enemy_tank_x_y_position[0], self.my_tank_x_y_position[1] + 3]
                Tank_Shot.enemy_shot(self)
                self.enemy_shoot = True
                self.enemy_motion = False

            # Event Handling
            for event in pygame.event.get():

                # Close Window Event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Key Down Event
                elif event.type == pygame.KEYDOWN:

                    # For Game Pause
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        Main_Screen.game_paused(self)
                        self.game_pause = True

            pygame.display.update()
            self.clock.tick(self.FPS)


class Messages(Main_Screen):

    # For Text Size
    def get_message(self, msg, color, size):

        if size == 'Small':
            self.text_surface = self.small_font.render(msg, True, color)
        elif size == 'Medium':
            self.text_surface = self.medium_font.render(msg, True, color)
        elif size == 'Large':
            self.text_surface = self.large_font.render(msg, True, color)

        return self.text_surface, self.text_surface.get_rect()

    # For Text Centering
    def message_to_screen(self, msg, color, size, y_displace, x_displace, center):

        self.text_surf, self.text_rect = Messages.get_message(self, msg, color, size)
        if center == 'Yes':
            self.text_rect.center = ((self.res[0] / 2) + x_displace, (self.res[1] / 2) + y_displace)
        elif center == 'No':
            self.text_rect = (x_displace, (self.res[1] / 2) + y_displace)
        self.game_display.blit(self.text_surf, self.text_rect)


game = Main_Screen()
