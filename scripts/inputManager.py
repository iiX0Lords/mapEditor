import pygame

inputs = []

class Input():
    def __init__(self, key):
        self.Key = key
        self.IsPressed = False
        inputs.append(self)

    def OnDown(self):
        pass

    def OnUp(self):
        pass



def HandleInputs(event):
    if event.type == pygame.KEYDOWN:
        for input in inputs:
            if input.Key == event.key:
                input.OnDown(input)
    elif event.type == pygame.KEYUP:
        for input in inputs:
            if input.Key == event.key:
                input.OnUp(input)