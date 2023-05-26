import pygame
import random
from pygame.sprite import Group, spritecollide
from game_object import GameObject
from text import Text
from maze import calculate_walls_coordinates, calculate_block_coordinates
from typing import Any


class Player(GameObject):
    sprite_filename = "player"


class Enemy(GameObject):
    sprite_filename = "sprite_filename"


class Slime1(Enemy):
    sprite_filename = "slime1"


class Slime2(Enemy):
    sprite_filename = "slime2"


class Slime3(Enemy):
    sprite_filename = "slime3"


class Wall(GameObject):
    sprite_filename = "wall"


def compose_context(screen: Any) -> dict:
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    block_coordinates = calculate_block_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    return {
        "player": Player(screen.get_width() // 10, screen.get_height() // 2),
        "slime1": Slime1(screen.get_width() // 3, screen.get_height() // 10),
        "slime2": Slime2(600, 400),
        "slime3": Slime3(300, 550),
        "walls": Group(*[Wall(x, y) for (x, y) in walls_coordinates], [Wall(x, y) for (x, y) in block_coordinates]),
        "message": ""
    }


def draw_whole_screen(screen: Any, context: dict) -> None:
    screen.fill("gray")
    context["player"].draw(screen)
    context["slime1"].draw(screen)
    context["slime2"].draw(screen)
    context["slime3"].draw(screen)
    context["walls"].draw(screen)
    Text(context["message"], (screen.get_width() // 3, screen.get_height() // 2)).draw(screen)


def players_movement(player_speed: int, context: dict) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        context["player"].rect = context["player"].rect.move(0, -1 * player_speed)
    if keys[pygame.K_s]:
        context["player"].rect = context["player"].rect.move(0, player_speed)
    if keys[pygame.K_a]:
        context["player"].rect = context["player"].rect.move(-1 * player_speed, 0)
    if keys[pygame.K_d]:
        context["player"].rect = context["player"].rect.move(player_speed, 0)


def set_vector() -> str:
    vectors = ['up', 'down', 'left', 'right']
    vector = random.choice(vectors)
    return vector


def change_vector(enemy, enemy_vectors) -> str:
    vectors = ['up', 'down', 'left', 'right']
    vector = enemy_vectors[enemy]
    vectors.remove(vector)
    vector = random.choice(vectors)
    return vector


def create_enemies_vectors(enemies: list) -> dict:
    enemy_vectors = {}
    for enemy in enemies:
        vector = set_vector()
        enemy_vectors[enemy] = vector
    return enemy_vectors


def enemy_movement(enemy_speed: int, enemy: str, enemy_vectors: dict, context: dict) -> None:
    if enemy_vectors[enemy] == "down":
        context[enemy].rect = context[enemy].rect.move(0, enemy_speed)
    if enemy_vectors[enemy] == "left":
        context[enemy].rect = context[enemy].rect.move(-1*enemy_speed, 0)
    if enemy_vectors[enemy] == "right":
        context[enemy].rect = context[enemy].rect.move(enemy_speed, 0)
    if enemy_vectors[enemy] == "up":
        context[enemy].rect = context[enemy].rect.move(0, -1*enemy_speed)


def check_game_over(context: dict, screen: Any, enemy: str) -> None:
    if context[enemy].is_collided_with(context["player"]):
        context["player"].rect.topleft = (screen.get_width(), screen.get_height())
        context['slime1'].rect.topleft = (screen.get_width(), screen.get_height())
        context['slime2'].rect.topleft = (screen.get_width(), screen.get_height())
        context['slime3'].rect.topleft = (screen.get_width(), screen.get_height())
        context["message"] = "GAME OVER"


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((840, 680))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5
    enemy_speed = 1
    enemies = ["slime1", "slime2", "slime3"]

    context = compose_context(screen)

    enemy_vectors = create_enemies_vectors(enemies)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if enemy_speed > player_speed:
            enemy_speed = player_speed

        draw_whole_screen(screen, context)

        pygame.display.flip()

        old_player_topleft = context["player"].rect.topleft
        players_movement(player_speed, context)
        if spritecollide(context["player"], context["walls"], dokill=False):
            context["player"].rect.topleft = old_player_topleft

        for enemy in enemies:
            old_enemy_topleft = context[enemy].rect.topleft
            enemy_movement(enemy_speed, enemy, enemy_vectors, context)
            if spritecollide(context[enemy], context["walls"], dokill=False):
                context[enemy].rect.topleft = old_enemy_topleft
                enemy_vectors[enemy] = change_vector(enemy, enemy_vectors)
                enemy_speed += 0.1
            check_game_over(context, screen, enemy)

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":

    main()
