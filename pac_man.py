from pygame.sprite import Group, spritecollide
import pygame
from game_object import GameObject
from text import Text
import random
from random import randint


class Player(GameObject):
    sprite_filename = "player"


class Enemy(GameObject):
    sprite_filename = "sprite_filename"


class Slime(Enemy):
    sprite_filename = "slime1"


class Wall(GameObject):
    sprite_filename = "wall"


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_block_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
            ])
    for block_num in range(1, vertical_wall_block_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
            ])


    return walls_coordinates


def calculate_block_coordinates_4_2(screen_width, screen_height, wall_block_width, wall_block_height, 
                                    horizontal_number=4, vertical_number=4):
    block_coordinates = []

    for block_horizontal_num in range(horizontal_number - 1, horizontal_number + 2):
        block_coordinates.extend([
            (block_horizontal_num * wall_block_width, wall_block_height * 4),
            (block_horizontal_num * wall_block_width, wall_block_height * 12),
            (screen_width - block_horizontal_num * wall_block_width - wall_block_width, wall_block_height * 4),
            (screen_width - block_horizontal_num * wall_block_width - wall_block_width * 7, wall_block_height * 8),
            (screen_width - block_horizontal_num * wall_block_width - wall_block_width, wall_block_height * 12),
            ])
        
    for block_vertical_num in range(vertical_number - 2, vertical_number + 2):
        block_coordinates.extend([

            (wall_block_width * 2, block_vertical_num * wall_block_height),
            (wall_block_width * 10, block_vertical_num * wall_block_height),
            (screen_width - wall_block_width * 2 - wall_block_width, block_vertical_num * wall_block_height),
            (wall_block_width * 2, screen_height - block_vertical_num * wall_block_height - wall_block_width ),
            (wall_block_width * 10, screen_height- block_vertical_num * wall_block_height - wall_block_width),
            (screen_width - wall_block_width * 2 - wall_block_width, screen_height - block_vertical_num * wall_block_height - wall_block_width)
            ])

    return block_coordinates


def compose_context(screen):
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    block_coordinates = calculate_block_coordinates_4_2(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    return {
        "player": Player(screen.get_width() // 10, screen.get_height() // 2),
        "slim1": Slime(screen.get_width() // 3, screen.get_height() // 10),
        "walls": Group(*[Wall(x, y) for (x, y) in walls_coordinates], [Wall(x, y) for (x, y) in block_coordinates]),
        "message": ""
    }

def draw_whole_screen(screen, context):
    screen.fill("gray")
    context["player"].draw(screen)
    context["slim1"].draw(screen)
    context["walls"].draw(screen)
    Text(context["message"], (screen.get_width() // 3, screen.get_height() // 2)).draw(screen)

def draw_game_over(screen):
    #не работает
    Text("GAME OVER", (screen.get_width() // 2, screen.get_height() // 2)).draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((840, 680))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5
    enemy_speed = 2

    context = compose_context(screen)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if enemy_speed < player_speed * 2:
            enemy_speed = enemy_speed * 1
        else: 
            enemy_speed = enemy_speed
        
        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft
        if keys[pygame.K_w]:
            context["player"].rect = context["player"].rect.move(0, -1 * player_speed)
        if keys[pygame.K_s]:
            context["player"].rect = context["player"].rect.move(0, player_speed)
        if keys[pygame.K_a]:
            context["player"].rect = context["player"].rect.move(-1 * player_speed, 0)
        if keys[pygame.K_d]:
            context["player"].rect = context["player"].rect.move(player_speed, 0)

        if spritecollide(context["player"], context["walls"], dokill=False):
            context["player"].rect.topleft = old_player_topleft
            draw_game_over(screen)


        old_slim_1_topleft = context["slim1"].rect.topleft

        slim_coord = randint(1, 4)
        if slim_coord == 1:
            context["slim1"].rect = context["slim1"].rect.move(0, enemy_speed)
        if slim_coord == 2:
            context["slim1"].rect = context["slim1"].rect.move(-1*enemy_speed, 0)
        if slim_coord == 3:
            context["slim1"].rect = context["slim1"].rect.move(enemy_speed, 0)
        if slim_coord == 4:
            context["slim1"].rect = context["slim1"].rect.move(0, -1*enemy_speed)
        
        
        if spritecollide(context["slim1"], context["walls"], dokill=False):
            context["slim1"].rect.topleft = old_slim_1_topleft

        if context["slim1"].is_collided_with(context["player"]):
            context["player"].rect.topleft = (screen.get_width(), screen.get_height())
            context["slim1"].rect.topleft = (screen.get_width(), screen.get_height())
            context["message"] = "GAME OVER"

#            running is False


        clock.tick(60) / 1000


    pygame.quit()


if __name__ == "__main__":
    main()