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

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
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
            "ImageTexture": object.ImageTexture,
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
        newObject.Object.update(object["Position"][0], object["Position"][1], 32, 32)
        newObject.Texture(object["ImageTexture"])

def screen_to_world(screen_x, screen_y):
    screen_width, screen_height = screen.get_width(), screen.get_height()
    scale_x, scale_y = cam.zoom, cam.zoom
    camera_x, camera_y = cam.pos.x, cam.pos.y
    normalized_x = (screen_x - screen_width / 2) / scale_x
    normalized_y = (screen_y - screen_height / 2) / scale_y

    world_x = normalized_x + camera_x
    world_y = normalized_y + camera_y
    
    return world_x, world_y

def world_to_screen(world_x, world_y):
    screen_width, screen_height = screen.get_width(), screen.get_height()
    scale_x, scale_y = cam.zoom, cam.zoom
    camera_x, camera_y = cam.pos.x, cam.pos.y
    screen_x = (world_x - camera_x) * scale_x + screen_width / 2
    screen_y = (world_y - camera_y) * scale_y + screen_height / 2
    
    return screen_x, screen_y

mainBrush = eng.Brush()
bucket = eng.Brush()
def fill(pos):
    pass
bucket.paint = fill

while running:
    screen.fill("black")
    #fillPreserve(preview, pygame.Color((255, 255, 255)))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
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
            if cam.zoom >= 2.0:
                cam.zoom = 2.0
            elif cam.zoom <= 0.2:
                cam.zoom = 0.2
            print(cam.zoom)

    x,y = pygame.mouse.get_pos()
    x = x - (preview.get_width() / 2)
    y = y - (preview.get_height() / 2)

    colliding = False

    cam.update()
    
    mouseWorld = pygame.Vector2(screen_to_world(x, y))
    mouseWorld = pygame.Vector2(snap(mouseWorld.x, 32), snap(mouseWorld.y, 32))
    position = pygame.Vector2(world_to_screen(mouseWorld.x, mouseWorld.y))

    for object in eng.workspace:
        if object.Object.collidepoint(mouseWorld.x, mouseWorld.y):
            colliding = True

    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        if colliding == False:
            mainBrush.paint(mouseWorld, "assets/textures/blocks/brick.png")

    elif pygame.mouse.get_pressed()[2]:
        if colliding == True:
            for object in eng.workspace:
                if object.Object.x == mouseWorld.x and object.Object.y == mouseWorld.y:
                    index = eng.workspace.index(object)
                    eng.workspace.pop(index)

    #Render Objects
    for object in eng.workspace:
        if object.Shape == "Rectangle":
            if not object.ImageTexture == None:
                local = pygame.Vector2(world_to_screen(object.Object.x, object.Object.y))
                if local.x < 0 or local.x > screen.get_width():
                    continue
                if local.y < 0 or local.y > screen.get_height():
                    continue
                surfaceObject = object.Image

                surfaceObject = pygame.transform.scale(surfaceObject, pygame.Vector2(object.Object.w * cam.zoom, object.Object.h * cam.zoom))
                zoomPos = pygame.Vector2(world_to_screen(object.Object.x, object.Object.y))
                screen.blit(surfaceObject, (
                zoomPos.x
                ,
                zoomPos.y
                ))
        elif object.Shape == "Circle":
            pass

    preview.set_alpha(150)
    preview = pygame.transform.scale(preview, pygame.Vector2(32 * cam.zoom, 32 * cam.zoom))

    previewPosition = position

    screen.blit(preview, (previewPosition.x, previewPosition.y))

    pygame.display.flip()

    dt = clock.tick(144) / 1000

pygame.quit()