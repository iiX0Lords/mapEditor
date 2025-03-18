import pygame
import eng
import math
import json
import os
import tkinter
import tkinter.filedialog

pygame.init()

pygame.display.set_caption("Map qEditor")
pygame.display.set_icon(pygame.image.load("icon.png"))

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True
dt = 0

preview = pygame.Surface((50, 50))

def prompt_file(name = "exportedMap", write = False):
    top = tkinter.Tk()
    top.withdraw()
    file_name = None
    if write:
        file_name = tkinter.filedialog.asksaveasfile(mode="w", initialfile = name+".json",filetypes = (("JSON files","*.json"),("All Files","*.*")),parent=top)
    else:
        file_name = tkinter.filedialog.askopenfile(mode="r",filetypes = (("JSON files","*.json"),("All Files","*.*")),parent=top)
    top.destroy()
    return file_name

def snap(x, mult):
    return math.floor((x / mult) + 0.5) * mult

def export():

    exportArray = []
    for object in eng.workspace:
        exportArray.append({
            "Shape": object.Shape,
            "Colour": (object.Colour.r, object.Colour.g, object.Colour.b),
            "Position": (object.Object.x, object.Object.y)
        })

    file = prompt_file("exportedMap", True)
    if file == None:
        print("Didnt save")
        return
    file.write(json.dumps(exportArray))
        

def load(file = None):
    if file == None:
        file = prompt_file()
        if file == None:
            print("No file picked")
            return
        file = file.name
    file = open(file, "r")
    file = file.read()
    openedArray = json.loads(file)

    eng.workspace = []

    for object in openedArray:
        print(object)
        newObject = eng.Object(pygame.Vector2(0, 0))
        newObject.Object.update(object["Position"][0], object["Position"][1], 50, 50)
    

while running:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                export()
            elif event.key == pygame.K_s:
                load()
            elif event.key == pygame.K_k:
                load("export.json")
        if event.type == pygame.KEYUP:
            pass

    x,y = pygame.mouse.get_pos()
    colliding = False

    position = pygame.Vector2(snap(x - 25, 50), snap(y - 25, 50))

    for object in eng.workspace:
        if object.Object.collidepoint(x, y):
            colliding = True

    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        if colliding == False:
            newObject = eng.Object(pygame.Vector2(0, 0))
            newObject.Object.update(position.x, position.y, 50, 50)
    elif pygame.mouse.get_pressed()[2]:
        if colliding == True:
            for object in eng.workspace:
                if object.Object.x == position.x and object.Object.y == position.y:
                    index = eng.workspace.index(object)
                    eng.workspace.pop(index)

    #Render Objects
    for object in eng.workspace:
        if object.Shape == "Rectangle":
            pygame.draw.rect(screen, object.Colour, object.Object)
        elif object.Shape == "Circle":
            pygame.draw.circle(screen, object.Colour, pygame.Vector2(object.Object.x, object.Object.y), object.Object.w)

    preview.set_alpha(115)
    preview.fill((255, 255, 255))
    screen.blit(preview, (position.x, position.y))

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()