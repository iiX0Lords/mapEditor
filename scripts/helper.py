import math

class init():
    def __init__(self, screen):
        self.screen = screen
        self.cam = None

    def snap(self, x, mult):
        return math.floor((x / mult) + 0.5) * mult

    def screen_to_world(self, screen_x, screen_y):
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        scale_x, scale_y = self.cam.zoom, self.cam.zoom
        camera_x, camera_y = self.cam.pos.x, self.cam.pos.y
        normalized_x = (screen_x - screen_width / 2) / scale_x
        normalized_y = (screen_y - screen_height / 2) / scale_y

        world_x = normalized_x + camera_x
        world_y = normalized_y + camera_y
        
        return world_x, world_y

    def world_to_screen(self, world_x, world_y):
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        scale_x, scale_y = self.cam.zoom, self.cam.zoom
        camera_x, camera_y = self.cam.pos.x, self.cam.pos.y
        screen_x = (world_x - camera_x) * scale_x + screen_width / 2
        screen_y = (world_y - camera_y) * scale_y + screen_height / 2
        
        return screen_x, screen_y