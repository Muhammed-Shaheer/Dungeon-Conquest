import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Conquest")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# States
MENU = "MENU"
PLAYING = "PLAYING"
GAME_OVER = "GAME_OVER"
VICTORY = "VICTORY"
game_state = MENU

# Buttons
swordsman_button = pygame.Rect(250, 220, 300, 60)
thief_button = pygame.Rect(250, 320, 300, 60)

# Map
game_map = [
    "####################",
    "#..................#",
    "#..................#",
    "#....######........#",
    "#..................#",
    "#..............#...#",
    "#..................#",
    "#..................#",
    "####################"
]

# Player
player_x = 80
player_y = 80
player_size = 30
player_speed = 4
player_hp = 100
player_class = None

# Slime
slimes = [
    {"x": 450, "y": 120, "hp": 50, "color": (255, 0, 0), "name": "Fire"},
    {"x": 600, "y": 120, "hp": 50, "color": (0, 0, 255), "name": "Water"},
    {"x": 450, "y": 240, "hp": 50, "color": (139, 69, 19), "name": "Mud"},
    {"x": 600, "y": 240, "hp": 50, "color": (0, 255, 255), "name": "Ice"}
]
slime_size = 30
slime_speed = 2
# Hidden Trap
trap_x = 320
trap_y = 240
trap_size = 30

trap_triggered = False
trap_disarmed = False
boss_room = pygame.Rect(700, 250, 50, 50)

boss_active = False
boss_defeated = False
king_slime = {
    "x": 650,
    "y": 250,
    "hp": 200,
    "size": 60
}
def get_wall_rects():
    walls = []

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if tile == "#":
                walls.append(
                    pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                )

    return walls


running = True

while running:

    clock.tick(60)

    # MENU
    if game_state == MENU:

        screen.fill((20, 20, 20))

        title = font.render(
            "DUNGEON CONQUEST",
            True,
            (255, 255, 255)
        )

        screen.blit(title, (220, 120))

        pygame.draw.rect(screen, (0, 100, 255), swordsman_button)
        pygame.draw.rect(screen, (0, 180, 0), thief_button)

        sword_text = font.render(
            "SWORDSMAN",
            True,
            (255, 255, 255)
        )

        thief_text = font.render(
            "THIEF",
            True,
            (255, 255, 255)
        )

        screen.blit(sword_text, (310, 235))
        screen.blit(thief_text, (360, 335))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()

                if swordsman_button.collidepoint(mouse_pos):
                    player_class = "Swordsman"
                    player_hp = 100
                    player_speed = 4
                    game_state = PLAYING

                elif thief_button.collidepoint(mouse_pos):
                    player_class = "Thief"
                    player_hp = 80
                    player_speed = 6
                    game_state = PLAYING

        pygame.display.update()
        continue

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                attack_rect = pygame.Rect(
                    player_x - 20,
                    player_y - 20,
                    player_size + 40,
                    player_size + 40
                )

                for slime in slimes:
                    if boss_active and king_slime["hp"] > 0:

                        king_rect = pygame.Rect(
                            king_slime["x"],
                            king_slime["y"],
                            king_slime["size"],
                            king_slime["size"]
                        )

                        if attack_rect.colliderect(king_rect):
                            king_slime["hp"] -= 10                    
                    slime_rect = pygame.Rect(
                        slime["x"],
                        slime["y"],
                        slime_size,
                        slime_size
                    )

                    if slime["hp"] > 0 and attack_rect.colliderect(slime_rect):
                        slime["hp"] -= 10

    walls = get_wall_rects()

    keys = pygame.key.get_pressed()
    if player_class == "Thief":

        if keys[pygame.K_f]:

            dx = player_x - trap_x
            dy = player_y - trap_y

            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < 60:
                trap_disarmed = True
    new_x = player_x
    new_y = player_y

    if keys[pygame.K_w]:
        new_y -= player_speed

    if keys[pygame.K_s]:
        new_y += player_speed

    if keys[pygame.K_a]:
        new_x -= player_speed

    if keys[pygame.K_d]:
        new_x += player_speed

    player_rect = pygame.Rect(
        new_x,
        new_y,
        player_size,
        player_size
    )
    if boss_room.colliderect(player_rect):
        boss_active = True
        print("Boss Activated")
    # Trap Collision
    trap_rect = pygame.Rect(
        trap_x,
        trap_y,
        trap_size,
        trap_size
    )

    if(not trap_triggered and not trap_disarmed and player_rect.colliderect(trap_rect)):
        player_hp -= 25
        trap_triggered = True    

    blocked = False

    for wall in walls:
        if player_rect.colliderect(wall):
            blocked = True
            break

    if not blocked:
        player_x = new_x
        player_y = new_y

    # Slime AI

    for slime in slimes:
        if slime["hp"] <= 0:
            continue
        dx = player_x - slime["x"]
        dy = player_y - slime["y"]

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 200 and distance > 0:

            new_slime_x = slime["x"] + slime_speed * dx / distance
            new_slime_y = slime["y"] + slime_speed * dy / distance

            slime_rect_test = pygame.Rect(
                new_slime_x,
                new_slime_y,
                slime_size,
                slime_size
            )

            slime_blocked = False

            for wall in walls:
                if slime_rect_test.colliderect(wall):
                    slime_blocked = True
                    break

            if not slime_blocked:
                slime["x"] = new_slime_x
                slime["y"] = new_slime_y

            slime_rect = pygame.Rect(
                slime["x"],
                slime["y"],
                slime_size,
                slime_size
            )

            if player_rect.colliderect(slime_rect):
                player_hp -= 0.1

    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_size,
        player_size
    )
    if boss_active and king_slime["hp"] > 0:

        dx = player_x - king_slime["x"]
        dy = player_y - king_slime["y"]

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:

            # X movement
            new_king_x = king_slime["x"] + 1.5 * dx / distance

            king_rect_x = pygame.Rect(
                new_king_x,
                king_slime["y"],
                king_slime["size"],
                king_slime["size"]
            )

            blocked_x = False

            for wall in walls:
                if king_rect_x.colliderect(wall):
                    blocked_x = True
                    break

            if not blocked_x:
                king_slime["x"] = new_king_x

            # Y movement
            new_king_y = king_slime["y"] + 1.5 * dy / distance

            king_rect_y = pygame.Rect(
                king_slime["x"],
                new_king_y,
                king_slime["size"],
                king_slime["size"]
            )

            blocked_y = False

            for wall in walls:
                if king_rect_y.colliderect(wall):
                    blocked_y = True
                    break

            if not blocked_y:
                king_slime["y"] = new_king_y

        king_rect = pygame.Rect(
            king_slime["x"],
            king_slime["y"],
            king_slime["size"],
            king_slime["size"]
        )

        if player_rect.colliderect(king_rect):
            player_hp -= 0.2

    if player_hp <= 0:
        game_state = GAME_OVER
    if (boss_active and king_slime["hp"] <= 0 and not boss_defeated):
        boss_defeated = True
        game_state = VICTORY
    # GAME OVER
    if game_state == GAME_OVER:

        screen.fill((0, 0, 0))

        text = font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        screen.blit(text, (300, 280))

        pygame.display.update()
        continue
    #victory
    if game_state == VICTORY:

        screen.fill((0, 0, 0))

        text = font.render(
            "FLOOR 1 CLEARED",
            True,
            (0, 255, 0)
        )

        screen.blit(text, (250, 280))

        pygame.display.update()
        continue
    # DRAW
    screen.fill((20, 20, 20))
    
    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)
    pygame.draw.rect(screen,(255, 255, 0),boss_room)
    
    pygame.draw.rect(
        screen,
        (0, 120, 255),
        (player_x, player_y, player_size, player_size)
    )

    for slime in slimes:
        if slime["hp"] > 0:
            pygame.draw.rect(
            screen,
            slime["color"],
            (
                slime["x"],
                slime["y"],
                slime_size,
                slime_size
            )
            )
        if boss_active and king_slime["hp"] > 0:

            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (
                    king_slime["x"],
                    king_slime["y"],
                    king_slime["size"],
                    king_slime["size"]
                )
            )

    hp_text = font.render(
        f"HP: {int(player_hp)}",
        True,
        (255, 255, 255)
    )

    class_text = font.render(
        f"Class: {player_class}",
        True,
        (255, 255, 255)
    )
        # Thief Trap Detection
    if (player_class == "Thief" and not trap_triggered and not trap_disarmed):
        dx = player_x - trap_x
        dy = player_y - trap_y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 100:

            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (trap_x, trap_y, trap_size, trap_size)
            )
    if trap_disarmed:
        pygame.draw.rect(
        screen,
        (0, 255, 0),
        (trap_x, trap_y, trap_size, trap_size)
    )

    screen.blit(hp_text, (10, 10))
    screen.blit(class_text, (10, 40))

    pygame.display.update()

pygame.quit()
sys.exit()