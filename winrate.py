def calculate_win_rate(wins, losses):
    """
    計算勝率的函數。

    :param wins: 勝利次數
    :param losses: 失敗次數
    :return: 勝率（百分比形式）
    """
    total_games = wins + losses  # 總比賽次數
    if total_games == 0:
        return 0.0  # 避免除以零的情況

    win_rate = (wins / total_games) * 100  # 勝率計算
    return round(win_rate, 2)  # 四捨五入到小數點後兩位

# 讓用戶輸入勝利和失敗次數
try:
    wins = int(input("請輸入勝利次數: "))
    losses = int(input("請輸入失敗次數: "))

    # 計算並打印勝率
    win_rate = calculate_win_rate(wins, losses)
    print(f"勝率: {win_rate}%")
except ValueError:
    print("請確保您輸入的是有效的整數。")
