
# Modules needed
import pgzrun
import random

# Screen size
WIDTH = 1000
HEIGHT = 600
SCOREBOARD_HEIGHT = 80

# Stating images and variables

BACKGROUND_TITLE = "background_logo"
BACKGROUND_LEVEL1 = "level1"
BACKGROUND_LEVEL2 = "level2"
BACKGROUND_LEVEL3 = "level3"


BACKGROUND_IMG = BACKGROUND_TITLE
PLAYER_IMG = "player_ship"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"

start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)

instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

# Counter Variables
score = 0
junk_speed = 5
satellite_speed = 3
debris_speed = 2
level = 0
level_screen = 0
junk_collect = 0
lvl2_LIMIT = 5
lvl3_LIMIT = 10

def on_mouse_down(pos):
    global level, level_screen

    # check start button
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1
        print("Start button pressed")


    # check start button
    if instructions_button.collidepoint(pos):
        level = -1
        level_screen = -1
        print("instructions pressed")


def init():
    global player, junks, satellite, debris, lasers
    # Initializing spaceship
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH-15, HEIGHT/2)

    # Initializing junks
    junks = []

    for i in range(5):
        junk = Actor(JUNK_IMG)
        x_pos = random.randint(-800, -50)
        y_pos = random.randint(SCOREBOARD_HEIGHT, HEIGHT - junk.height)
        junk.topleft = (x_pos, y_pos)
        junks.append(junk)

    # Initializing satellite
    satellite = Actor(SATELLITE_IMG)
    x_sat = random.randint(-500, -50)
    y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)

    # Initializing debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500,-50)
    y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

    lasers = []

    # Background music
    music.play("spacelife")


init()



# Opens screen with images
def draw():
    # Draws player
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))

    if level == 0:
        start_button.draw()
        instructions_button.draw()

    if level == -1:
        start_button.draw()

    if level >= 1:
        player.draw()
        for junk in junks:
            junk.draw()
    if level >= 2:
        satellite.draw()
    if level == 3:
        debris.draw()
        for laser in lasers:
            laser.draw()
            
    # Displays the score
    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(828,20), fontsize=35, color='black')
    show_junk_collect = "Junk: " + str(junk_collect)
    screen.draw.text(show_junk_collect, topleft=(450,15), fontsize=35, color='black')

    if level == -1: # instructions screen
        start_button.draw()
        show_instructions = "Use UP/DOWN arrow keys or W/S keys to move your player\n\npress SPACEBAR to shoot"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 250), fontsize=35, color='white')
    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_transition = "LEVEL " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_transition, center=(WIDTH/2, HEIGHT/2), fontsize=70, color='white')

# updates objects positions
def update():

    global level, level_screen, BACKGROUND_IMG, junk_collect, score
    if level == -1: # Instructions screen
        BACKGROUND_IMG = BACKGROUND_LEVEL1
        
    if junk_collect == lvl2_LIMIT:  # Level 2
        level = 2
        
    if junk_collect == lvl3_LIMIT:  # Level 3
        level = 3


    if level>=1:
        if level_screen == 1:  # Level 1 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1:
                level_screen = 2
                print("ENTER key is pressed")
        if level_screen == 2:  # Level 1 Gameplay Screen
            playerUpdate()
            junkUpdate()
            # updateLasers()

        if level == 2 and level_screen <= 3:  
            level_screen = 3  # Level 2 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            if keyboard.RETURN == 1:
                level_screen = 4
                print("ENTER key is pressed")
        if level_screen == 4:  # Level 2 Gameplay Screen
            playerUpdate()
            junkUpdate()
            satelliteUpdate()

        if level == 3 and level_screen <= 5:
            level_screen = 5  # Level 3 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            if keyboard.RETURN == 1:
                level_screen = 6
                print("ENTER key is pressed")
        if level_screen == 6:  # Level 3 Gameplay Screen
            playerUpdate()
            junkUpdate()
            satelliteUpdate()
            debrisUpdate()
            updateLasers()

    if score < 0:
        music.stop()
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            level = 0
            init()
   

def junkUpdate():
    global score, junk_speed, junk_collect
    for junk in junks:
        junk.x += junk_speed
        collision = player.colliderect(junk)
    
        if (junk.left > WIDTH or collision == 1):
        #junk_speed = random.randint(2,10)
            x_pos = -50
            y_pos = random.randint(SCOREBOARD_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)
        
        if (collision == 1):
            score += 1
            junk_collect += 1  # increase by 1 every time collision occurs
            sounds.collect_pep.play()
        

def playerUpdate():
    if (keyboard.up == 1 or keyboard.w == 1):
        player.y -= 5

    elif (keyboard.down == 1 or keyboard.s == 1):
        player.y += 5

    if (player.top < 80):
        player.top = 80
        
    if (player.bottom > HEIGHT - 5):
        player.bottom = HEIGHT - 5

    if (keyboard.space == 1) and level == 3:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

def satelliteUpdate():
    global score, satellite_speed
    satellite.x += satellite_speed
    collision = player.colliderect(satellite)

    if (satellite.left > WIDTH or collision == 1):
        x_sat = random.randint(-500, -50)
        y_sat = random.randint (SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if (collision == 1):
        score -= 10
        sounds.collect_pep.play()

def debrisUpdate():
    global score, debris_speed
    debris.x += debris_speed
    collision = player.colliderect(debris)

    if (debris.left > WIDTH or collision==1):
        x_deb = random.randint(-500,-50)
        y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if (collision == 1):
        score -= 5
        sounds.collect_pep.play()

LASER_SPEED = -5
def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        collision_sat = satellite.colliderect(laser)
        collision_deb = debris.colliderect(laser)

        if laser.right < 0:
            lasers.remove(laser)

        # checking for collision with satellite
        if collision_sat == 1:
            x_sat = random.randint(-500,-50)
            y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score -= 5
            sounds.explosion.play()

        # checking for collision with debris
        if collision_deb == 1:
            x_deb = random.randint(-500,-50)
            y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5


        

player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list
    



# Finsihes Code
pgzrun.go()
