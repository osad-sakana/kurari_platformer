import json
import os


class Map:
    def __init__(self):
        self.map_data = []

    def update(self):
        pass

    def draw(self):
        pass

    def load_map(self, filename):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "maps", filename)
        with open(file_path, "r") as f:
            self.map_data = json.load(f)
