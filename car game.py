import tkinter as tk
import random

# 初始化窗口
root = tk.Tk()
root.title("避開障礙物遊戲")
root.geometry("400x600")

# 設置車輛位置
car_width = 50
car_height = 80
car_x = 175
car_y = 500
car_speed = 20

# 障礙物設定
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacle_y = 0
obstacle_x = random.randint(0, 350)  # 初始化障礙物的水平位置

# 創建畫布
canvas = tk.Canvas(root, width=400, height=600)
canvas.pack()

# 創建車輛
car = canvas.create_rectangle(car_x, car_y, car_x + car_width, car_y + car_height, fill="blue")

# 創建障礙物
obstacle = canvas.create_rectangle(obstacle_x, obstacle_y, obstacle_x + obstacle_width, obstacle_y + obstacle_height, fill="red")

def move_car(event):
    global car_x
    # 根據觸控事件來移動車輛，event.x 是觸控的 x 坐標
    car_x = event.x - car_width / 2  # 車輛居中在觸控位置
    # 限制車輛移動範圍
    if car_x < 0:
        car_x = 0
    elif car_x > 400 - car_width:
        car_x = 400 - car_width
    canvas.coords(car, car_x, car_y, car_x + car_width, car_y + car_height)

def move_obstacle():
    global obstacle_x, obstacle_y  # 使用global來確保修改外部變量
    obstacle_y += obstacle_speed
    if obstacle_y > 600:  # 如果障礙物超出畫布
        obstacle_y = 0
        obstacle_x = random.randint(0, 350)  # 隨機生成障礙物的水平位置
    canvas.coords(obstacle, obstacle_x, obstacle_y, obstacle_x + obstacle_width, obstacle_y + obstacle_height)
    root.after(50, move_obstacle)

# 綁定觸控事件（點擊並拖動來移動車輛）
canvas.bind("<B1-Motion>", move_car)  # B1-Motion 代表左鍵拖動事件

# 開始移動障礙物
move_obstacle()

# 運行遊戲
root.mainloop()
