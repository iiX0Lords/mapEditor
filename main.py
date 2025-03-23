import pygame
import eng
import os
import scripts.filesystem as filesystem
import scripts.helper as helper
import scripts.inputManager as input
import scripts.renderer as renderer

pygame.init()

pygame.display.set_caption("Map qEditor")
pygame.display.set_icon(pygame.image.load("icon.png"))

base_width = 1280
base_height = 720
screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
hp = helper.init(screen)

running = True
clock = pygame.time.Clock()
dt = 0

cam = eng.Camera(pygame.Vector2(0, 0))
hp.cam = cam

preview = pygame.image.load("assets/textures/preview.png").convert_alpha()
blocks = []

class Block:
    def __init__(self, texture, name):
        self.Texture = texture
        self.Name = name
        blocks.append(self)
        self.Id = len(blocks) - 1

mainBrush = eng.Brush()

for name in os.listdir("assets/textures/blocks"):
    Name = name.replace(".png", "")
    Name = Name.capitalize()
    Block("assets/textures/"+name, Name)


# Init Functions

def file(key):
    if key.Key == pygame.K_k:
        filesystem.export()
    elif key.Key == pygame.K_l:
        filesystem.load()

def registerMovement():
    up = input.Input(pygame.K_w); up.OnDown = cam.Move; up.OnUp = cam.Stop
    down = input.Input(pygame.K_s); down.OnDown = cam.Move; down.OnUp = cam.Stop
    right = input.Input(pygame.K_d); right.OnDown = cam.Move; right.OnUp = cam.Stop
    left = input.Input(pygame.K_a); left.OnDown = cam.Move; left.OnUp = cam.Stop

    export = input.Input(pygame.K_k); export.OnDown = file
    load = input.Input(pygame.K_l); load.OnDown = file
registerMovement()

# Main Loop
while running:
    screen.fill("black")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
        if event.type == pygame.MOUSEWHEEL:
            cam.zoom += event.y / 10
            if cam.zoom >= 2.0:
                cam.zoom = 2.0
            elif cam.zoom <= 0.2:
                cam.zoom = 0.2
            print(cam.zoom)

        input.HandleInputs(event)

    x,y = pygame.mouse.get_pos()
    x = x - (preview.get_width() / 2)
    y = y - (preview.get_height() / 2)

    colliding = False

    cam.update()
    
    mouseWorld = pygame.Vector2(hp.screen_to_world(x, y)); mouseWorld = pygame.Vector2(hp.snap(mouseWorld.x, 32), hp.snap(mouseWorld.y, 32))
    position = pygame.Vector2(hp.world_to_screen(mouseWorld.x, mouseWorld.y))

    for object in renderer.workspace:
        if object.Object.collidepoint(mouseWorld.x, mouseWorld.y):
            colliding = True

    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        if colliding == False:
            mainBrush.paint(mouseWorld, "assets/textures/blocks/brick.png")

    elif pygame.mouse.get_pressed()[2]:
        if colliding == True:
            for object in renderer.workspace:
                if object.Object.x == mouseWorld.x and object.Object.y == mouseWorld.y:
                    index = renderer.workspace.index(object)
                    renderer.workspace.pop(index)

    #Render Objects
    renderer.Render(screen, cam, hp)

    preview.set_alpha(150)
    preview = pygame.transform.scale(preview, pygame.Vector2(32 * cam.zoom, 32 * cam.zoom))

    previewPosition = position

    screen.blit(preview, (previewPosition.x, previewPosition.y))


    pygame.display.flip()

    dt = clock.tick(144) / 1000

pygame.quit()