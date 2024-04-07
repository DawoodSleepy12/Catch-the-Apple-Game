import pygame
from sys import exit
from random import randint
from math import floor

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the apple")
font = pygame.font.Font(None, 16)
clock = pygame.time.Clock()
bgColor = (0, 197, 255)
score = 0

fps = 60

class Bowl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load('images/bowl.png').convert_alpha()
        self.image = pygame.transform.scale(self.img, (90, 33))
        self.Xpos = SCREEN_WIDTH/2 - 33
        self.rect = self.image.get_rect(midbottom=(self.Xpos, 455))
        self.velocity = 10

    def player_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.move_ip(-self.velocity, 0)
        if key[pygame.K_d]:
            self.rect.move_ip(self.velocity, 0)

    def update(self):
        self.player_input()

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/apple.png').convert_alpha()
        width = self.image.get_width()
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/2 - width, -50))
        self.gravity = 2
        self.sound = pygame.mixer.Sound('sounds/sound1.wav')

    def apply_gravity(self):
        global onGame
        global bgColor
        self.rect.y += self.gravity

        if self.rect.bottom >= 580:
            gameOver()
            onGame = False

    def changePos(self):
        self.rect.x = randint(30, 760)
        self.rect.bottom = -50

    def update(self):
        global score
        self.apply_gravity()
        collision = collision_sprite()
        if collision == True:
            self.changePos()
            self.sound.play()
            self.gravity += 0.025
            score += 1

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, apple, False):
        return True
    else:
        return False

class button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        global onMenu
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

player = pygame.sprite.GroupSingle()
player.add(Bowl())

apple = pygame.sprite.GroupSingle()
apple.add(Apple())

def gameOver():
    gameOverSound = pygame.mixer.Sound('sounds/game-over.wav')
    gameOverSound.play()
    endFont = pygame.font.Font(None, 97)
    sFont  = pygame.font.Font(None, 32)
    while True:
        screen.fill((255, 255, 255))

        gameOverText = endFont.render("Game Over", True, (0, 235, 234))
        gameOverTextRect = gameOverText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))

        scoretxt = sFont.render(f"score: {str(floor(score))}", True, (0, 235, 234))
        scoretxtRect = scoretxt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        screen.blit(gameOverText, gameOverTextRect)
        screen.blit(scoretxt, scoretxtRect)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                exit()

        pygame.display.update()
        clock.tick(fps)

ground = pygame.image.load('images/ground.png').convert_alpha()
groundRect = ground.get_rect()

def game():
    onGame = True
    while onGame:
        screen.fill(bgColor)

        player.draw(screen)
        player.update()

        apple.draw(screen)
        apple.update()

        screen.blit(ground, (0, 450), groundRect)

        scoreText = font.render(f"score: {str(floor(score))}", True, (255, 255, 255))
        scoreRect = scoreText.get_rect()
        scoreRect.center = (100, 40)
        screen.blit(scoreText, scoreRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        clock.tick(fps)
        pygame.display.update()

startImage = pygame.image.load("images/start_btn.png").convert_alpha()
exitImage = pygame.image.load("images/exit_btn.png").convert_alpha()

start_btn = button(SCREEN_WIDTH/2 - 615 * 0.15, SCREEN_HEIGHT/2, startImage, 0.20)
exit_btn = button(SCREEN_WIDTH/2 - 615 * 0.15, SCREEN_HEIGHT/2 + 125, exitImage, 0.20)

onMenu = True
while onMenu:
    screen.fill((0, 255, 255))
    font = pygame.font.Font(None, 64)

    menuText = font.render("Catch the Apple", True, (255, 255, 255))
    menutextRect = menuText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 75))

    screen.blit(menuText, menutextRect)

    if exit_btn.draw():
        pygame.quit()
        exit()
    if start_btn.draw():
        game()
        onMenu = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(fps)