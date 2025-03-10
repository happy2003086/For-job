import pygame

# 初始化 pygame
pygame.mixer.init()

def play_music(file_path):
    try:
        # 加載音樂文件
        pygame.mixer.music.load(file_path)
        # 播放音樂
        pygame.mixer.music.play()
        print("音樂播放中...")
    except Exception as e:
        print(f"播放音樂時出錯: {e}")

# 音樂檔案的完整路徑
music_file = '/storage/emulated/0/Notifications/Yahoo_Got_Mail.mp3'

# 播放音樂
play_music(music_file)

# 保持程式運行直到音樂播放完畢
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
