import random
import time

# 初始化游戏
width, height = 10, 10  # 10x10 的地图
snake = [[5, 5]]  # 蛇的初始位置
food = [random.randint(0, width - 1), random.randint(0, height - 1)]
direction = "d"  # 初始方向向右

def print_board():
    board = [["." for _ in range(width)] for _ in range(height)]
    for x, y in snake:
        board[y][x] = "#"
    board[food[1]][food[0]] = "*"
    
    for row in board:
        print(" ".join(row))
    print("\n控制方式: W (上), A (左), S (下), D (右)")

while True:
    print_board()
    move = input("输入 w/a/s/d 控制蛇: ").strip().lower()
    if move in ["w", "a", "s", "d"]:
        direction = move  # 更新方向

    # 计算新位置
    head = [snake[0][0], snake[0][1]]
    if direction == "w":
        head[1] -= 1
    elif direction == "s":
        head[1] += 1
    elif direction == "a":
        head[0] -= 1
    elif direction == "d":
        head[0] += 1

    # 判断是否撞墙或撞自己
    if head in snake or not (0 <= head[0] < width and 0 <= head[1] < height):
        print("游戏结束!")
        break

    # 移动蛇
    snake.insert(0, head)
    if head == food:
        food = [random.randint(0, width - 1), random.randint(0, height - 1)]  # 生成新的食物
    else:
        snake.pop()  # 移除尾巴

    time.sleep(0.5)  # 让游戏有节奏
