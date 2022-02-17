import pygame
import pygame.freetype
import math
import random
import pickle
import treelib

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('N Body Simulation')
pygame.init()
FPS = 60
WHITE = (255, 255, 255)
STEPSIZE = 0.1
objects = []
recording = []
GAME_FONT = pygame.font.Font("Montserrat-VariableFont_wght.ttf", 24)
reviewing = True
scale = 5

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
    
    quadtree = treelib.quadtree()   
    quadtree.create_node("Root", "root", data=objects(objects))
    recurse(quadtree.node("Root"))
    
def findsize():
    list = []
    for i in objects:
        list.append(max(abs(i[0]), abs(i[1])))
    return math.ceil(max(list))
    
def recurse(node):
    for i in node:
        pass
         
        
        
def iterate():
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
            addobject(1, i + random.randint(-5, 5), j + random.randint(-5, 5), 0, 0)

def randbox(number, size):
    for i in range(number):
        addobject(5, random.randint(-size, size), random.randint(-size, size), 0, 0)


randbox(2000, 250)

def draw():

    WIN.fill((0, 0, 0))
    com = findcom()
    for i in objects:
        pygame.draw.circle(WIN, (255, 0, 0), (round(com[0]) / scale + WIDTH / 2, round(com[1]) / scale + HEIGHT / 2), 5)
        pygame.draw.line(WIN, WHITE, ((i[1]) / scale + WIDTH / 2, (i[2]) / scale + HEIGHT / 2), ((i[1] - i[3] * STEPSIZE ** 2) / scale + WIDTH / 2, (i[2] - i[4] * STEPSIZE ** 2) / scale + HEIGHT / 2), 1)
    textsurface = GAME_FONT.render(str(int(clock.get_fps())), False, (255, 255, 255))
    size = findsize()
    pygame.draw.rect(WIN, (0, 255, 0), (size / -scale + WIDTH / 2, size / -scale + HEIGHT / 2, size * 2 / scale, size * 2 / scale), 3)
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


