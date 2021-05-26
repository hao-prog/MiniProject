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
        self.clouds = pygame.sprite.Group()

        self.alpha = random.randint(0, 9)
        self.beta = self.rndBeta()

        self.topz = round(self.height*0.5787)

        self.imgz = []
        self.sizez = []

        self.one = None
        self.two = None
        self.three = None

        self.result = []
        self.resultSizez = []

        self.ans = False

        self.quest = True

        self.countdown = False
        self.cd = 359
        self.faded = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA, 32)
        self.faded = self.faded.convert_alpha()
        self.faded.fill((0, 0, 0, 175))

        self.basic = True
        self.time1 = 10801

        self.time2 = 7200

        self.hide = False

        self.loading = False

    def rndBeta(self):
        t = -1
        while t < 0 or t > 9:
            daGap = random.randint(2, 4)
            t = self.alpha + random.choice((-1, 1)) * daGap
        return t

    def loop(self):
        if self.playing:
            self.addPlanets()

        while self.playing:

            self.events()

            self.window.blit(self.canvas, (0, 0))
            self.canvas.blit(self.background, (0, 0))
            self.updFPS()

            if self.time1 == 10800:
                self.countdown = False

            if self.quest:
                if not self.hide:
                    self.blitTimes()
                    self.blitSpace()
                    self.blitAitch()
                self.blitPlanets()

                if self.countdown:
                    self.blitCountdown()

                elif self.basic:
                    self.time1 -= 1
                    if self.time1 <= 0:
                        self.basic = False
                        self.rmOrbit()
                        self.rmMoons()
                        self.addClouds()

                else:
                    self.time2 -= 1
                    if self.time2 <= 0:
                        self.quest = False
                        self.loading = True
            elif self.loading:
                self.blitText('Loading...', self.wi-150,
                              self.he, self.canvas, size=70)
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
                f = pygame.font.Font('editundo.ttf', 40)
                self.blitText(self.end, self.wi - f.size(self.end)[0]//2,
                              self.he//6, self.canvas, size=40)
                self.blitText("Your answer:", self.wi - f.size("Your answer:")[0]//2,
                              self.he//3, self.canvas, size=40)
                self.blitChoices(y = self.he//2)
                
                self.blitText("Correct answer:", self.wi - f.size("Correct answer:")[0]//2,
                              self.he*9//16 + self.topz//2 , self.canvas, size=40)
                self.blitChoices(y = self.he*5//4, result = True)
                self.blitText("Press R to play again!", self.wi - f.size("Press R to play again!")[0]//2,
                              self.he*15//8, self.canvas, size=40)
                
            pygame.display.update()
            self.clock.tick(self.fps)

    def addPlanets(self):
        for i in range(1, 11):
            self.moons.add(Moon(self, i))
        self.earths.add(Earth(self))
        self.moonz = self.moons.sprites()
        self.alpha = self.moonz[self.alpha]
        self.beta = self.moonz[self.beta]
        
    def addClouds(self):
        tempMoon = self.alpha.id - 1
        if self.alpha.id < self.beta.id:
            tempMoon = self.beta.id - 1
        
        angle1 = random.randint(0, 360) * math.pi / 180   
        anglez = []
        for i in range(0, 3):
            anglez.append(angle1 + i * 2 * math.pi / 3)
        
        for angle in anglez:
            centerX = math.cos(angle)*self.moonz[tempMoon].r + self.moonz[tempMoon].w
            centerY = math.sin(angle)*self.moonz[tempMoon].r + self.moonz[tempMoon].h
            self.clouds.add(Cloud(self, centerX, centerY))    
        
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
                    if not self.countdown:
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
                if event.key == pygame.K_r:
                    self.moons.empty()
                    self.clouds.empty()
                    
                    self.alpha = random.randint(0, 9)
                    self.beta = self.rndBeta()
                    
                    self.addPlanets()
                    self.imgz = []
                    self.sizez = []
                    self.one = None
                    self.two = None
                    self.three = None
                    self.result = []
                    self.resultSizez = []
                    self.ans = False
                    self.quest = True
                    self.basic = True
                    self.time1 = 10801
                    self.time2 = 7200

    def checkResult(self):
        a = self.imgz[self.one]
        b = self.imgz[self.two]
        c = self.imgz[self.three]

        if a not in self.result or b not in self.result or c not in self.result:
            self.end = "Wrong"
        else:
            self.end = "Correct"

    def updFPS(self):
        fps = str(round(self.clock.get_fps()))
        self.blitText(fps, 20, 20, self.canvas)

    def blitTimes(self):
        l = []
        l.append('You have')
        l.append('to observe ten')
        l.append('moving planets')
        l.append('with orbits')
        l.append('Then,')
        l.append('You have')
        l.append('to observe two')
        l.append('random selected')
        l.append('planes moving')
        l.append('without orbits')
        for i in range(len(l)):
            if i >= 4:
                self.blitText(l[i], 50, 200 + (i*40) + 20, self.canvas)
            else:
                self.blitText(l[i], 50, 200 + (i*40), self.canvas)

        t1 = str(self.time1//60) + " s"
        self.blitText(t1, 200, 200, self.canvas, color=(249, 192, 0))
        t2 = str(self.time2//60) + " s"
        self.blitText(t2, 200, 420, self.canvas, color=(249, 192, 0))

    def blitSpace(self):
        l = []
        l.append('Press')
        l.append('to skip (Current')
        l.append('Countdown time')
        l.append('is reduced to 0)')
        for i in range(len(l)):
            self.blitText(l[i], self.width-300, 200 + (i*40), self.canvas)

        raw = pygame.image.load("Matls/Keys/Space.png")
        img = pygame.transform.scale2x(raw)
        self.canvas.blit(img, (self.width-200, 200))
        self.blitText('Space', self.width-145, 203, self.canvas, size=20)

    def blitAitch(self):
        l1 = 'Press   to'
        self.blitText(l1, self.width-300, 380, self.canvas)
        l2 = 'hide instructions'
        self.blitText(l2, self.width-300, 420, self.canvas)

        raw = pygame.image.load("Matls/Keys/H.png")
        img = pygame.transform.scale2x(raw)
        self.canvas.blit(img, (self.width-213, 380))

    def blitPlanets(self):
        self.earths.update()
        self.moons.update()
        self.clouds.update()

        self.earths.draw(self.canvas)
        self.moons.draw(self.canvas)
        self.clouds.draw(self.canvas)

    def blitCountdown(self):
        self.window.blit(self.faded, (0, 0))

        l = 'Game start in:'
        self.blitText(l, self.wi-150, self.he-100, self.window, size=50)
        cd = str(self.cd//60)
        self.blitText(cd, self.wi - 25, self.he, self.window, size=100)

        self.cd -= 1
        if self.cd == 0:
            self.countdown = False
            self.time1 -= 1

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
                if (a == self.alpha and b == self.beta) or (a == self.beta and b == self.alpha):
                    self.result.append(z)
                    self.resultSizez.append(s)
                j += 1
            i += 1

    def sizeImg(self, a, b):
        m = max(a.r, b.r)
        t = 1
        while t*m < self.topz:
            t += 1
        return t

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

    def setImg(self):
        d = self.id
        s = self.sizez[d]
        t = pygame.image.fromstring(self.imgz[d], (s, s), 'RGBA')
        self.top = pygame.transform.smoothscale(t, (self.topz, self.topz))

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

    def blitNums(self):
        l1 = 'Press   ,   or   to add'
        self.blitText(l1, self.width-450, 150, self.canvas)
        l2 = 'the current image to the'
        self.blitText(l2, self.width-450, 190, self.canvas)
        l3 = 'corresponding cell'
        self.blitText(l3, self.width-450, 230, self.canvas)

        self.blitKey('one', self.width - 363, 150)
        self.blitKey('two', self.width-308, 150)
        self.blitKey('three', self.width-227, 150)

    def blitEnter(self):
        l1 = "Press      to submit"
        self.blitText(l1, self.width-450, 290, self.canvas)
        l2 = 'answers once you have'
        self.blitText(l2, self.width-450, 330, self.canvas)
        l3 = 'filled them up'
        self.blitText(l3, self.width-450, 370, self.canvas)

        self.blitKey('Enter', self.width - 363, 290)

    def blitAns(self):
        h = self.height//3
        x = self.wi-self.topz//2
        y = h-self.topz//2
        
        self.blitBorder(self.top, x, y)
        self.canvas.blit(self.top, (x, y))
        self.blitIndex(x+20, y+20)
        self.blitChoices()

    def blitBorder(self, img, x, y):
        mask = pygame.mask.from_surface(img)
        mask_surf = mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))
        mask_surf.fill((214, 187, 154))
        self.canvas.blit(mask_surf, (x - 2, y))
        self.canvas.blit(mask_surf, (x + 2, y))
        self.canvas.blit(mask_surf, (x, y - 2))
        self.canvas.blit(mask_surf, (x, y + 2))

    def blitIndex(self, x, y):
        l = len(self.imgz)
        index = str(self.id+1) + "/" + str(l)
        self.blitText(index, x, y, self.canvas)

    def blitChoices(self, y = 0, result = False):
        t = self.topz//2
        x = self.width//6
        if y == 0:
            y = round(self.height*0.815 - t//2)

        self.blitKey("One", x-t*3//5, y+t//3)
        self.blitKey("Two", x*3-t*3//5, y+t//3)
        self.blitKey("Three", x*5-t*3//5, y+t//3)

        if result:
            self.blitChoice(self.result[0], x-t//4, y, self.resultSizez[0])
            self.blitChoice(self.result[1], x*3-t//4, y, self.resultSizez[1])
            self.blitChoice(self.result[2], x*5-t//4, y, self.resultSizez[2])
        else:
            if self.one != None:
                self.blitChoice(self.one, x-t//4, y)
            else:
                self.blitRect(x-t//4, y)
            if self.two != None:
                self.blitChoice(self.two, x*3-t//4, y)
            else:
                self.blitRect(x*3-t//4, y)
            if self.three != None:
                self.blitChoice(self.three, x*5-t//4, y)
            else:
                self.blitRect(x*5-t//4, y)

    def blitChoice(self, c, x, y, s = 0):
        if type(c) is int:
            img = self.getImg(c)
        else:
            t = pygame.image.fromstring(c, (s, s), 'RGBA')
            img = pygame.transform.smoothscale(t, (self.topz//2, self.topz//2))
        self.blitBorder(img, x, y)
        self.canvas.blit(img, (x, y))

    def getImg(self, i):
        s = self.sizez[i]
        t = pygame.image.fromstring(self.imgz[i], (s, s), 'RGBA')
        c = pygame.transform.smoothscale(t, (self.topz//2, self.topz//2))
        return c

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

    def blitKey(self, n, x, y):
        raw = pygame.image.load(f"Matls/Keys/{n}.png")
        img = pygame.transform.scale2x(raw)
        self.canvas.blit(img, (x, y))

    def blitText(self, text, x, y, surf, size=32, color=(255, 255, 255)):
        f = pygame.font.Font('editundo.ttf', size)
        t = f.render(text, True, color)
        surf.blit(t, (x, y))


class Moon(pygame.sprite.Sprite):
    def __init__(self, game, n, t=0):
        pygame.sprite.Sprite.__init__(self)
        self.id = n
        self.game = game
        self.w = self.game.wi
        self.h = self.game.he
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
        self.rect.center = (game.wi, game.he)
        
class Cloud(pygame.sprite.Sprite):
    def __init__(self, game, centerX, centerY):
        pygame.sprite.Sprite.__init__(self)
        
        self.raw = pygame.image.load("Matls/Others/cloud{}.png".format(random.choice((1, 2))))
        size = round(game.height * 0.5)
        self.raw = pygame.transform.scale(self.raw, (size, size))
        self.image = self.raw
        self.rect = self.image.get_rect()
        self.rect.center = (centerX, centerY)
        