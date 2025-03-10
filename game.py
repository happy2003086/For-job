import random

class Player:
    def __init__(self):
        self.hp = 10
        self.sanity = 10
        self.inventory = []
        self.equipped_weapon = None

def start_game():
    player = Player()
    print("你在一间冰冷潮湿的牢房中醒来。空气中弥漫着腐烂的气味。一盏摇曳的火把照亮了一条通往黑暗深处的狭窄通道。")
    print("你必须逃离这里，否则就会被黑暗吞噬。你要怎么做？")
    choice1(player)

def choice1(player):
    print(f"\n你的生命值：{player.hp} | 你的理智：{player.sanity}")
    print("1. 调查牢房内是否有任何有用的物品。")
    print("2. 尝试打破牢房的门。")
    print("3. 聆听外面的声音。")
    print("4. 仔细检查火把。")

    choice = input("请输入你的选择：")

    if choice == "1":
        investigate_cell(player)
    elif choice == "2":
        break_door(player)
    elif choice == "3":
        listen_outside(player)
    elif choice == "4":
        examine_torch(player)
    else:
        print("无效的选择。请重试。")
        choice1(player)

def investigate_cell(player):
    # 有一定概率找到有用的物品，但也有一定概率遇到令人不安的景象
    if random.randint(1, 4) == 1:
        item = random.choice(["生锈的钥匙", "发霉的面包", "啃过的骨头", "钝刀"]) 
        player.inventory.append(item)
        print(f"\n你在一个隐蔽的角落里找到了{item}。")
        if item == "钝刀":
            print("你装备了钝刀。")
            player.equipped_weapon = "钝刀"
    else:
        player.sanity -= 1
        print("\n你撞见了一幅令人不安的壁画。它让你感到毛骨悚然。") 
    choice1(player)

def break_door(player):
    if "生锈的钥匙" in player.inventory:
        print("\n你使用生锈的钥匙打开了门。门发出嘎吱嘎吱的响声打开了。")
        escape_attempt(player) 
    else:
        if player.equipped_weapon:
            print(f"\n你试图用你的{player.equipped_weapon}打破门。")
            if random.randint(1, 2) == 1: 
                print("\n门碎裂了。你用力过猛，损失了1点生命值。")
                player.hp -= 1
                escape_attempt(player) 
            else:
                print(f"\n你的{player.equipped_weapon}折断了。你损失了1点生命值。")
                player.hp -= 1
                choice1(player)
        else:
            print("\n你试图徒手打破门。你损失了2点生命值。")
            player.hp -= 2
            choice1(player)

def listen_outside(player):
    if random.randint(1, 3) == 1:
        print("\n你听到远处传来低沉的咆哮声。")
        player.sanity -= 2
    else:
        print("\n除了滴水声和自己的呼吸声外，你什么也没听到。")
    choice1(player)

def examine_torch(player):
    if random.randint(1, 3) == 1:
        print("\n火把忽明忽暗，在墙上投下舞动的影子。你感到一阵寒意。")
        player.sanity -= 1
    else:
        print("\n火把提供了微弱但令人安心的光源，照亮了黑暗。")
    choice1(player)

def escape_attempt(player):
    print("\n你小心翼翼地走出牢房。通道阴暗潮湿。你听到远处传来微弱的、有节奏的砰砰声。")
    choice2(player)

def choice2(player):
    print(f"\n你的生命值：{player.hp} | 你的理智：{player.sanity}")
    print("1. 谨慎地沿着通道前进。")
    print("2. 退回到牢房中。")
    print("3. 大声呼救（有风险）。")

    choice = input("请输入你的选择：")

    if choice == "1":
        proceed_passage(player)
    elif choice == "2":
        retreat_cell(player)
    elif choice == "3":
        shout_for_help(player)
    else:
        print("无效的选择。请重试。")
        choice2(player)

def proceed_passage(player):
    # 在通道中遇到随机事件
    event = random.choice(["陷阱", "怪物", "死路", "宝藏"])

    if event == "陷阱":
        if player.equipped_weapon:
            print(f"\n你使用你的{player.equipped_weapon}拆除了陷阱。") 
        else:
            player.hp -= random.randint(1, 3)
            print("\n你触发了一个隐藏的陷阱！你损失了生命值。")
        if player.hp <= 0:
            game_over(player) 
        else:
            choice2(player) 
    elif event == "怪物":
        if player.equipped_weapon:
            print(f"\n你用你的{player.equipped_weapon}与怪物战斗。")
            if random.randint(1, 2) == 1:
                print("\n你击败了怪物！") 
            else:
                player.hp -= random.randint(2, 5)
                player.sanity -= 2
                print("\n你在战斗中受伤了！你损失了生命值和理智。")
                if player.hp <= 0:
                    game_over(player) 
        else:
            player.hp -= random.randint(2, 5)
            player.sanity -= 2
            print("\n你被怪物击垮了！你损失了生命值和理智。")
            if player.hp <= 0:
                game_over(player) 
        choice2(player) 
    elif event == "死路":
        player.sanity -= 1
        print("\n你到达了死路。通道在你身后坍塌，封锁了你的逃生之路。")
        choice2(player) 
    elif event == "宝藏":
        item = random.choice(["治愈药水", "锋利的匕首", "古老的护身符"]) 
        player.inventory.append(item)
        if item == "锋利的匕首":
            if player.equipped_weapon:
                print(f"\n你找到了{item}，但你已经装备了武器。")
            else:
                print(f"\n你发现了一个隐藏的宝藏，里面包含一把{item}！你装备了锋利的匕首。")
                player.equipped_weapon = "锋利的匕首"
        else:
            print(f"\n你发现了一个隐藏的宝藏，里面包含{item}！")
        choice2(player) 

def retreat_cell(player):
    print("\n你退回到牢房中，感到一阵恐惧。")
    choice1(player)

def shout_for_help(player):
    player.sanity -= 1
    if random.randint(1, 5) == 1:
        print("\n你的呼救得到了回应。一个神秘的身影靠近了...") 
        # 添加与神秘人物的新遭遇
    else:
        print("\n你的呼救声在空荡荡的走廊里回荡，无人回应。")
        choice2(player)

def game_over(player):
    if player.hp <= 0:
        print("\n你因伤势过重而死。")
    elif player.sanity <= 0:
        print("\n黑暗吞噬了你的心智。")
    print("游戏结束！")
    play_again()

def play_again():
    choice = input("是否重新开始游戏？(yes/no): ")
    if choice.lower() == "yes":
        start_game()
    else:
        print("感谢游戏！")

# 开始游戏
start_game()