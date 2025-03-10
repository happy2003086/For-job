import random

class Game:
    def __init__(self, player_name, ai_name):
        self.players = [player_name, ai_name]  # 玩家同AI
        self.positions = {player_name: 0, ai_name: 0}  # 每個玩家嘅位置
        self.winner = None

    def roll_dice(self):
        return random.randint(1, 6)  # 每次擲骰子，隨機 1 到 6 點

    def move_player(self, player, dice_roll):
        self.positions[player] += dice_roll
        if self.positions[player] >= 30:  # 假設30格為終點
            self.positions[player] = 30
            self.winner = player
            print(f"恭喜 {player} 贏咗！")

    def print_board(self):
        print("飛行棋棋盤:")
        for player, position in self.positions.items():
            print(f"{player}: {'-' * position}{'>'} ({position})")

    def play_turn(self, player):
        # 等待玩家按 Enter 擲骰
        input(f"{player} 嘅回合，撳 Enter 擲骰子！")
        dice_roll = self.roll_dice()
        print(f"{player} 擲咗骰子: {dice_roll}")
        self.move_player(player, dice_roll)
        self.print_board()

    def play_game(self):
        while self.winner is None:
            for player in self.players:
                if self.winner:
                    break
                self.play_turn(player)

# 主程序
player_name = "玩家"  # 你嘅名字
ai_name = "AI"  # AI 嘅名字
game = Game(player_name, ai_name)
game.play_game()
