import pygame

workspace = []
ui = []
class Object:
    def __init__(self, position):
        self.Position = position or pygame.Vector2()
        workspace.append(self)
        self.Id = len(workspace) - 1

        self.Shape = "Rectangle"
        self.Object = pygame.Rect(self.Position.x, self.Position.y, 10, 10)
        self.Colour = pygame.Color(255, 255, 255)
        self.ImageTexture = None
    def Destroy(self):
        workspace.pop(self.Id)
    def Scale(self, newSize):
        self.Object.update(self.Position.x - newSize.x/2 , self.Position.y - newSize.y/2, newSize.x, newSize.y)
    def Texture(self, img):
        self.ImageTexture = img
        self.Image = pygame.image.load(self.ImageTexture).convert_alpha()


class Frame:
    def __init__(self, position = pygame.Vector2(0, 0)):
        self.Position = position
        ui.append(self)
        self.Id = len(ui) - 1

        self.Colour = pygame.Color(255, 255, 255)
        self.Object = pygame.Rect(position.x, position.y, 10, 10)
        self.Size = pygame.Vector2(50, 50)
    def Destroy(self):
        ui.pop(self.Id)


def Render(screen, cam, hp):
    for object in workspace:
        if object.Shape == "Rectangle":
            if not object.ImageTexture == None:
                local = pygame.Vector2(hp.world_to_screen(object.Object.x, object.Object.y))
                if local.x < 0 or local.x > screen.get_width():
                    continue
                if local.y < 0 or local.y > screen.get_height():
                    continue
                surfaceObject = object.Image

                surfaceObject = pygame.transform.scale(surfaceObject, pygame.Vector2(object.Object.w * cam.zoom, object.Object.h * cam.zoom))
                zoomPos = pygame.Vector2(hp.world_to_screen(object.Object.x, object.Object.y))
                screen.blit(surfaceObject, (
                zoomPos.x
                ,
                zoomPos.y
                ))
        elif object.Shape == "Circle":
            pass