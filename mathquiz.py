import random
import time

class MathQuiz:
    def __init__(self):
        self.questions_answered = 0  # 记录回答的问题数量
        self.time_left = 30  # 初始时间为30秒

    def generate_question(self):
        """生成随机的数学题目"""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(['+', '-', '*'])
        question = f"{num1} {operator} {num2}"
        answer = eval(question)
        return question, answer

    def start_quiz(self):
        print("欢迎来到计算测验！你有30秒的时间回答问题。")
        
        while self.time_left > 0:
            question, answer = self.generate_question()
            print(f"题目: {question} = ?")
            
            start_time = time.time()
            user_answer = input("请输入你的答案（或输入'退出'来结束游戏）：")
            end_time = time.time()
            
            # 检查是否退出
            if user_answer.lower() == '退出':
                print("游戏结束！你回答了 {} 道题目。".format(self.questions_answered))
                break
            
            # 检查用户输入的答案
            try:
                user_answer = int(user_answer)
            except ValueError:
                print("请输入一个有效的数字。")
                continue
            
            # 计算剩余时间
            time_taken = end_time - start_time
            self.time_left -= time_taken
            
            # 不加分，只调整剩余时间
            if user_answer == answer:
                print("答对了！")
            else:
                self.time_left -= 3  # 答错减3秒
                print("答错了！正确答案是 {}。".format(answer))

            self.questions_answered += 1  # 增加回答的问题数量
            print("剩余时间: {:.2f}秒\n".format(self.time_left))

        print("时间到！你回答了 {} 道题目。".format(self.questions_answered))

if __name__ == "__main__":
    quiz = MathQuiz()
    quiz.start_quiz()
