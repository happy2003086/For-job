import random

class PasswordGame:
    def __init__(self):
        self.password = self.generate_password()
        self.attempts = 0  # Initialize attempt counter
    
    def generate_password(self):
        """Generate an 8-digit random password."""
        return ''.join(random.choices('0123456789', k=8))

    def check_guess(self, guess):
        """Check the user's guess against the generated password and provide feedback."""
        feedback = []
        
        for i in range(8):
            if guess[i] == self.password[i]:
                feedback.append(f"数字 {guess[i]}: ✓ (位置和数字都正确)")  # Checkmark for correct position and digit
            elif guess[i] in self.password:
                feedback.append(f"数字 {guess[i]}: ⚪ (数字正确但位置不正确)")  # Circle for correct digit but wrong position
            else:
                feedback.append(f"数字 {guess[i]}: ❌ (两种都不正确)")  # Cross for incorrect digit and position
        
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
            
            self.attempts += 1  # Increment attempts counter
            feedback = self.check_guess(guess)
            for result in feedback:
                print(result)
                
            if guess == self.password:
                print(f"恭喜你！你猜对了密码！你总共尝试了 {self.attempts} 次。")
                break  # End the game if the guess is correct

if __name__ == "__main__":
    game = PasswordGame()
    game.start_game()
