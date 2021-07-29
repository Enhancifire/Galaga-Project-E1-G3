import pygame
import os
import random
import time

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#---------------------------------------------Ankush--------------------------------#
pygame.mixer.music.load(os.path.join("Assets", "Bloodytears.wav"))
pygame.mixer.music.play(-1)

#---------------------------------------------Faiz--------------------------------#
# Loading the Images
# Enemy Ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("Assets",'pixel_ship_red_small_ro.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("Assets",'pixel_ship_blue_small_ro.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("Assets",'pixel_ship_green_small_ro.png'))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("Assets",'pixel_ship_yellow.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space-bkg.png")), (WIDTH, HEIGHT))

# Lasers
RED_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_yellow.png"))
#---------------------Parag-------------------------#
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)

#-------------------------------Rohan and Parag-----------------------------------#
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
            return self.ship_img.get_height()

#-------------------------------------------------Rohan------------------------------------------------------#
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else: 
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height()+ 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height()+ 10, self.ship_img.get_width()*(self.health/self.max_health), 10))

#-----------------------------------------------Parag------------------------#
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color,health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offest_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offest_y)) != None

#------------------------Faiz--------------------------#
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    lost = False
    lost_count = 0
    player_laser_vel = 15
    enemy_laser_vel = 5
    laserstate = 0
    lasers_count = 1

    main_font = pygame.font.SysFont("Ubuntu Mono", 50)
    lost_font = pygame.font.SysFont("Roboto Bold", 70)

    clock = pygame.time.Clock()

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5

    player = Player(300, 630)

    def redraw_window():
        WIN.blit(BG, (0,0))
        # Draw text
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH -level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
 
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH//2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5

            for i in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
        #------------------------Rohan-------------------------------------------------------#
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #Left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: #Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: #Down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            if lasers_count == 1:
                player.shoot()
            elif lasers_count == 3:
                player.shoot()
                player.shoot()
                player.shoot()

        #----------- CHEATS SECTION (For the Filthy Cheater) ---------------------------------------------#

        #------------------------Arshad------------------------------------------------------#
        if keys[pygame.K_e]:  # Increase player velocity using E
            player_vel += 10
        if keys[pygame.K_q] and player_vel > 5: # Decrease player velocity using Q
            player_vel -= 10
        if keys[pygame.K_f]:# Increase laser velocity using F
            player_laser_vel = 70
        if keys[pygame.K_r]:# Decrease laser velocity using R
            player_laser_vel = 15
        if keys[pygame.K_c]:# Increase laser count using C (Currently not working)
            if laserstate == 0:
                laserstate = 1
                lasers_count = 3
            elif laserstate == 1:
                laserstate = 0
                lasers_count = 3
        if keys[pygame.K_m] and player.health < 80: # Increase player health to max using M
            player.health = 100

        #----------- CHEATS SECTION END ---------------------------------------------------------------#


        #----------------------------------Parag--------------------------------------------------------#
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 4*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            
        
        player.move_lasers(-player_laser_vel, enemies)


#-----------------------------------Ankush---------------------------------------------------------------------#
def menu():

    # define the RGB value for white,
    #  green, blue colour .
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    black =(0,0,0)

    # assigning values to X and Y variable
    X = WIDTH
    Y = HEIGHT

    # create the display surface object
    # of specific dimension..e(X, Y).
    display_surface = pygame.display.set_mode((X, Y))

    # set the pygame window name
    pygame.display.set_caption('GALAGA PROJECT')
    image = pygame.image.load(os.path.join("Assets", "galaga_logo.png"))


    main_font = pygame.font.SysFont("Ubuntu Mono", 100)

    # create a text surface object,
    # on which text is drawn on it.
    start_text = main_font.render("Start Game", 3, (255, 255, 255))

    


    while True:

        # completely fill the surface object
        # with white color
        display_surface.fill(white)

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        display_surface.blit(BG, (0,0))
        display_surface.blit(start_text, ((X//2) - (start_text.get_width()//2), Y//2))
        display_surface.blit(image, ((WIDTH//2 - image.get_width()//2), (HEIGHT//6) ))
        


        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

        # Draws the surface object to the screen.
            pygame.display.update()
            display_surface.blit(start_text, ((X//2) - (start_text.get_width()//2), Y//2))
            pygame.display.update()

menu()
