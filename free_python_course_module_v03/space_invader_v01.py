import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_INITIAL_SPEED = 0.1
ENEMY_SPEED_INCREMENT = 0.01  # Increase in enemy speed per level
NUM_ENEMIES = 5  # Number of enemies to start with

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Player
player_img = pygame.image.load("player.png")
player_x = SCREEN_WIDTH // 2 - 32
player_y = SCREEN_HEIGHT - 64
player_x_change = 0

# Enemies
enemy_imgs = [pygame.image.load("enemy.png") for _ in range(NUM_ENEMIES)]
enemy_x = [random.randint(0, SCREEN_WIDTH - 64) for _ in range(NUM_ENEMIES)]
enemy_y = [random.randint(50, 150) for _ in range(NUM_ENEMIES)]
enemy_x_change = [ENEMY_INITIAL_SPEED] * NUM_ENEMIES
enemy_y_change = [40] * NUM_ENEMIES

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = SCREEN_HEIGHT - 64
bullet_y_change = 10
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Game Over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


# Functions
def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_imgs[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    if distance < 27:
        return True
    return False


# Game Loop
running = True
level = 1  # Initialize game level

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player_x_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - 64:
        player_x = SCREEN_WIDTH - 64

    for i in range(len(enemy_imgs)):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] < 0:
            enemy_x_change[i] = ENEMY_INITIAL_SPEED + (level - 1) * ENEMY_SPEED_INCREMENT
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] > SCREEN_WIDTH - 64:
            enemy_x_change[i] = -ENEMY_INITIAL_SPEED - (level - 1) * ENEMY_SPEED_INCREMENT
            enemy_y[i] += enemy_y_change[i]

        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = SCREEN_HEIGHT - 64
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = SCREEN_HEIGHT - 64
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)

    # Display Score
    score_text = font.render("Score: " + str(score), True, GREEN)
    screen.blit(score_text, (text_x, text_y))

    # Check for game over
    for i in range(len(enemy_imgs)):
        if enemy_y[i] > SCREEN_HEIGHT - 64:
            game_over_text = game_over_font.render("GAME OVER", True, GREEN)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 32))
            pygame.display.update()
            pygame.time.delay(2000)  # Delay for 2 seconds
            sys.exit()  # Exit the game

    # Check for level up
    if score >= level * 10:
        level += 1
        # Increase enemy speed and add more enemies
        for i in range(len(enemy_imgs)):
            enemy_x_change[i] += ENEMY_SPEED_INCREMENT
        NUM_ENEMIES += 1
        enemy_imgs.append(pygame.image.load("enemy.png"))
        enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(ENEMY_INITIAL_SPEED + (level - 1) * ENEMY_SPEED_INCREMENT)
        enemy_y_change.append(40)

    pygame.display.update()

# Quit the game
pygame.quit()
