import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        self.volume = 1.0

    def load_sounds(self):
        # assets/se ディレクトリから全ての効果音をロード
        se_dir = os.path.join("assets", "se")
        for filename in os.listdir(se_dir):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                sound_name = os.path.splitext(filename)[0]  # 拡張子を除いたファイル名
                sound_path = os.path.join(se_dir, filename)
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)

    def play(self, sound_name):
        """効果音を再生する"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"警告: 効果音 '{sound_name}' が見つかりません")

    def set_volume(self, volume):
        """全ての効果音のボリュームを設定する (0.0 〜 1.0)"""
        self.volume = max(0.0, min(volume, 1.0))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
