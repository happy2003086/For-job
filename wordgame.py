import nltk
from nltk.corpus import words

# 下载 words 数据集
nltk.download('words')

# 获取单词列表
word_list = set(words.words())  # 使用 set 来加速查找

# 初始化已使用单词集合
used_words = set()
last_word = None  # 用于跟踪上一个单词

# 英文接龙游戏
def play_word_chain():
    global last_word
    print("欢迎来到英文接龙游戏！")
    print("请输入一个单词，接下来请输入一个以该单词最后一个字母开始的单词。")
    print("如果输入的单词不在字典中、已被使用或不符合接龙规则，游戏结束。")

    while True:
        # 玩家输入
        player_word = input("请输入一个单词: ").lower()

        # 检查玩家输入的单词是否有效
        if player_word not in word_list:
            print(f"这个单词 {player_word} 不在字典中，游戏结束！")
            break  # 如果单词不在字典中，游戏结束

        if player_word in used_words:
            print(f"这个单词 {player_word} 已经被用过了，游戏结束！")
            break  # 如果单词已被用过，游戏结束

        # 如果是第一个单词，不检查接龙规则
        if last_word is not None:
            last_char = last_word[-1]  # 上一个单词的最后一个字母

            # 如果玩家输入的单词不以最后一个字母开始，游戏结束
            if player_word[0] != last_char:
                print(f"你的单词 {player_word} 必须以 {last_char} 开头，游戏结束！")
                break

        # 添加玩家输入的单词到已使用的单词集合中
        used_words.add(player_word)
        last_word = player_word  # 更新最后一个单词

        # 根据最后一个字母找一个新的单词
        last_char = player_word[-1]
        next_word = next((word for word in word_list if word[0] == last_char and word not in used_words), None)

        if next_word:
            print(f"计算机选择的单词是: {next_word}")
            used_words.add(next_word)
            last_word = next_word  # 更新最后一个单词
        else:
            print(f"计算机没有找到以 {last_char} 开头的单词，游戏结束！")
            break

# 启动游戏
play_word_chain()