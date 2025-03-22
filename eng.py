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

class Entity(Object):
    def __init__(self, position):
        Object.__init__(self, position)

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

class Camera():
    def __init__(self, position):
        self.pos = position
        self.zoom = 1
        self.speed = 15
        self.keys = {
            "w" : False,
            "s" : False,
            "a" : False,
            "d" : False,
        }
    def update(self):
        if self.keys["w"]:
            self.pos += pygame.Vector2(0, -self.speed / self.zoom)
        if self.keys["s"]:
            self.pos += pygame.Vector2(0, self.speed / self.zoom)
        if self.keys["a"]:
            self.pos += pygame.Vector2(-self.speed / self.zoom, 0)
        if self.keys["d"]:
            self.pos += pygame.Vector2(self.speed / self.zoom, 0)
    def offset(self, x):
        return x - self.zoom
    def positionOffset(self, x, horizontal):
        if horizontal:
            return x - self.pos.x
        else:
            return x - self.pos.y
        

class Brush:
    def __init__(self):
        self.size = 1,
    def paint(self, pos, texture):
        newObject = Object(pygame.Vector2(0, 0))
        newObject.Texture(texture)
        newObject.Object.update(pos.x, pos.y, 32, 32)