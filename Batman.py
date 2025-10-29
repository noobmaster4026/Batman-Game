import random
import math
import pygame
import sys
import os

# ✅ Helper to load files both during development and after PyInstaller build
def resource_path(relative_path):
    """Get absolute path to resource (works for dev and PyInstaller EXE)"""
    try:
        base_path = sys._MEIPASS  # when running from PyInstaller bundle
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
utilityBelt = []  # list of batarangs
batarangYChange = 4.0
score = 0
health = 5
gameStatus = False  # False = playing, True = game over
familyActive = None
familyTimer = 0

# Font setup
font = pygame.font.Font(resource_path("BADABB__.ttf"), 40)

# Music
pygame.mixer.music.load(resource_path("batman_the_animated.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Batman")
icon = pygame.image.load(resource_path("halloween(1).png"))
pygame.display.set_icon(icon)

# Load images
batmanImg = pygame.image.load(resource_path("Batman.png"))
batarangImg = pygame.image.load(resource_path("Batarang.png"))
background = pygame.transform.scale(pygame.image.load(resource_path("Background.png")), (800, 600))

enemyImgs = [
    pygame.image.load(resource_path(n)) for n in [
        "Bane.png", "Black Mask.png", "Blight.png", "Catwoman.png", "Clayface.png",
        "ClockKing.png", "Creeper.png", "Deadshot.png", "Deathstroke.png", "Falconi.png",
        "Firefly.png", "HarleyQuinn.png", "HugoStrange.png", "Hush.png", "Joker.png",
        "Killer Croc.png", "MrFreeze1.png", "Penguin.png", "Phantasm.png", "PoisonIvy.png",
        "RasAlGhul.png", "SolomonGrundy.png", "TheVentriloquistandScarface.png",
        "Two-Face.png", "VictorZsasz.png"
    ]
]

batFamilyImg = {
    "Robin": pygame.image.load(resource_path("Robin.png")),
    "Batgirl": pygame.image.load(resource_path("Batgirl.png")),
    "Nightwing": pygame.image.load(resource_path("Nightwing.png")),
    "Alfred": pygame.image.load(resource_path("Alfred Pennyworth.png")),
}

# Batman position
batmanX, batmanY = 350, 400
batmanXChange, batmanYChange = 0, 0

# Enemy spawner (base_speed increases with score)
def spawn_enemy():
    base_speed = 1 + (score * 0.5)
    dir_x = random.choice([-1, 1])
    dir_y = random.choice([-1, 1])
    return {
        "img": random.choice(enemyImgs),
        "x": random.randint(20, 736),
        "y": random.randint(20, 520),
        "x_change": base_speed * dir_x,
        "y_change": base_speed * dir_y,
        "base_speed": base_speed
    }

# Initial enemy
enemies = [spawn_enemy()]

# Draw Batman
def draw_batman(x, y):
    screen.blit(batmanImg, (x, y))

# Fire batarang
def fire_batarang(x, y):
    utilityBelt.append([x + 16, y + 10])

# Collision detection
def isCollision(enemyX, enemyY, batarangX, batarangY):
    return math.hypot(enemyX - batarangX, enemyY - batarangY) < 40

# HUD
def show_score():
    shadow = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(shadow, (12, 12))
    text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(text, (10, 10))

def show_health():
    text = font.render(f"Health: {health}", True, (255, 0, 0))
    screen.blit(text, (650, 10))

# Game over
def gotham_has_fallen():
    fade_surface = pygame.Surface((800, 600))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(background, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(15)
    fallen_text = font.render("GOTHAM HAS FALLEN.....", True, (255, 0, 0))
    screen.blit(fallen_text, (100, 250))
    pygame.display.update()
    pygame.mixer.music.stop()
    pygame.time.delay(1500)

def show_game_over():
    text = font.render("Press ENTER to Restart", True, (255, 0, 0))
    screen.blit(text, (150, 300))

# Main loop
running = True
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                batmanYChange = 3.5
            elif event.key == pygame.K_UP:
                batmanYChange = -3.5
            elif event.key == pygame.K_LEFT:
                batmanXChange = -3.5
            elif event.key == pygame.K_RIGHT:
                batmanXChange = 3.5
            elif event.key == pygame.K_SPACE and not gameStatus:
                fire_batarang(batmanX, batmanY)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_DOWN, pygame.K_UP]:
                batmanYChange = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                batmanXChange = 0

    # Family summon
    if not gameStatus:
        if keys[pygame.K_r]:
            familyActive = "Robin"
            familyTimer = pygame.time.get_ticks() + 5000
        elif keys[pygame.K_b]:
            familyActive = "Batgirl"
            familyTimer = pygame.time.get_ticks() + 5000
        elif keys[pygame.K_a]:
            familyActive = "Alfred"
            familyTimer = pygame.time.get_ticks() + 5000
        elif keys[pygame.K_n]:
            familyActive = "Nightwing"
            familyTimer = pygame.time.get_ticks() + 5000

    # Batman movement
    if not gameStatus:
        batmanX += batmanXChange
        batmanY += batmanYChange
        batmanX = max(0, min(batmanX, 736))
        batmanY = max(0, min(batmanY, 536))

    # Batarang movement
    for b in utilityBelt[:]:
        b[1] -= batarangYChange
        screen.blit(batarangImg, (b[0], b[1]))
        if b[1] < -20:
            utilityBelt.remove(b)

    # Enemy logic
    if not gameStatus:
        for enemy in enemies[:]:
            current_speed = enemy["base_speed"] + (score * 0.05)
            current_speed = min(current_speed, 3.0)
            direction_x = 1 if enemy["x_change"] > 0 else -1
            direction_y = 1 if enemy["y_change"] > 0 else -1
            enemy["x_change"] = current_speed * direction_x
            enemy["y_change"] = current_speed * direction_y
            enemy["x"] += enemy["x_change"]
            enemy["y"] += enemy["y_change"]

            # Bounce off edges
            if enemy["x"] <= 20 or enemy["x"] >= 736:
                enemy["x_change"] = -enemy["x_change"]
            if enemy["y"] <= 20 or enemy["y"] >= 520:
                enemy["y_change"] = -enemy["y_change"]

            # Collision with Batman
            if math.hypot(enemy["x"] - batmanX, enemy["y"] - batmanY) < 40:
                health -= 1
                enemies.remove(enemy)
                enemies.append(spawn_enemy())

            # Collision with batarang
            for b in utilityBelt[:]:
                if isCollision(enemy["x"], enemy["y"], b[0], b[1]):
                    utilityBelt.remove(b)
                    enemies.remove(enemy)
                    score += 1
                    enemies.append(spawn_enemy())
                    break

            screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

    # Check game over
    if health <= 0 and not gameStatus:
        gotham_has_fallen()
        gameStatus = True
        utilityBelt.clear()

    # Draw Batman + family
    draw_batman(batmanX, batmanY)
    if familyActive and pygame.time.get_ticks() < familyTimer:
        fam_img = batFamilyImg.get(familyActive)
        if fam_img:
            screen.blit(fam_img, (batmanX + 60, batmanY - 40))
    else:
        familyActive = None

    show_score()
    show_health()
    if gameStatus:
        show_game_over()

    # Restart
    if keys[pygame.K_RETURN] and gameStatus:
        score = 0
        health = 5
        enemies = [spawn_enemy()]
        utilityBelt.clear()
        gameStatus = False
        pygame.mixer.music.play(-1)

    pygame.display.update()

# Quit
pygame.quit()
sys.exit()