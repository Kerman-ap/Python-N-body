import math
import pygame
import random
import colorsys

FPS = 999
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
GAME_FONT = pygame.font.Font("Montserrat-VariableFont_wght.ttf", 24)
objects = []
stepsize = 0.2

def galaxy(n):
    for i in range(n):
        rot = random.uniform(0, 2 * math.pi)
        objects.append(object(math.sin(rot) * random.randint(30, 100), math.cos(rot) * random.randint(30, 100), math.sin(rot - 1.57) * 0.1, math.cos(rot - 1.57) * 0.1, 1))

def getcenterofmass(objects):
    x = 0
    y = 0
    for i in objects:
        x += i.x 
        y += i.y
    return (x/len(objects), y/len(objects))

class rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def contains(self, point):
        return(point[0] > self.x - self.width / 2 and point[0] < self.x + self.width / 2 and point[1] < self.y + self.height / 2 and point[1] > self.y - self.height / 2)
    
class quadtree():
    def __init__(self, boundary):
        self.boundary = boundary
        self.divided = False
        self.centerofmass = (0, 0)
        self.objects = []
        
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        width = self.boundary.width
        height = self.boundary.height
        
        # Create subtrees for each quadrant 
        nw = rect(x - width/4, y + height/4, width/2, width/2)
        self.nw = quadtree(nw)
        ne = rect(x + width/4, y + height/4, width/2, width/2)
        self.ne = quadtree(ne)
        sw = rect(x - width/4, y - height/4, width/2, width/2)
        self.sw = quadtree(sw)
        se = rect(x + width/4, y - height/4, width/2, width/2)
        self.se = quadtree(se)
        
        self.divided = True # Mark as divided
        
    def insert(self, object):
        if len(self.objects) < 1 and not self.divided: # If box is already empty (no subdivision needed)
            self.objects.append(object)
        else:
            if not self.divided:
                self.subdivide() #Subdivide if not already
            self.objects.append(object)
            while self.objects: #Put all objects in node into children
                object = self.objects.pop()
                x = object.x > self.boundary.x
                y = object.y > self.boundary.y
                
                #insert to quadrant
                if y:
                    if x:
                        self.ne.insert(object)
                    else: 
                        self.nw.insert(object)
                else:
                    if x: 
                        self.se.insert(object)
                    else: 
                        self.sw.insert(object)
            
    def drawtree(self, iterations, maxiterator):
        maxiter = maxiterator
        iterations = iterations + 1
        if iterations > maxiter:
            maxiter = iterations
        color = hsv2rgb(iterations / 10, 1, 1)
        pygame.draw.rect(WIN, color, (round(self.boundary.x - self.boundary.width / 2 + WIDTH/2), round(self.boundary.y - self.boundary.height / 2 + HEIGHT/2), self.boundary.width, self.boundary.height), 1)
        if self.divided:
            divmax = (
            self.ne.drawtree(iterations, maxiter),
            self.nw.drawtree(iterations, maxiter),
            self.sw.drawtree(iterations, maxiter),
            self.se.drawtree(iterations, maxiter))
            if max(divmax) > maxiter:
                maxiter = max(divmax)
        return maxiter



class object():
    def __init__(self, x, y, xvel, yvel, mass):
      self.x = x
      self.y = y
      self.xvel = xvel
      self.yvel = yvel
      self.mass = mass



def buildtree(objects):
    boundary = findrect(objects)
    rectboundary = rect(boundary[0], boundary[1], boundary[2], boundary[3])
    global tree
    tree = quadtree(rectboundary)
    for object in objects:
        tree.insert(object)
    
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def findrect(objects):
    length = []
    for i in objects:
        length.append(i.x)
        length.append(i.y)
    size = math.ceil((max(length) + abs(min(length)))/32)*32
    return (min(length) + max(length))/2, (min(length) + max(length))/2, size, size
      
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
    centerofmass = 0, 0 
    WIN.fill((0, 0, 0))
    #tree.drawtree(0, 1)
    for i in objects:
        if i.x + WIDTH/2 - centerofmass[0] > 0 and i.x + WIDTH/2 - centerofmass[0] < WIDTH and i.y + HEIGHT/2 - centerofmass[1] > 0 and i.y + HEIGHT/2 - centerofmass[1] < HEIGHT: # If point is in window
            pygame.draw.circle(WIN, (255, 255, 255), (i.x + WIDTH/2 - centerofmass[0], i.y + HEIGHT/2 - centerofmass[1]), 1)
    textsurface = GAME_FONT.render(str(int(clock.get_fps())), False, (255, 255, 255))
    WIN.blit(textsurface, (0, 0))
    pygame.display.update()

galaxy(200)

def main():
    run = True
    global clock
    clock = pygame.time.Clock()
    while run: 
        #buildtree(objects)
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
