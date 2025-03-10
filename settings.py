IS_DEBUG_MODE = False

# ウィンドウサイズ
WIDTH = 800
HEIGHT = 600

# ウィンドウタイトル
TITLE = "くらりのプラットフォーマー"

# FPS
FPS = 60

# 1マスの大きさ
GRID_SIZE = 40

# 色
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

# プレイヤーの挙動に関する設定
PLAYER_MAX_SPEED = 5  # プレイヤーの最大速度
PLAYER_ACCELERATION = 0.5  # プレイヤーの加速度
PLAYER_GRAVITY = 1  # プレイヤーの重力
PLAYER_JUMP_POWER = 11  # プレイヤーのジャンプ力

# ステージファイル
STAGE_FILE_NAMES = [
    "Stage1.json",
    "Stage2.json",
    "Stage3.json",
    "Stage4.json",
]
