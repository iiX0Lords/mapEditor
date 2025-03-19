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


class Entity(Object):
    def __init__(self, position):
        Object.__init__(self, position)