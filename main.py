import pygame
import eng
import math
import json
import os

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True
dt = 0

preview = pygame.Surface((50, 50))


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

    with open("export.txt", "w") as file:
        file.write(json.dumps(exportArray))

while running:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                export()
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