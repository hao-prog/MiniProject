import pygame
from pygame.locals import *
import random
import math


class Game:

    pygame.init()
    star = "sun.png"
    one = "One.png"
    two = "Two.png"

    pygame.display.set_caption("Star Trek")
    pygame.display.set_icon(pygame.image.load("solar-system.png"))

    def __init__(self):
        self.running = True
        self.playing = True

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.window.get_width()
        self.height = self.window.get_height()

        self.canvas = pygame.Surface((self.width, self.height))
        self.milky = pygame.image.load("space.jpg")
        self.background = pygame.transform.scale(
            self.milky, (self.width, self.height))

        self.stars = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()

    def loop(self):
        if self.playing:
            self.stars.add(Star(self))
            self.planets.add(Planet(self, 1))

        while self.playing:

            self.events()

            self.window.blit(self.background, (0, 0))
            self.stars.update()
            self.planets.update()

            self.stars.draw(self.window)
            self.planets.draw(self.window)
            
            pygame.display.update()
            self.clock.tick(self.fps)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    print(self.planets.sprites()[0].x)


class Planet(pygame.sprite.Sprite):
    def __init__(self, game, n, t=0):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.time = t
        self.image = pygame.image.load("Baren.png")
        self.image = pygame.transform.scale(self.image,(30, 30))
        self.rect = self.image.get_rect()
        self.a = 300*n
        self.rect.center = [self.game.width//2, self.game.height//2 + self.a]

    def update(self):
        self.time += 1
        self.theta = 2*math.pi*self.time/1000
        self.x = math.cos(self.theta)*self.a
        self.y = math.sin(self.theta)*self.a
        self.rect.center = [self.game.width//2 + self.x, self.game.height//2 + self.y]
        pygame.draw.circle(self.game.window, (255, 204, 0), self.game.stars.sprites()[0].rect.center, self.a, width = 2)


class Star(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Terran.png")
        self.image = pygame.transform.scale(self.image,(70, 70))
        self.rect = self.image.get_rect()
        self.rect.center =[game.width//2, game.height//2]




