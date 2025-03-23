import tkinter
import tkinter.filedialog
import json
import pygame
import scripts.renderer as renderer

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

def export():

    exportArray = []
    for object in renderer.workspace:
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

    renderer.workspace = []

    for object in openedArray:
        print(object)
        newObject = renderer.Object(pygame.Vector2(0, 0))
        newObject.Object.update(object["Position"][0], object["Position"][1], 32, 32)
        newObject.Texture(object["ImageTexture"])