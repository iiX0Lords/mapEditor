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

display = pygame.display.set_mode((1280, 720))
screen = pygame.surface.Surface( (1280, 720) )
cam = eng.Camera(pygame.Vector2(0, 0))
clock = pygame.time.Clock()

running = True
dt = 0

preview = pygame.image.load("assets/textures/preview.png").convert_alpha()

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
            "Texture": object.Texture,
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
        newObject.Texture = object["Texture"]

def fillPreserve(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

while running:
    screen.fill("black")
    #fillPreserve(preview, pygame.Color((255, 255, 255)))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                cam.keys["w"] = True
            elif event.key == pygame.K_s:
                cam.keys["s"] = True
            if event.key == pygame.K_a:
                cam.keys["a"] = True
            elif event.key == pygame.K_d:
                cam.keys["d"] = True
            elif event.key == pygame.K_k:
                export()
            elif event.key == pygame.K_l:
                load()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                cam.keys["w"] = False
            elif event.key == pygame.K_s:
                cam.keys["s"] = False
            if event.key == pygame.K_a:
                cam.keys["a"] = False
            elif event.key == pygame.K_d:
                cam.keys["d"] = False
        if event.type == pygame.MOUSEWHEEL:
            cam.zoom += event.y / 10
            print(cam.zoom)

    x,y = pygame.mouse.get_pos()
    #x,y = x * cam.zoom, y * cam.zoom
    #x,y = x - cam.pos.x, y - cam.pos.y

    colliding = False

    cam.update()
    #cam.pos = pygame.Vector2(snap(cam.pos.x, 10), snap(cam.pos.y, 10))

    position = pygame.Vector2(
        x,
        y
    )

    position = pygame.Vector2(snap(x - 25, 50), snap(y - 25, 50))
    

    for object in eng.workspace:
        if object.Object.collidepoint(x - cam.pos.x, y - cam.pos.y):
            colliding = True

    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        if colliding == False:
            newObject = eng.Object(pygame.Vector2(0, 0))
            newObject.Texture = "assets/textures/blocks/brick.png"
            newObject.Object.update(position.x - cam.pos.x, position.y - cam.pos.y, 50, 50)
            print("new")
    elif pygame.mouse.get_pressed()[2]:
        #fillPreserve(preview, pygame.Color(255, 0, 0))
        if colliding == True:
            for object in eng.workspace:
                if object.Object.x == position.x and object.Object.y == position.y:
                    index = eng.workspace.index(object)
                    eng.workspace.pop(index)

    #Render Objects
    for object in eng.workspace:
        if object.Shape == "Rectangle":
            if not object.Texture == None:
                surfaceObject = pygame.image.load(object.Texture).convert_alpha()
                image_center = surfaceObject.get_rect().center
                surfaceObject = pygame.transform.scale(surfaceObject, pygame.Vector2(object.Object.w, object.Object.h))
                screen.blit(surfaceObject, (
                (object.Object.x + cam.pos.x)
                ,
                (object.Object.y + cam.pos.y)
                ))
        elif object.Shape == "Circle":
            pass

    preview.set_alpha(150)
    preview = pygame.transform.scale(preview, pygame.Vector2(50, 50))
    #screen.blit(preview, (cam.offset(position.x), cam.offset(position.y)))
    screen.blit(preview, (position.x, position.y))

    surface_mod = screen.copy()
    surface_mod_rect = surface_mod.get_rect()
    surface_mod = pygame.transform.rotozoom(surface_mod, 0, cam.zoom)
    surface_mod_rect = surface_mod.get_rect()

    display.fill("black")

    display.blit(surface_mod, surface_mod_rect)
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()