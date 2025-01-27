from player import Player


class Stage:
    def __init__(self, surface):
        self.surface = surface
        self.player = Player(self.surface)

    def update(self):
        self.player.update()

    def draw(self):
        self.player.draw()
