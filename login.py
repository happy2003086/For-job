import random

class PasswordGame:
    def __init__(self):
        self.password = self.generate_password()
    
    def generate_password(self):
        """生成一个八位数的随机密码"""
        return ''.join(random.choices('0123456789', k=8))

    def check_guess(self, guess):
        """检查用户输入的密码与生成的密码"""
        feedback = []
        
        for i in range(8):
            if guess[i] == self.password[i]:
                feedback.append(f"数字 {guess[i]}: 位置和数字都正确")
            elif guess[i] in self.password:
                feedback.append(f"数字 {guess[i]}: 数字正确但位置不正确")
            else:
                feedback.append(f"数字 {guess[i]}: 两种都不正确")
        
        return feedback

    def start_game(self):
        print("欢迎来到密码判断游戏！")
        print("系统已生成一个八位数的密码。")
        
        while True:
            guess = input("请输入你猜测的八位数密码（或输入'a'显示答案，或输入'退出'来结束游戏）：")
            if guess.lower() == '退出':
                print("游戏结束！正确密码是：{}".format(self.password))
                break
            elif guess.lower() == 'a':
                print(f"正确密码是：{self.password}")
                continue
            
            if len(guess) != 8 or not guess.isdigit():
                print("请输入一个有效的八位数字密码。")
                continue
            
            feedback = self.check_guess(guess)
            for result in feedback:
                print(result)

if __name__ == "__main__":
    game = PasswordGame()
    game.start_game()
