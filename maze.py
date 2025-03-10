import random

# 定義迷宮大小
WIDTH, HEIGHT = 21, 21  # 使用奇數以確保邊界和通道

def initialize_maze(width, height):
    return [['#' for _ in range(width)] for _ in range(height)]

def generate_maze(maze, x, y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # 右、下、左、上
    random.shuffle(directions)  # 隨機化方向

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 1 <= nx < WIDTH - 1 and 1 <= ny < HEIGHT - 1 and maze[ny][nx] == '#':
            maze[y + dy // 2][x + dx // 2] = ' '  # 打通牆壁
            maze[ny][nx] = ' '  # 打通新的位置
            generate_maze(maze, nx, ny)  # 遞迴生成

def print_maze(maze, player_pos):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if (y, x) == player_pos:
                print('P', end=' ')  # 玩家位置
            else:
                print(maze[y][x], end=' ')
        print()
    print()

def move_player(maze, player_pos, direction):
    y, x = player_pos
    if direction == 'w' and maze[y-1][x] == ' ':
        return (y-1, x)
    elif direction == 's' and maze[y+1][x] == ' ':
        return (y+1, x)
    elif direction == 'a' and maze[y][x-1] == ' ':
        return (y, x-1)
    elif direction == 'd' and maze[y][x+1] == ' ':
        return (y, x+1)
    return player_pos

def maze_game():
    maze = initialize_maze(WIDTH, HEIGHT)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = ' '  # 設定起點
    generate_maze(maze, start_x, start_y)

    # 設定入口和出口
    maze[1][0] = ' '  # 入口在迷宮左邊
    maze[HEIGHT-2][WIDTH-1] = ' '  # 出口在迷宮右下角

    player_pos = (start_y, start_x)  # 玩家初始位置

    while True:
        print_maze(maze, player_pos)
        if player_pos == (HEIGHT-2, WIDTH-1):  # 檢查是否到達出口
            print("恭喜，你成功走出了迷宮！")
            break

        print("使用 WASD 鍵移動（W: 上, A: 左, S: 下, D: 右）")
        direction = input("請輸入移動方向: ").lower()
        if direction in ['w', 'a', 's', 'd']:
            player_pos = move_player(maze, player_pos, direction)
        else:
            print("無效的輸入，請使用 W、A、S 或 D 鍵。")

# 開始遊戲
maze_game()
