import pygame
from pygame.locals import *
import random
import math


class Game:

    pygame.init()
    
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

        self.earths = pygame.sprite.Group()
        self.moons = pygame.sprite.Group()

    def loop(self):
        if self.playing:
            for i in range(1, 11):                
                self.moons.add(Moon(self, i))
            self.earths.add(Earth(self))

        while self.playing:

            self.events()

            self.window.blit(self.background, (0, 0))
            self.earths.update()
            self.moons.update()

            self.earths.draw(self.window)
            self.moons.draw(self.window)

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
                    print(self.moons.sprites()[0].x)


class Moon(pygame.sprite.Sprite):
    def __init__(self, game, n, t=0):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.w = self.game.width//2
        self.h = self.game.height//2
        self.time = t
        self.image = pygame.image.load("Baren.png")
        size = int(game.height * 0.03)
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect()
        self.r = int(game.height * (0.045 * n +  0.0175))
        self.rect.center = [self.w, self.h + self.r]
        self.dir = random.choice([-1, 1])
        self.cycle = random.randint(1000, 1500) - (12-n)*75

    def update(self):
        self.time += 1
        self.theta = 2*math.pi*self.time/self.cycle
        self.x = math.cos(self.theta)*self.r
        self.y = self.dir * math.sin(self.theta)*self.r
        self.rect.center = [self.w + self.x, self.h + self.y]
        pygame.draw.circle(self.game.window, (255,255,255), (self.w, self.h), self.r, 1)



class Earth(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Terran.png")
        size = int(game.height * 0.13)
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect()
        self.rect.center =[game.width//2, game.height//2]




