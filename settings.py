IS_DEBUG_MODE = False

FONT_FILE_NAME = "PixelMplus12-Regular.ttf"
FONT_NAME = "PixelMplus12"

# ウィンドウサイズ
WIDTH = 768
HEIGHT = 576

# ウィンドウタイトル
TITLE = "くらりのプラットフォーマー"

# FPS
FPS = 60

# 1マスの大きさ
GRID_SIZE = 32

# 色
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "gray": (128, 128, 128),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "light_blue": (173, 216, 230),
    "light_green": (144, 238, 144),
    "light_gray": (211, 211, 211),
    "light_yellow": (255, 255, 224),
    "light_orange": (255, 218, 185),
    "light_purple": (221, 160, 221),
    "light_cyan": (224, 255, 255),
    "light_pink": (255, 182, 193),
    "light_brown": (210, 105, 30),
}

# プレイヤーの挙動に関する設定
PLAYER_MAX_SPEED = 5  # プレイヤーの最大速度
PLAYER_ACCELERATION = 0.5  # プレイヤーの加速度
PLAYER_GRAVITY = 1  # プレイヤーの重力
PLAYER_JUMP_POWER = 11  # プレイヤーのジャンプ力

# ステージファイル
STAGE_FILE_NAMES = [
    "n_stage1.json",
    "n_stage2.json",
    "n_stage3.json",
]
