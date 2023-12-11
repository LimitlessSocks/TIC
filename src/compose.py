import sys
import os
import re
import json
import copy

from PIL import Image
from dataclasses import dataclass

# modified from https://stackoverflow.com/a/2669120/4119004
def natural_sort(xs):
    """ Sort the given iterable `xs` in the way that humans expect, with numbers sorted according to their numeric value as opposed to the ASCII values of their individual digits.""" 
    alphanum_key = lambda key: [
        int(text) if text.isdigit() else text
        for text in re.split("([0-9]+)", key)
    ] 
    return sorted(xs, key = alphanum_key)

@dataclass
class TICImageComponent:
    path: str
    size: (int, int)
    position: (int, int)

@dataclass
class TICTemplate:
    data: dict
    
    def __post_init__(self):
        if "size" not in self.data:
            if "width" in self.data and "height" in self.data:
                self.data["size"] = [ self.data["width"], self.data["height"] ]
        
        for layer_key, layer in self.layers().items():
            self.layers()[layer_key] = [
                TICImageComponent(
                    component["path"],
                    component["size"],
                    component["position"],
                )
                for component in layer
            ]
    
    def layers(self):
        return self.data["layers"]
    
    def size(self):
        return self.data["size"]
    
    def compose(self, **params):
        # TODO: allow background color to be parameterized
        # TODO: implement parameters
        base = Image.new("RGBA", self.size(), (0, 0, 0, 0))

        iterate_key_order = natural_sort(data["layers"].keys())

        for key in iterate_key_order:
            layer = data["layers"][key]
            for component in layer:
                image = Image.open(component.path)
                image = image.resize(component.size)
                # 3rd parameter to paste is alpha/clip channel
                base.paste(image, component.position, image)
        return base

if __name__ == "__main__":
    json_path = sys.argv[1]
    with open(sys.argv[1], "r") as json_file:
        data = json.load(json_file)

    # print(os.path.dirname(json_path))
    os.chdir(os.path.dirname(json_path))

    template = TICTemplate(data)
    result = template.compose()
    result.show()
