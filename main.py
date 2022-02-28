import pygame
import pygame.freetype
import math
import random
import pickle
import colorsys


WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('N Body Simulation')
pygame.init()
FPS = 240
WHITE = (255, 255, 255)
STEPSIZE = 0.1
objects = []
recording = []
GAME_FONT = pygame.font.Font("Montserrat-VariableFont_wght.ttf", 24)
reviewing = False
Drawtree = True
Buildtree = True
scale = 1
lastmax = 10
recentmax = []
lagger = (0, 0)

for i in range(25):
    recentmax.append(10)

class quadtree:
    def __init__(self, iboundary):
        self.boundary = iboundary
        self.points = []
        self.divided = False
    
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        
        nw = rect(x - w/4, y + h/4, w/2, h/2)
        self.nw = quadtree(nw)
        ne = rect(x + w/4, y + h/4, w/2, h/2)
        self.ne = quadtree(ne)
        sw = rect(x - w/4, y - h/4, w/2, h/2)
        self.sw = quadtree(sw)
        se = rect(x + w/4, y - h/4, w/2, h/2)
        self.se = quadtree(se)
        self.divided = True
        
    def insert(self, point):
        
        buildtime = pygame.time.get_ticks()
        if len(self.points) < 1:
            self.points.append(point)
        else:
            if not self.divided:
                self.subdivide()
            x = point[0] > self.boundary.x
            y = point[1] > self.boundary.y
            if y:
                if x:
                    self.ne.insert(point)
                else:
                    self.nw.insert(point)
            else:
                if x:
                    self.se.insert(point)
                else:
                    self.sw.insert(point)
        if pygame.time.get_ticks() - buildtime > 1:
            global lagger
            print(pygame.time.get_ticks() - buildtime)
            print(point)
            lagger = point

    
    def drawtree(self, iterations, maxiterator):
        maxiter = maxiterator
        iterations = iterations + 1
        if iterations > maxiter:
            maxiter = iterations
        color = hsv2rgb(iterations / usedmax, 1, 1)
        normalized = normalize((self.boundary.x - self.boundary.w / 2, self.boundary.y - self.boundary.h / 2))
        pygame.draw.rect(WIN, color, (normalized[0], normalized[1], self.boundary.w / scale, self.boundary.h / scale), 1)
        if self.divided:
            divmax = (
            self.ne.drawtree(iterations, maxiter),
            self.nw.drawtree(iterations, maxiter),
            self.sw.drawtree(iterations, maxiter),
            self.se.drawtree(iterations, maxiter))
            if max(divmax) > maxiter:
                maxiter = max(divmax)
        return maxiter
            

            
            
            
class rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def contains(self, point):
        return(point[0] > self.x - self.w / 2 and point[0] < self.x + self.w / 2 and point[1] < self.y + self.h / 2 and point[1] > self.y - self.h / 2)
    
    
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    

def addobject(mass, x, y, xvel, yvel):
    objects.append((mass, x, y, xvel, yvel))

def save(list):
    with open("save.txt", "wb") as fp:
        pickle.dump(list, fp)


def calcmove():
    for indx, i in enumerate(objects):
        temp = list(objects[indx])
        temp[1] = i[1] + i[3] * STEPSIZE
        temp[2] = i[2] + i[4] * STEPSIZE
        objects[indx] = tuple(temp)

def findcom():
    com = [0, 0]
    for i in objects:
        com[0] = com[0] + i[1] / len(objects)
        com[1] = com[1] + i[2] / len(objects)
    return com

def buildtree():
    size = findsize()
    bounds = rect(0, 0, size * 2, size * 2)
    global tree
    tree = quadtree(bounds)

    for i in objects:
        point = (i[1], i[2])
        tree.insert(point)

def mean(list):
    return sum(list)/len(list)
    
    
def drawquad():
    global lastmax
    global usedmax
    recentmax.pop(0)
    recentmax.append(lastmax)
    usedmax = mean(recentmax)
    lastmax = tree.drawtree(1, 0)
    
    
def squareup(x):
    x = x + 0.01
    return 2 ** math.ceil(math.log(x) / math.log(2))

def findsize():
    list = []
    for i in objects:
        list.append(squareup(max(abs(i[1]), abs(i[2]))))
    return math.ceil(max(list))
    
def galaxy(n, size):
    addobject(100, 0, 0, 0, 0)
    for i in range(n):
        rot = random.uniform(0, math.radians(360))
        objsize = random.randint(30, size)
        speed = math.sqrt(100 / objsize)
        addobject(0.05, math.sin(rot) * objsize, math.cos(rot) * objsize, math.sin(rot + 1.57) * speed, math.cos(rot + 1.57) * speed)
        
        
def iterate():
    if Buildtree:
        buildtree()
    for indx, i in enumerate(objects):
        relative = (0, 0)
        for num, j in enumerate(objects):
            if num != indx:
                dist = math.sqrt((j[1] - i[1]) ** 2 + (j[2] - i[2]) ** 2) + 0.5
                relative = (relative[0] + ((j[0] * (j[1] - i[1])) / dist ** 3) * STEPSIZE, relative[1] + ((j[0] * (j[2] - i[2])) / dist ** 3) * STEPSIZE)
        objects[indx] = (objects[indx][0], objects[indx][1], objects[indx][2], objects[indx][3] + relative[0], objects[indx][4] + relative[1])
    calcmove()
    temp = []
    for i in objects:
        temp.append(i)
    recording.append(temp)

def gensquare(number, x, y):
    root = int(math.floor(math.sqrt(number)))
    for i in range(int(y / -2), root, int(y / root)):
        for j in range(int(x / -2), root, int(x / root)):
            addobject(1, i + random.randint(-5, 5), j + random.randint(-5, 5), 0, 0) # format (mass, x, y, xvel, yvel)

def randbox(number, size):
    for i in range(number):
        addobject(5, random.randint(-size, size), random.randint(-size, size), 0, 0)

def normalize(point):
    x = round(point[0] / scale + WIDTH / 2)
    y = round(point[1] / scale + HEIGHT / 2)
    return((x, y))

galaxy(50, 250)

def draw():
    WIN.fill((0, 0, 0))
    com = findcom()
    if Drawtree:
        drawquad()
    for i in objects:
        pygame.draw.circle(WIN, (0, 255, 0), (round(lagger[0]) / scale + WIDTH / 2, round(lagger[1]) / scale + HEIGHT / 2), 5)
        pygame.draw.line(WIN, WHITE, ((i[1]) / scale + WIDTH / 2, (i[2]) / scale + HEIGHT / 2), ((i[1] - i[3] * STEPSIZE ** 2) / scale + WIDTH / 2, (i[2] - i[4] * STEPSIZE ** 2) / scale + HEIGHT / 2), 1)
    
    textsurface = GAME_FONT.render(str(int(clock.get_fps())), False, (255, 255, 255))
    WIN.blit(textsurface, (0, 0))
    pygame.display.update()



def main():
    n = 0
    if reviewing:
        with open("save.txt", "rb") as fp:
            rerunning = pickle.load(fp)
    global objects
    global clock
    clock = pygame.time.Clock()
    run = True
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if reviewing:
            objects = rerunning[n]
            if n + 1 == len(rerunning):
                run = False
            if Buildtree:
                treetime = pygame.time.get_ticks()
                buildtree()
                print('tree time:' + str(pygame.time.get_ticks() - treetime))
        else:
            iterate()
        draw()
        n = n + 1
        
    if not reviewing:
        saved = input('save recording?')
        if saved == 'yes':
            save(recording)
    pygame.quit()




if __name__ == "__main__":

        
    main()


