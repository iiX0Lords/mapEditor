import pygame
import scripts.renderer as renderer

class Camera():
    def __init__(self, position):
        self.pos = position
        self.zoom = 1
        self.speed = 15
        self.keys = {
            pygame.K_w : False,
            pygame.K_s : False,
            pygame.K_a : False,
            pygame.K_d : False,
        }
    def update(self):
        if self.keys[pygame.K_w]:
            self.pos += pygame.Vector2(0, -self.speed / self.zoom)
        if self.keys[pygame.K_s]:
            self.pos += pygame.Vector2(0, self.speed / self.zoom)
        if self.keys[pygame.K_a]:
            self.pos += pygame.Vector2(-self.speed / self.zoom, 0)
        if self.keys[pygame.K_d]:
            self.pos += pygame.Vector2(self.speed / self.zoom, 0)
    def Move(self, input):
        self.keys[input.Key] = True
    def Stop(self, input):
        self.keys[input.Key] = False
        

class Brush:
    def __init__(self):
        self.size = 1,
    def paint(self, pos, texture):
        newObject = renderer.Object(pygame.Vector2(0, 0))
        newObject.Texture(texture)
        newObject.Object.update(pos.x, pos.y, 32, 32)