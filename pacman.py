import sys
import pygame
from pygame.locals import *
from math import floor
import random





def init_window():
    pygame.init()
    pygame.display.set_mode((tile_size*map_size,tile_size*map_size))
    pygame.display.set_caption('Packman')




def draw_background(screen, image=None):
    if image:
        screen.blit(image,(0,0))
    else:
        background=pygame.Surface(screen.get_size())
        background.fill((0,0,0))
        screen.blit(background,(0,0))
        
        
        
        
class GameObject(pygame.sprite.Sprite):

    def __init__(self,x,y,image,map_size,tile_size):
    
        self.x=0
        self.y=0
        self.image=pygame.image.load(image)
        self.screen_rect=None
        self.map_size=map_size        
        self.tile_size=tile_size
        self.tick=0
        self.set_coord(x,y)


    def set_coord(self,x,y):
        self.x=x
        self.y=y
        self.screen_rect=Rect(floor(x)*self.tile_size,floor(y)*self.tile_size,self.map_size,self.map_size)

    def game_tick(self):
        self.tick+=1

    def draw(self,screen):
        screen.blit(self.image,(self.screen_rect.x,self.screen_rect.y))






class Ghost(GameObject):
    
    def __init__(self,x,y,image,map_size,tile_size):
        GameObject.__init__(self,x,y,image,map_size,tile_size)
        self.direction=None
        self.speed=4.0/10.0
    
    def game_tick(self):
    
        super(Ghost,self).game_tick()
        
        if self.tick%20==0 or self.direction==None:
            self.direction=random.randint(1,4) 
            
        if self.direction==1:
            self.y-=self.speed
            if self.y<0 or map.get(floor(self.x),floor(self.y))=='W' or map.get(floor(self.x),floor(self.y))=='D':
                self.y+=self.speed
                self.direction=random.randint(1,4)
                
        
        elif self.direction==2:
            self.x+=self.speed
            if self.x>map_size or map.get(floor(self.x),floor(self.y))=='W' or map.get(floor(self.x),floor(self.y))=='D':
                self.x-=self.speed
                self.direction=random.randint(1,4)
        
        elif self.direction==3:
            self.y+=self.speed
            if self.y>map_size or map.get(floor(self.x),floor(self.y))=='W' or map.get(floor(self.x),floor(self.y))=='D':
                self.y-=self.speed
                self.direction=random.randint(1,4)
        
        elif self.direction==4:
            self.x-=self.speed
            if self.x<0 or map.get(floor(self.x),floor(self.y))=='W' or map.get(floor(self.x),floor(self.y))=='D':
                self.x+=self.speed
                self.direction=random.randint(1,4)
                
        self.set_coord(self.x,self.y)                   
                
                
                
                
class Packman(GameObject):
    
    def __init__(self,x,y,image,map_size,tile_size):
        GameObject.__init__(self,x,y,image,map_size,tile_size)
        self.direction=0
        self.speed=4.0/10.0
            
    def game_tick(self):
    
        super(Packman,self).game_tick()        
                 
        if self.direction==1:
            self.y-=self.speed
            if self.y<0 :
                self.y+=self.speed 
            elif map.get(floor(self.x),floor(self.y))=='W':
                self.direction=0
                self.y+=self.speed 
            self.image=pygame.image.load('./resources/pacmanUP.png')                      
        
        elif self.direction==2:
            self.x+=self.speed
            if self.x>map_size:
                self.x-=self.speed 
            elif map.get(floor(self.x),floor(self.y))=='W':
                self.direction=0
                self.x-=self.speed  
            self.image=pygame.image.load('./resources/pacmanRIGHT.png')             
        
        elif self.direction==3:
            self.y+=self.speed
            if self.y>map_size:
                self.y-=self.speed
            elif map.get(floor(self.x),floor(self.y))=='W':
                self.direction=0
                self.y-=self.speed
            self.image=pygame.image.load('./resources/pacmanDOWN.png')
                
        elif self.direction==4:
            self.x-=self.speed
            if self.x<0:
                self.x+=self.speed
            elif map.get(floor(self.x),floor(self.y))=='W':
                self.direction=0
                self.x+=self.speed      
            self.image=pygame.image.load('./resources/pacmanLEFT.png')                  
                
        self.set_coord(self.x,self.y)




class Map():
    
    def __init__(self,map_size,filename):
        
        self.map=[['']*map_size for i in range(map_size)]
        self.file=open(filename,'r')  
        for y in range(map_size):
            for x in range(0,map_size+1):
                b=self.file.read(1)
                if b!='\n':
                   self.map[y][x]=b
            
        
    def get(self,x,y):
        return self.map[y][x]



class Wall(GameObject):
    
    def __init__(self,x,y,image,map_size,tile_size):
        GameObject.__init__(self,x,y,image,map_size,tile_size)
        
        
        
            
class DestroyWall(GameObject):
    
    def __init__(self,x,y,image,map_size,tile_size):
        GameObject.__init__(self,x,y,image,map_size,tile_size)
        



class Food(GameObject):

    def __init__(self,x,y,image,map_size,tile_size):
        GameObject.__init__(self,x,y,image,map_size,tile_size)
        
    
        



def process_events(events):
    
    for event in events:
        if (event.type==QUIT) or (event.type==KEYDOWN and event.key==K_ESCAPE):
            sys.exit(0)
        elif event.type==KEYDOWN:
            if event.key==K_UP:
                packman.direction=1
            elif event.key==K_RIGHT:
                packman.direction=2
            elif event.key==K_DOWN:
                packman.direction=3
            elif event.key==K_LEFT:
                packman.direction=4
            elif event.key==K_SPACE:
                packman.direction=0




if __name__=='__main__':
    
    tile_size=32    
    map_size=16
    init_window()
    ghost=[]
    wall=[]
    destroy_wall=[]
    food=[]
    map=Map(map_size,'map.txt')                 
    
    for y in range(map_size):
        for x in range(map_size):
            if map.get(x,y)=='G':
                ghost.append(Ghost(x,y,'./resources/ghost.png',map_size,tile_size))
            if map.get(x,y)=='P':
                packman=Packman(x,y,'./resources/pacmanRIGHT.png',map_size,tile_size,)
            if map.get(x,y)=='F':
                food.append(Food(x,y,'./resources/FOOD.png',map_size,tile_size))
            if map.get(x,y)=='W':
                wall.append(Wall(x,y,'./resources/WALL.png',map_size,tile_size))
            if map.get(x,y)=='D':
                destroy_wall.append(DestroyWall(x,y,'./resources/WALL1.png',map_size,tile_size))
    
    background=pygame.image.load('./resources/background.png')
    screen=pygame.display.get_surface()
    k=len(food)
    while 1:
        
        for i in range(len(ghost)):
            if (floor(packman.x)==floor(ghost[i].x) and floor(packman.y)==floor(ghost[i].y)) or k<=0:
                sys.exit(0)
        else:
            
            for i in range(len(destroy_wall)):
                if floor(packman.x)==floor(destroy_wall[i].x) and floor(packman.y)==floor(destroy_wall[i].y):
                    map.map[destroy_wall[i].y][destroy_wall[i].x]=' '
                    destroy_wall[i].set_coord(-1,-1)
                    
            for i in range(len(food)):
                if floor(packman.x)==floor(food[i].x) and floor(packman.y)==floor(food[i].y):
                    food[i].set_coord(-1,-1)
                    k-=1
                    
            process_events(pygame.event.get())
            pygame.time.delay(100)
            packman.game_tick()
            for i in range(len(ghost)):
                ghost[i].game_tick()
            for i in range(len(wall)):
                wall[i].game_tick()   
            for i in range(len(destroy_wall)):
                destroy_wall[i].game_tick()   
            for i in range(len(food)):
                food[i].game_tick()           
            draw_background(screen,background)
            for i in range(len(wall)):
                wall[i].draw(screen)
            for i in range(len(destroy_wall)):
                destroy_wall[i].draw(screen)
            for i in range(len(food)):
                food[i].draw(screen)
            for i in range(len(ghost)):
                ghost[i].draw(screen)
            packman.draw(screen)
            pygame.display.flip()

