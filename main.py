import math
import pygame
import random

FPS = 240
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
GAME_FONT = pygame.font.Font("Montserrat-VariableFont_wght.ttf", 24)
objects = []
stepsize = 0.1

def galaxy(n):
    for i in range(n):
        rot = random.uniform(0, 2 * math.pi)
        objects.append(object(math.sin(rot) * random.randint(10, 100), math.cos(rot) * random.randint(10, 100), 0, 0, 1))

    
class object():
    def __init__(self, x, y, xvel, yvel, mass):
      self.x = x
      self.y = y
      self.xvel = xvel
      self.yvel = yvel
      self.mass = mass
      
def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + 0.5  # COORDINATE GEOMETRY!!! 
      
def iterate(objects): 
    for i in objects: #Calculate gravity for all objects
        for j in objects: #Calculate for each pair
            if i != j:
                distance = dist(i.x, i.y, j.x, j.y)
                i.xvel += j.mass * (j.x - i.x) / distance ** 3 * stepsize
                i.yvel += j.mass * (j.y - i.y) / distance ** 3 * stepsize

def moveobjects(objects):
    for object in objects:
        object.x += object.xvel
        object.y += object.yvel 

def draw(objects):
    WIN.fill((0, 0, 0))
    for i in objects:
        if i.x + WIDTH/2 > 0 and i.x + WIDTH/2 < WIDTH and i.y + HEIGHT/2 > 0 and i.y + HEIGHT/2 < HEIGHT: # If point is in window
            pygame.draw.circle(WIN, (255, 255, 255), (i.x + WIDTH/2, i.y + HEIGHT/2), 1)
    textsurface = GAME_FONT.render(str(int(clock.get_fps())), False, (255, 255, 255))
    WIN.blit(textsurface, (0, 0))
    pygame.display.update()

galaxy(100)

def main():
    run = True
    global clock
    clock = pygame.time.Clock()
    while run: 
        draw(objects)
        clock.tick(FPS)
        iterate(objects)
        moveobjects(objects)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


          
if __name__ == "__main__":
    main()
