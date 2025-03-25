from sprite_with_frames import SpriteWithFrames

IMAGE_URL = "./assets/images/pipo-battlebg002.jpg"
IMAGE_ROWS = 1
IMAGE_COLS = 1
SPRITE_WIDTH = 768
SPRITE_HEIGHT = 576

class Background(SpriteWithFrames):
    def __init__(self, surface):
        super().__init__(
            surface=surface,
            pos=(0, 0),
            image_url=IMAGE_URL,
            image_cols=IMAGE_COLS,
            image_rows=IMAGE_ROWS,
            sprite_width=SPRITE_WIDTH,
            sprite_height=SPRITE_HEIGHT,
        )

    def update(self):
        pass

    def draw(self):
        super().draw(
            magnification_rate=1,
            is_center=False,
        )
