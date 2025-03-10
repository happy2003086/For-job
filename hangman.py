import random
import nltk
from nltk.corpus import words

# 下载词汇数据
nltk.download('words')

def choose_word():
    word_list = words.words()  # 获取词汇列表
    return random.choice(word_list).lower()  # 随机选择单词并转换为小写

def display_hangman(tries):
    stages = [
        """
           -----
           |   |
           |   O
           |  /|\\
           |  / \\
           |
        """,
        """
           -----
           |   |
           |   O
           |  /|\\
           |  /
           |
        """,
        """
           -----
           |   |
           |   O
           |  /|
           |  
           |
        """,
        """
           -----
           |   |
           |   O
           |  
           |  
           |
        """,
        """
           -----
           |   |
           |  
           |  
           |  
           |
        """,
        """
           -----
           |   
           |  
           |  
           |  
           |
        """,
    ]
    return stages[tries]

def play():
    word = choose_word()
    guessed = set()
    tries = 5
    word_completion = "_" * len(word)
    
    print("Let's play Hangman!")
    
    while tries > 0 and "_" in word_completion:
        print(display_hangman(tries))
        print("Word:", " ".join(word_completion))
        print("Guessed letters:", " ".join(sorted(guessed)))
        
        guess = input("Please guess a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        if guess in guessed:
            print("You've already guessed that letter.")
            continue
        
        guessed.add(guess)
        
        if guess in word:
            print("Good guess!")
            word_completion = ''.join([letter if letter in guessed else "_" for letter in word])
        else:
            print("Sorry, that letter is not in the word.")
            tries -= 1
            
    if "_" not in word_completion:
        print("Congratulations! You've guessed the word:", word)
    else:
        print(display_hangman(tries))
        print("Sorry, you've run out of tries. The word was:", word)

if __name__ == "__main__":
    play()
