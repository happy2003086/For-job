import time
import sys

def typewriter_effect(text, speed=0.1, move_effect=False):
    """逐字顯示文字，並根據需要加入移動效果"""
    if move_effect:
        for i in range(10):
            sys.stdout.write("\r" + " " * i + "ufo")
            sys.stdout.flush()
            time.sleep(0.1)

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    
    print()  # 換行

def draw_ufo():
    """畫出簡單的 UFO"""
    ufo = """
         _______
        /       \\
       /_________\\
      |           |
     /             \\
    |_______________|
        |  |   |  |
        |  |   |  |
    """
    print(ufo)

def alien_kidnap():
    """模擬外星人綁架情節"""
    print("突然間，一道強光照亮了天空！你感覺到自己被吸了上去，無法反抗！")
    time.sleep(1)
    print("你發現自己被困在外星人的飛碟裡...")
    time.sleep(1)
    print("外星人看著你，露出邪惡的微笑。他們要做什麼？")
    time.sleep(1)

def make_choice():
    """讓用戶選擇反抗還是逃跑"""
    while True:
        choice = input("你想要反抗還是逃跑？ (輸入 '1' 反抗 或 '2' 逃跑): ")

        if choice == "1":
            print("你決定反抗！你用力推開外星人，然而他們的力量太強大了...")
            time.sleep(2)
            print("最終，你被制服了，但你仍然保持著不屈的精神！")
            break
        elif choice == "2":
            print("你決定逃跑！你迅速找到一個出口，成功地逃脫了飛碟！")
            time.sleep(2)
            print("你安全著陸，並決定再次與外星人作鬥爭！")
            break
        else:
            print("無效選擇，請輸入 '1' 反抗 或 '2' 逃跑")

# 用法範例
message = "很久很久以前，外星人(ufo)侵略地球。。。"
message2 = "現在你是守護地球的戰士"
draw_ufo()  # 畫 UFO
typewriter_effect(message, speed=0.1, move_effect=True)  # UFO 飛入
typewriter_effect(message2, speed=0.2)  # 顯示 "守護地球的戰士" 並放慢節奏

alien_kidnap()  # 外星人綁架情節
make_choice()  # 用戶選擇反抗還是逃跑
