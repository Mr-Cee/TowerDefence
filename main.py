import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as c


# Initialize pygame
pg.init()

# Create clock
clock = pg.time.Clock()

# Create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Load images
    #map
map_image = pg.image.load('levels/level.png').convert_alpha()
    #Individual turret for mouse cursor
cursor_target = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
    #enemies
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

# Load JSON data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)

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
            new_turret = Turret(cursor_target, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

# Create World
world = World(world_data, map_image)
world.process_data()

# Create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)



# Game Loop
run =True
while run:

    clock.tick(c.FPS)

    screen.fill('grey100')

    # Draw level
    world.draw(screen)

    #Draw Enemy Path
    pg.draw.lines(screen, "grey0", False, world.waypoints)

    # Update groups
    enemy_group.update()

    # Draw groups
    enemy_group.draw(screen)
    turret_group.draw(screen)

    pg.display.update()

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
                create_turret(mouse_pos)




pg.quit()
