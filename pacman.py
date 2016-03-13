import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Packman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((0, 0, 0))
        scr.blit(bg, (0, 0))

class Map:
    def __init__(self,x,y):
        self.map=[[list()]*x for i in range(y)]
    def get(self,x,y):
        return self.map[x][y]

class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    ghosts=[]
    num=2
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(floor(self.x+self.velocity), self.y):
                self.x += self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x,(floor( self.y+self.velocity))):
                self.y += self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if not is_wall(floor(self.x-self.velocity),self.y):
                self.x -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if not is_wall(self.x,(floor(self.y-self.velocity))):
                self.y -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)

class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        self.food=0
        GameObject.__init__(self, './resources/pacmanRIGHT.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x+self.velocity), self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if not is_wall(self.x,(floor(self.y+self.velocity))):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x-self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x,(floor(self.y-self.velocity))):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.set_coord(self.x, self.y)

class FOOD(GameObject):

    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/FOOD.png', x,y,tile_size,map_size)
        self.life=1

def draw_food(screen):
    for F in FOOD:
        if F.life>0:
            GameObject.draw(F,screen)

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/WALL.png', x, y, tile_size, map_size)

    def get(self,x,y):
        return self.map[x][y]


def is_wall(x, y):
    for W in walls:
        if (int(W.x), int(W.y)) == (int(x), int(y)):
            return True
    return False

def draw_walls(screen):
    for W in walls:
        GameObject.draw(W,screen)

def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
                pacman.image=pygame.image.load('./resources/pacmanLEFT.png')
            elif event.key == K_RIGHT:
                packman.direction = 1
                pacman.image=pygame.image.load('./resources/pacmanRIGHT.png')
            elif event.key == K_UP:
                packman.direction = 4
                pacman.image=pygame.image.load('./resources/pacmanUP.png')
            elif event.key == K_DOWN:
                packman.direction = 2
                pacman.image=pygame.image.load('./resources/pacmanDOWN.png')
            elif event.key == K_SPACE:
                packman.direction = 0


if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16
    walls=[]
    ghosts=[]
    food=[]
    input=open('map.txt','r')
    for i in range (map_size+1):
        for z in range(map_size+1):
            T=input.read(1)
            if T=='W':
                walls.append(Wall(z,i,tile_size,map_size))
            elif T=='G':
                ghosts.append(Ghost(z,i,tile_size,map_size))
            elif T=='F':
                food.append(Food(z,i,tile_size,map_size))
    pacman = Pacman(5, 5, tile_size, map_size)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick()
        pacman.game_tick()
        draw_background(screen, background)
        pacman.draw(screen)
        ghost.draw(screen)
        pygame.display.update()
        for F in FOOD:
            if int(F.x)==int(pacman.x) and int(F.y)==int(pacman.y):
                food.remove(f)
                if len(food)==0:
                    sys.exit(0)
        for G in GHOSTS:
            if int(G.x)==int(pacman.x) and int(G.y)==int(pacman.y):
                sys.exit()
