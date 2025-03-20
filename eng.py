import pygame

workspace = []
class Object:
    def __init__(self, position):
        self.Position = position or pygame.Vector2()
        workspace.append(self)
        self.Id = len(workspace) - 1

        self.Shape = "Rectangle"
        self.Object = pygame.Rect(self.Position.x, self.Position.y, 10, 10)
        self.Colour = pygame.Color(255, 255, 255)
        self.Texture = None
    def Destroy(self):
        workspace.pop(self.Id)
    def Scale(self, newSize):
        self.Object.update(self.Position.x - newSize.x/2 , self.Position.y - newSize.y/2, newSize.x, newSize.y)
    def update(self):
        if self.Texture != None:
            self.Image = pygame.image.load(self.Texture).convert_alpha()

class Entity(Object):
    def __init__(self, position):
        Object.__init__(self, position)


class Camera():
    def __init__(self, position):
        self.pos = position
        self.zoom = 1
        self.keys = {
            "w" : False,
            "s" : False,
            "a" : False,
            "d" : False,
        }
    def update(self):
        if self.keys["w"]:
            self.pos += pygame.Vector2(0, 32)
        if self.keys["s"]:
            self.pos += pygame.Vector2(0, -32)
        if self.keys["a"]:
            self.pos += pygame.Vector2(32, 0)
        if self.keys["d"]:
            self.pos += pygame.Vector2(-32, 0)
        #print(self.pos)
    def offset(self, x):
        return x - self.zoom
    def positionOffset(self, x, horizontal):
        if horizontal:
            return x - self.pos.x
        else:
            return x - self.pos.y