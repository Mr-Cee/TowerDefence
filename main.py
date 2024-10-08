import pygame as pg
import json

################################
#### 2:53#################

from constants import TURRET_LEVELS
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c


# Initialize pygame
pg.init()

# Create clock
clock = pg.time.Clock()

# Create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

#Game Variables
game_over = False
game_outcome = 0 # -1 is loss and 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

# Load images
    #map
map_image = pg.image.load('levels/level.png').convert_alpha()
    #Turret Sprite Sheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'assets/images/turrets/turret_{x}.png.').convert_alpha()
    turret_spritesheets.append(turret_sheet)
    #Individual turret for mouse cursor
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
    #enemies
enemy_images = {
    "weak": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    "medium": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    "strong": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
}

    #Buttons
buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
    #GUI
heart_image = pg.image.load('assets/images/gui/heart.png').convert_alpha()
coin_image = pg.image.load('assets/images/gui/coin.png').convert_alpha()
logo_image = pg.image.load('assets/images/gui/logo.png').convert_alpha()

# Load JSON data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)

# Load fonts for display
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    # Draw Panel
    pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    screen.blit(logo_image, (c.SCREEN_WIDTH, 400))
    # Draw Text
    draw_text("LEVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70)



def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #Calculate the sequential number of tiles
    mouse_tile_number = (mouse_tile_y * c.COLS) + mouse_tile_x
    #Check if that tile is grass
    if world.tile_map[mouse_tile_number] == 7:
        #Check that there isn't already a turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        #if it is free space, place turret
        if space_is_free == True:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)
            world.money -= c.BUY_COST

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

# Create World
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_turret_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 50, 300, fast_forward_image, False)


# Game Loop
run =True
while run:

    clock.tick(c.FPS)
############################################################

##############################
    # UPDATING SECTION #
##############################

    if not game_over:
        # check if player has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1 #lost game
        # Check if player has won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1  # won game


        # Update groups
        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        #highlight selected turret
        if selected_turret:
            selected_turret.selected = True

##############################
    # DRAWING SECTION #
##############################
    # Draw level
    world.draw(screen)

    #Draw Enemy Path
    # pg.draw.lines(screen, "grey0", False, world.waypoints)

    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    display_data()




    if not game_over:

        #check if the level has been started
        if not level_started:
            if begin_button.draw(screen):
                level_started = True
        else:
            # Fast forward button
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 2
            # Spawn Enemies
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        # Check if the wave has been finished
        if world.check_level_complete():
            world.level += 1
            if world.level >= c.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1  # won game
            else:
                world.money += c.LEVEL_COMPLETE_REWARD
                level_started = False
                last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_enemies()

        #Draw Buttons
        #button for placing turrets
        # for the turret button, show cost of button and draw button
        draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))
        if turret_button.draw(screen):
            placing_turrets = True
        #if placing turrets then show the cancel button as well
        if placing_turrets:
            #Show cursor turret
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] < c.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            #button for cancel
            if cancel_button.draw(screen):
                placing_turrets = False
        #if a turret is selected, show the upgrade button
        if selected_turret:
            #if a turret can be upgraded, then show the upgrade button
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                draw_text(str(selected_turret.upgrade_cost), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
                screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
                if upgrade_turret_button.draw(screen):
                    print(selected_turret.upgrade_cost)
                    if world.money >= selected_turret.upgrade_cost:
                        world.money -= selected_turret.upgrade_cost
                        selected_turret.upgrade()
    else:
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("YOU WIN", large_font, "grey0", 315, 230)        # Restart Level
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            #empty groups
            enemy_group.empty()
            turret_group.empty()


    # Event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #Mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Check if mouse is in the game area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                #clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    #check if ther eis neough money for a turret
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                        placing_turrets = False
                    else:
                        placing_turrets = False

                else:
                    selected_turret = select_turret(mouse_pos)


    #Update the display
    pg.display.update()



pg.quit()
