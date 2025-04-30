import random

# 創建 Bingo 卡片
def create_bingo_card():
    card = []
    # 每列的數字範圍
    ranges = {
        'B': (1, 15),
        'I': (16, 30),
        'N': (31, 45),
        'G': (46, 60),
        'O': (61, 75)
    }

    for col, (start, end) in ranges.items():
        column_numbers = random.sample(range(start, end + 1), 5)
        card.append(column_numbers)
    
    # 設定 Free Space
    card[2][2] = 'Free'

    return card

# 顯示 Bingo 卡片
def print_bingo_card(card):
    print(" B   I   N   G   O")
    for row in card:
        print("  ".join(f"{str(cell):<2}" for cell in row))

# 隨機抽取號碼
def draw_number(drawn_numbers):
    number = random.randint(1, 75)
    while number in drawn_numbers:
        number = random.randint(1, 75)
    drawn_numbers.add(number)
    return number

# 標記號碼
def mark_number(card, number):
    # 確定數字在卡片中的位置並標記
    for i in range(5):
        for j in range(5):
            if card[i][j] == number:
                card[i][j] = 'X'  # X 代表標記的數字
                return

# 檢查是否完成 Bingo（橫、直、斜）
def check_bingo(card):
    # 檢查行和列
    for i in range(5):
        if all(cell == 'X' for cell in card[i]):  # 檢查行
            return True
        if all(card[j][i] == 'X' for j in range(5)):  # 檢查列
            return True
    
    # 檢查斜線
    if all(card[i][i] == 'X' for i in range(5)):  # 斜線1
        return True
    if all(card[i][4 - i] == 'X' for i in range(5)):  # 斜線2
        return True
    
    return False

def play_bingo():
    card = create_bingo_card()
    print_bingo_card(card)

    drawn_numbers = set()
    while True:
        input("Press Enter to draw a number...")
        
        # 抽取號碼
        number = draw_number(drawn_numbers)
        print(f"Number drawn: {number}")
        
        # 標記號碼
        mark_number(card, number)
        print_bingo_card(card)
        
        # 檢查是否完成 Bingo
        if check_bingo(card):
            print("Bingo! You win!")
            break

# 開始遊戲
play_bingo()
