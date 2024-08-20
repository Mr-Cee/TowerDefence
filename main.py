import pygame as pg
import json
from enemy import Enemy
import constants as c
from world import World

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
    #enemies
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

# Load JSON data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)


# Create World
world = World(world_data, map_image)
world.process_data()

# Create groups
enemy_group = pg.sprite.Group()

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

    pg.display.update()

    # Event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False

pg.quit()
