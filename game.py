import pygame
from pygame.locals import *
import random
import math
import numpy
import operator
from sklearn.utils import shuffle


class Game:

    pygame.init()

    pygame.display.set_caption("Star Trek")
    pygame.display.set_icon(pygame.image.load("Matls/Others/icon.png"))

    def __init__(self):
        self.running = True
        self.playing = True

        self.font = pygame.font.Font('editundo.ttf', 32)

        self.clock = pygame.time.Clock()
        self.fps = 66

        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.window.get_width()
        self.height = self.window.get_height()
        self.wi = self.width//2
        self.he = self.height//2

        self.canvas = pygame.Surface((self.width, self.height))
        self.id = 0

        self.space = pygame.image.load("Matls/Others/dark.jpg")
        self.background = pygame.transform.smoothscale(
            self.space, (self.width, self.height))

        self.earths = pygame.sprite.Group()
        self.moons = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()

        self.one = None
        self.two = None
        self.three = None

        self.alpha = random.randint(0, 9)
        self.beta = self.rndBeta()

        self.result = []

        self.imgz = []
        self.sizez = []

        self.ans = False

        self.topz = round(self.height*0.5787)

        self.countdown = False
        self.cd = 359

        self.quest = True
        self.basic = True
        self.time1 = 10801
        self.time2 = 7200
        self.loading = False
        self.hide = False

        self.faded = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA, 32)
        self.faded = self.faded.convert_alpha()
        self.faded.fill((0, 0, 0, 175))

    def loop(self):
        if self.playing:
            self.addPlanets()

        while self.playing:

            self.events()

            self.window.blit(self.canvas, (0, 0))
            self.canvas.blit(self.background, (0, 0))
            self.canvas.blit(self.updFPS(), (20, 20))

            if self.time1 == 10800:
                self.countdown = True

            if self.quest:
                if not self.hide:
                    self.blitTimes()
                    self.blitSpace()
                    self.blitAitch()
                self.blitPlanets()

                if self.countdown:
                    self.blitCountdown()
                    self.cd -= 1
                    if self.cd == 0:
                        self.countdown = False
                        self.time1 -= 1

                elif self.basic:
                    self.time1 -= 1
                    if self.time1 <= 0:
                        self.basic = False
                        self.rmOrbit()
                        self.rmMoons()
                else:
                    self.time2 -= 1
                    if self.time2 <= 0:
                        self.quest = False
                        self.loading = True
            elif self.loading:
                l = self.font.render("Loading...", True, (255, 255, 255))
                self.canvas.blit(l, (self.width//2-100, self.height//2))
                self.creAns()
                self.setImg()
                self.loading = False
                self.ans = True
            elif self.ans:
                if not self.hide:
                    self.blitRules()
                    self.blitNums()
                    self.blitEnter()
                self.blitAns()
            else:
                e = self.font.render(self.end, True, (255, 255, 255))
                self.canvas.blit(e, (self.width//2, self.height//2))

            pygame.display.update()

            self.clock.tick(self.fps)

    def addPlanets(self):
        for i in range(1, 11):
            self.moons.add(Moon(self, i))
        self.earths.add(Earth(self))
        self.moonz = self.moons.sprites()
        self.alpha = self.moonz[self.alpha]
        self.beta = self.moonz[self.beta]

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_1:

                    self.one = self.id

                if event.key == pygame.K_2:

                    self.two = self.id
                if event.key == pygame.K_3:

                    self.three = self.id

                if event.key == pygame.K_RIGHT:
                    self.id += 1
                    if self.id >= len(self.imgz):
                        self.id = 0
                    self.setImg()
                if event.key == pygame.K_LEFT:
                    self.id -= 1
                    if self.id < 0:
                        self.id = len(self.imgz)-1
                    self.setImg()
                if event.key == pygame.K_SPACE:
                    if self.basic:
                        self.time1 = 1
                    elif self.quest:
                        self.time2 = 1
                if event.key == pygame.K_RETURN:
                    if self.one != None and self.one != None and self.one != None:
                        self.checkResult()
                        self.ans = False
                if event.key == pygame.K_h:
                    self.hide = not self.hide

    def blitCountdown(self):
        self.window.blit(self.faded, (0, 0))

        l = 'Game start in:'
        self.blitText(l, self.wi-150, self.he-100, self.window, size=50)

        cd = str(self.cd//60)
        self.blitText(cd, self.wi - 25, self.he, self.window, size=100)

    def blitPlanets(self):

        self.earths.update()
        self.moons.update()

        self.earths.draw(self.canvas)
        self.moons.draw(self.canvas)

    def rndBeta(self):
        t = -1
        while t < 0 or t > 9:
            daGap = random.randint(2, 4)
            t = self.alpha + random.choice((-1, 1)) * daGap
        return t

    def updFPS(self):

        fps = str(round(self.clock.get_fps()))
        fps_text = self.font.render(fps, True, (255, 255, 255))
        return fps_text

    def rmOrbit(self):
        s = self.moons.sprites()
        for x in s:
            x.orbit = not x.orbit

    def rmMoons(self):
        ms = self.moons.sprites()
        for x in ms:
            if x != self.alpha and x != self.beta:
                x.kill()

    def creAns(self):
        s = len(self.moonz)
        for i in range(s):
            if i+2 < s:
                self.creImg(self.moonz[i], self.moonz[i+2])
            if i+3 < s:
                self.creImg(self.moonz[i], self.moonz[i+3])
            if i+4 < s:
                self.creImg(self.moonz[i], self.moonz[i+4])
        self.imgz, self.sizez = shuffle(self.imgz, self.sizez, random_state=0)

    def creImg(self, a, b):

        t = self.sizeImg(a, b)
        s = round(max(a.r, b.r)*t*1.05*2)
        cs = []
        c = self.collinear(a, b)
        while c < 12000:
            cs.append(c)
            c *= 2

        i = 0
        j = 0
        while j < 3:
            if cs[i] > 1000:
                surf = pygame.Surface((s, s))
                self.drawLines(a, b, cs[i], surf, t)
                z = pygame.image.tostring(surf, 'RGBA')
                self.imgz.append(z)
                self.sizez.append(s)
                if a == self.alpha and b == self.beta:
                    self.result.append(z)
                j += 1
            i += 1

    def sizeImg(self, a, b):
        m = max(a.r, b.r)
        t = 1
        while t*m < self.topz:
            t += 1
        return t

    def drawLines(self, a, b, stop, surf, t=1):
        da = a.dots
        db = b.dots
        s = tuple(x//2 for x in surf.get_size())

        for i in range(0, stop, 25):
            ta = tuple(x*t for x in da[i])
            tb = tuple(x*t for x in db[i])
            pa = tuple(map(operator.add, ta, s))
            pb = tuple(map(operator.add, tb, s))
            pygame.draw.line(surf, (255, 255, 255), pa, pb, 2)

    def collinear(self, a, b):
        da = a.dots
        db = b.dots
        ra = a.r
        rb = b.r

        for i in range(len(da)):
            d = round(math.sqrt((da[i][0]-db[i][0])**2 +
                                (da[i][1]-db[i][1])**2))
            if i > 100 and (ra + rb == d or abs(ra-rb) == d):
                return i + 25

    def setImg(self):
        d = self.id
        s = self.sizez[d]
        t = pygame.image.fromstring(self.imgz[d], (s, s), 'RGBA')
        self.top = pygame.transform.smoothscale(t, (self.topz, self.topz))

    def blitAns(self):
        w = self.width//2
        h = self.height//3
        x = w-self.topz//2
        y = h-self.topz//2

        self.blitBorder(self.top, x, y)
        self.canvas.blit(self.top, (x, y))
        self.canvas.blit(self.blitIndex(), (x+20, y+20))
        self.blitChoices()
        self.keys.draw(self.canvas)

    def blitBorder(self, img, x, y):
        mask = pygame.mask.from_surface(img)
        mask_surf = mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))
        mask_surf.fill((214, 187, 154))
        self.canvas.blit(mask_surf, (x - 2, y))
        self.canvas.blit(mask_surf, (x + 2, y))
        self.canvas.blit(mask_surf, (x, y - 2))
        self.canvas.blit(mask_surf, (x, y + 2))

    def blitIndex(self):
        l = len(self.imgz)
        index = str(self.id+1) + "/" + str(l)
        index_text = self.font.render(index, True, (255, 255, 255))
        return index_text

    def blitChoices(self):
        t = self.topz//2
        x = self.width//6
        y = round(self.height*0.815 - t//2)

        self.blitKey("One", x-t//5*3, y+t//3)
        self.blitKey("Two", x*3-t//5*3, y+t//3)
        self.blitKey("Three", x*5-t//5*3, y+t//3)

        if self.one != None:
            self.blitOne(x-t//4, y)
        else:
            self.blitRect(x-t//4, y)

        if self.two != None:
            self.blitTwo(x*3-t//4, y)
        else:
            self.blitRect(x*3-t//4, y)

        if self.three != None:
            self.blitThree(x*5-t//4, y)
        else:
            self.blitRect(x*5-t//4, y)

    def blitRect(self, x, y):
        t = self.topz//2
        pygame.draw.rect(self.canvas, (214, 187, 154),
                         pygame.Rect(x-2, y, t, t))
        pygame.draw.rect(self.canvas, (214, 187, 154),
                         pygame.Rect(x+2, y, t, t))
        pygame.draw.rect(self.canvas, (214, 187, 154),
                         pygame.Rect(x, y-2, t, t))
        pygame.draw.rect(self.canvas, (214, 187, 154),
                         pygame.Rect(x, y+2, t, t))

        pygame.draw.rect(self.canvas, (0, 0, 0),
                         pygame.Rect(x, y, t, t))

    def creKeys(self):
        l = Key('left', (100, 100))
        self.keys.add(l)

    def blitOne(self, x, y):

        img = self.getImg(self.one)
        self.blitBorder(img, x, y)
        self.canvas.blit(img, (x, y))

    def blitTwo(self, x, y):

        img = self.getImg(self.two)
        self.blitBorder(img, x, y)
        self.canvas.blit(img, (x, y))

    def blitThree(self, x, y):

        img = self.getImg(self.three)
        self.blitBorder(img, x, y)
        self.canvas.blit(img, (x, y))

    def getImg(self, i):
        s = self.sizez[i]
        t = pygame.image.fromstring(self.imgz[i], (s, s), 'RGBA')
        c = pygame.transform.smoothscale(t, (self.topz//2, self.topz//2))
        return c

    def blitKey(self, n, x, y):
        raw = pygame.image.load(f"Matls/Keys/{n}.png")
        img = pygame.transform.scale2x(raw)
        self.canvas.blit(img, (x, y))

    def blitTimes(self):
        l1 = 'You have'
        self.blitText(l1, 50, 200, self.canvas)
        t1 = str(self.time1//60) + " s"
        self.blitText(t1, 200, 200, self.canvas, color=(249, 192, 0))
        l2 = 'to observe ten'
        self.blitText(l2, 50, 240, self.canvas)
        l3 = 'moving planets'
        self.blitText(l3, 50, 280, self.canvas)
        l4 = 'with orbits'
        self.blitText(l4, 50, 320, self.canvas)
        l5 = 'Then,'
        self.blitText(l5, 50, 380, self.canvas)
        l6 = 'You have'
        self.blitText(l6, 50, 420, self.canvas)
        t2 = str(self.time2//60) + " s"
        self.blitText(t2, 200, 420, self.canvas, color=(249, 192, 0))
        l7 = 'to observe two'
        self.blitText(l7, 50, 460, self.canvas)
        l8 = 'random selected'
        self.blitText(l8, 50, 500, self.canvas)
        l9 = 'planes moving'
        self.blitText(l9, 50, 540, self.canvas)
        l10 = 'without orbits'
        self.blitText(l10, 50, 580, self.canvas)

    def blitSpace(self):
        l1 = 'Press'
        self.blitText(l1, self.width-300, 200, self.canvas)
        raw = pygame.image.load("Matls/Keys/Space.png")
        img = pygame.transform.scale2x(raw)
        self.canvas.blit(img, (self.width-200, 200))
        l2 = 'Space'
        self.blitText(l2, self.width-145, 203, self.canvas, size=20)
        l3 = 'to skip (Current'
        self.blitText(l3, self.width-300, 240, self.canvas)
        l4 = 'Countdown time'
        self.blitText(l4, self.width-300, 280, self.canvas)
        l5 = 'is reduced to 0)'
        self.blitText(l5, self.width-300, 320, self.canvas)

    def blitAitch(self):
        l1 = 'Press   to'
        self.blitText(l1, self.width-300, 380, self.canvas)
        raw = pygame.image.load("Matls/Keys/H.png")
        img = pygame.transform.scale2x(raw)
        self.canvas.blit(img, (self.width-213, 380))
        l2 = 'hide instructions'
        self.blitText(l2, self.width-300, 420, self.canvas)

    def blitNums(self):
        l1 = 'Press   ,   or   to add'
        self.blitText(l1, self.width-450, 150, self.canvas)
        self.blitKey('one', self.width - 363, 150)
        self.blitKey('two', self.width-308, 150)
        self.blitKey('three', self.width-227, 150)

        l2 = 'the current image to the'
        self.blitText(l2, self.width-450, 190, self.canvas)
        l3 = 'corresponding cell'
        self.blitText(l3, self.width-450, 230, self.canvas)

    def blitEnter(self):
        l1 = "Press      to submit"
        self.blitText(l1, self.width-450, 290, self.canvas)
        self.blitKey('Enter', self.width - 363, 290)
        l2 = 'answers once you have'
        self.blitText(l2, self.width-450, 330, self.canvas)
        l3 = 'filled them up'
        self.blitText(l3, self.width-450, 370, self.canvas)

    def blitRules(self):
        l = []
        l.append('Based on what you have')
        l.append('seen, now you have to')
        l.append('find 3 stages where')
        l.append('2 selected planets')
        l.append('and the center planet')
        l.append('collinear and arrange')
        l.append('them in the ascending')
        l.append('order of time')
        for i in range(len(l)):
            self.blitText(l[i], 50, 150 + (i*40), self.canvas)

    def checkResult(self):
        a = self.imgz[self.one]
        b = self.imgz[self.two]
        c = self.imgz[self.three]

        if a not in self.result or b not in self.result or c not in self.result:
            self.end = "Wrong"
        else:
            self.end = "Correct"

    def blitText(self, text, x, y, surf, size=32, color=(255, 255, 255)):

        f = pygame.font.Font('editundo.ttf', size)
        t = f.render(text, True, color)
        surf.blit(t, (x, y))


class Moon(pygame.sprite.Sprite):
    def __init__(self, game, n, t=0):
        pygame.sprite.Sprite.__init__(self)
        self.id = n
        self.game = game
        self.w = self.game.width//2
        self.h = self.game.height//2
        self.time = t
        self.raw = pygame.image.load("Matls/Planets/no.png")
        size = round(game.height * 0.03)
        self.raw = pygame.transform.scale(self.raw, (size, size))
        self.image = self.raw
        self.rect = self.image.get_rect()
        self.r = round(game.height * (0.045 * n + 0.02))
        self.rect.center = [self.w, self.h]
        self.cycle = 1250 - (10-n)*125 - random.randint(25, 50)
        self.dots = self.getDots()
        self.orbit = True

    def update(self):
        if not self.game.countdown:
            self.time += 1
            self.rect.center = self.coord(self.time, self.w, self.h)

        if self.orbit:
            pygame.draw.circle(self.game.canvas, (255, 255, 255),
                               (self.w, self.h), self.r, 1)

    def coord(self, time, w=0, h=0):
        self.theta = 2*math.pi*time/self.cycle
        self.x = math.cos(self.theta)*self.r
        self.y = math.sin(self.theta)*self.r

        return (self.x + w, self.y + h)

    def getDots(self):
        dots = []
        for i in range(0, 12000):
            dots.append(self.coord(i))
        return dots


class Earth(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.raw = pygame.image.load("Matls/Planets/wet.png")
        size = round(game.height * 0.055)
        self.raw = pygame.transform.scale(self.raw, (size, size))
        self.image = self.raw
        self.rect = self.image.get_rect()
        self.rect.center = (game.width//2, game.height//2)


class Key(pygame.sprite.Sprite):
    def __init__(self, k, r):
        pygame.sprite.Sprite.__init__(self)
        self.k = k
        self.image = pygame.image.load(f"Matls/Keys/{self.k}.png")
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = r
        self.ed = False
        self.count = False
        self.time = 0

    def update(self):
        if self.ed:
            self.image = pygame.image.load(f"Matls/Keys/{self.k}-ed.png")
            self.rect = self.image.get_rect(center=self.rect.center)
            self.count = True
            self.ed = False

        if self.count:
            if self.time >= 10:
                self.image = pygame.image.load(f"Matls/Keys/{self.k}.png")
                self.rect = self.image.get_rect(center=self.rect.center)
                self.time = 0
                self.count = False
            self.time += 1
