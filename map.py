import json
import os
from terrain import Terrain


class Map:
    def __init__(self, surface):
        self.map_data = []
        self.map_objects = []
        self.surface = surface

    def update(self):
        pass

    def draw(self):
        for obj in self.map_objects:
            obj.draw()

    def load_map(self, filename):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "maps", filename)
        with open(file_path, "r") as f:
            self.map_data = json.load(f)
        self._make_objects()

    def _make_objects(self):
        for y, row in enumerate(self.map_data["map_data"]):
            for x, cell in enumerate(row):
                terrain = Terrain(
                    self.surface, x, y, cell
                )
                self.map_objects.append(terrain)
