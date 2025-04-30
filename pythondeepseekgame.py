import random
import time
import sys

class Player:
    def __init__(self):
        self.health = 100
        self.hunger = 50
        self.thirst = 50
        self.energy = 80
        self.inventory = []
        self.shelter = False
        self.fire = False
        self.day = 1
        self.location = "沙灘"
    
    def status(self):
        print(f"\n=== 第 {self.day} 天 ===")
        print(f"位置: {self.location}")
        print(f"健康: {self.health}/100")
        print(f"飢餓: {self.hunger}/100")
        print(f"口渴: {self.thirst}/100")
        print(f"精力: {self.energy}/100")
        print("物品:", ", ".join(self.inventory) if self.inventory else "無")
        print("庇護所:", "已建立" if self.shelter else "無")
        print("火源:", "已點燃" if self.fire else "無")
    
    def update_stats(self):
        self.hunger += random.randint(5, 10)
        self.thirst += random.randint(5, 10)
        self.energy -= random.randint(5, 15)
        
        if self.hunger >= 80:
            self.health -= 5
            print("\n警告: 你太餓了，健康值下降！")
        if self.thirst >= 80:
            self.health -= 5
            print("\n警告: 你太渴了，健康值下降！")
        if self.energy <= 20:
            self.health -= 3
            print("\n警告: 你太累了，健康值下降！")
        
        if self.hunger > 100: self.hunger = 100
        if self.thirst > 100: self.thirst = 100
        if self.energy < 0: self.energy = 0
        if self.health <= 0:
            print("\n遊戲結束！你沒能在荒島上生存下來...")
            sys.exit()
    
    def new_day(self):
        self.day += 1
        self.energy = min(100, self.energy + 30)
        if self.shelter:
            self.health = min(100, self.health + 10)
        self.update_stats()

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def intro():
    slow_print("""
    荒島求生：命運之島
    
    你的飛機在太平洋上空遭遇了可怕的風暴。在一陣劇烈的顛簸後，你失去了意識...
    
    當你醒來時，發現自己躺在一個陌生島嶼的沙灘上。海浪拍打著海岸，四周是茂密的叢林，
    遠處有高聳的山脈。飛機殘骸散落在沙灘上，但沒有其他生還者的跡象。
    
    你必須利用有限的資源，在這個荒島上生存下去，直到救援到來...
    或者找到逃離的方法。
    
    你的生存冒險現在開始！
    """)

def explore_beach(player):
    options = {
        '1': ("搜索沙灘", search_beach),
        '2': ("前往叢林邊緣", explore_jungle_edge),
        '3': ("檢查飛機殘骸", check_wreckage),
        '4': ("返回主選單", None)
    }
    
    while True:
        player.location = "沙灘"
        print("\n你站在金色的沙灘上。面前是無邊無際的大海，身後是茂密的叢林。")
        print("你可以:")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        
        choice = input("你的選擇: ")
        if choice in options:
            if options[choice][1] is None:
                return
            options[choice][1](player)
        else:
            print("無效選擇，請重試。")

def search_beach(player):
    slow_print("\n你沿著沙灘漫步，尋找可能有用的物品...")
    time.sleep(2)
    
    found_items = [
        ("椰子", 30),
        ("漂流木", 20),
        ("空瓶子", 15),
        ("塑膠桶", 10),
        ("漁網碎片", 5),
        ("什麼都沒找到", 20)
    ]
    
    item = random.choices([i[0] for i in found_items], weights=[i[1] for i in found_items])[0]
    
    if item != "什麼都沒找到":
        slow_print(f"你找到了: {item}！")
        player.inventory.append(item)
    else:
        slow_print("這次搜索一無所獲。")
    
    player.energy -= 15
    player.update_stats()

def check_wreckage(player):
    if "已搜索殘骸" in player.inventory:
        slow_print("\n飛機殘骸已經被徹底搜索過了，沒有更多有用的東西。")
        return
    
    slow_print("""
    \n你走近飛機殘骸。機身已經斷裂成幾部分，大部分被海水侵蝕。
    你小心翼翼地搜索可能有用的物品...
    """)
    time.sleep(3)
    
    items = [
        ("急救包", "健康值恢復50點"),
        ("金屬片", "可用於製作工具"),
        ("打火機", "可以生火"),
        ("水瓶", "可以儲存淡水"),
        ("降落傘", "可用於製作庇護所")
    ]
    
    found = random.sample(items, 2)
    for item, desc in found:
        slow_print(f"你找到了: {item} - {desc}")
        player.inventory.append(item)
    
    player.inventory.append("已搜索殘骸")
    player.energy -= 20
    player.update_stats()

def explore_jungle_edge(player):
    options = {
        '1': ("進入叢林", explore_jungle),
        '2': ("沿著叢林邊緣行走", walk_jungle_edge),
        '3': ("返回沙灘", None)
    }
    
    while True:
        player.location = "叢林邊緣"
        print("\n你站在叢林的邊緣。茂密的植被讓人難以看清內部，但你能聽到鳥叫和未知動物的聲音。")
        print("你可以:")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        
        choice = input("你的選擇: ")
        if choice in options:
            if options[choice][1] is None:
                return
            options[choice][1](player)
        else:
            print("無效選擇，請重試。")

def explore_jungle(player):
    slow_print("""
    \n你小心翼翼地進入叢林。陽光透過樹葉斑駁地灑在地面上。
    空氣中瀰漫著潮濕的泥土氣息和植物的芬芳。
    """)
    
    events = [
        ("你發現了一棵果樹，摘了一些水果。", "獲得水果", 15),
        ("你被荊棘劃傷了。", "健康值-10", -10),
        ("你發現了一條清澈的小溪，喝了些水。", "口渴值-30", 0),
        ("你迷路了一陣子才找到回去的路。", "精力-20", 0),
        ("你發現了一些有用的草藥。", "獲得草藥", 10)
    ]
    
    event = random.choice(events)
    slow_print(event[0])
    
    if event[1].startswith("獲得"):
        player.inventory.append(event[1][3:])
    elif event[1] == "健康值-10":
        player.health -= 10
    elif event[1] == "口渴值-30":
        player.thirst = max(0, player.thirst - 30)
    elif event[1] == "精力-20":
        player.energy -= 20
    
    player.energy -= 25
    player.update_stats()

def walk_jungle_edge(player):
    slow_print("\n你沿著叢林邊緣行走，希望能發現些什麼...")
    time.sleep(2)
    
    discoveries = [
        ("你發現了一個洞穴入口。", "發現洞穴"),
        ("你看到遠處有煙升起！可能是救援？", "看到煙霧"),
        ("你發現了一片竹林，可以獲取建材。", "獲得竹子"),
        ("你什麼特別的都沒發現。", "無")
    ]
    
    discovery = random.choice(discoveries)
    slow_print(discovery[0])
    
    if discovery[1] == "獲得竹子":
        player.inventory.append("竹子")
    elif discovery[1] == "發現洞穴":
        explore_cave(player)
    
    player.energy -= 15
    player.update_stats()

def explore_cave(player):
    slow_print("""
    \n你進入洞穴。裡面黑暗潮濕，但似乎能提供良好的庇護。
    你可以選擇深入探索或在入口處活動。
    """)
    
    options = {
        '1': ("深入洞穴", deep_cave),
        '2': ("在入口處搜索", cave_entrance),
        '3': ("離開洞穴", None)
    }
    
    while True:
        player.location = "洞穴"
        print("\n你在洞穴中。你可以:")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        
        choice = input("你的選擇: ")
        if choice in options:
            if options[choice][1] is None:
                return
            options[choice][1](player)
        else:
            print("無效選擇，請重試。")

def deep_cave(player):
    slow_print("\n你點燃一支火把，深入洞穴...")
    time.sleep(2)
    
    if random.random() < 0.3:
        slow_print("洞穴深處有一隻熊！你慌忙逃出，受了些傷。")
        player.health -= 20
    else:
        slow_print("你在洞穴深處發現了一些古老的壁畫和一個淡水池。")
        player.thirst = max(0, player.thirst - 40)
        if "古老壁畫" not in player.inventory:
            player.inventory.append("古老壁畫")
            slow_print("這些壁畫可能揭示了島嶼的秘密...")
    
    player.energy -= 30
    player.update_stats()

def cave_entrance(player):
    slow_print("\n你在洞穴入口處搜索...")
    time.sleep(2)
    
    if random.random() < 0.5:
        slow_print("你找到了一些乾燥的木柴和石頭。")
        player.inventory.extend(["木柴", "石頭"])
    else:
        slow_print("入口處沒有什麼特別的東西。")
    
    player.energy -= 15
    player.update_stats()

def craft(player):
    recipes = {
        "簡易庇護所": {"需求": ["漂流木", "竹子", "降落傘"], "效果": "建立庇護所"},
        "魚叉": {"需求": ["木棍", "金屬片"], "效果": "獲得魚叉"},
        "集水器": {"需求": ["空瓶子", "塑膠桶"], "效果": "獲得集水器"},
        "火堆": {"需求": ["木柴", "打火機"], "效果": "生火"}
    }
    
    print("\n可製作的物品:")
    for i, (item, recipe) in enumerate(recipes.items(), 1):
        req = ", ".join(recipe["需求"])
        print(f"{i}. {item} (需要: {req})")
    print(f"{len(recipes)+1}. 返回")
    
    choice = input("選擇要製作的物品: ")
    try:
        choice = int(choice)
        if choice == len(recipes)+1:
            return
        item = list(recipes.keys())[choice-1]
        recipe = recipes[item]
        
        if all(req in player.inventory for req in recipe["需求"]):
            slow_print(f"\n你成功製作了 {item}！")
            for req in recipe["需求"]:
                player.inventory.remove(req)
            
            if recipe["效果"] == "建立庇護所":
                player.shelter = True
            elif recipe["效果"] == "生火":
                player.fire = True
            else:
                player.inventory.append(item)
        else:
            slow_print("\n你缺少必要的材料。")
    except:
        print("無效選擇。")

def rest(player):
    slow_print("\n你決定休息恢復精力...")
    time.sleep(3)
    
    restore = random.randint(20, 40)
    if player.shelter:
        restore += 20
        slow_print("在庇護所中休息讓你恢復更多精力。")
    
    player.energy = min(100, player.energy + restore)
    player.health = min(100, player.health + 10)
    slow_print(f"你恢復了{restore}點精力。")
    
    if player.fire:
        player.hunger += 10
        slow_print("火堆讓你感到溫暖舒適。")
    else:
        player.hunger += 20
        slow_print("夜晚的寒冷讓你消耗更多能量。")
    
    player.new_day()

def try_rescue(player):
    if player.day < 7:
        slow_print("\n你嘗試發出求救信號，但可能還需要更多時間才會有救援。")
        return
    
    chance = min(90, 30 + player.day * 5)
    if player.fire: chance += 20
    
    slow_print("\n你嘗試用各種方法發出求救信號...")
    time.sleep(3)
    
    if random.randint(1, 100) <= chance:
        slow_print("""
        遠處傳來引擎的聲音！一艘船看到了你的信號，正向島嶼駛來。
        
        經過艱苦的生存挑戰，你終於獲救了！
        
        恭喜你成功在荒島上生存了{}天並獲救！
        """.format(player.day))
        sys.exit()
    else:
        slow_print("這次沒有救援到來...不要放棄希望！")
    
    player.energy -= 20
    player.update_stats()

def main_menu(player):
    while True:
        player.status()
        print("\n主選單:")
        print("1. 探索")
        print("2. 製作")
        print("3. 休息")
        print("4. 嘗試求救")
        print("5. 退出遊戲")
        
        choice = input("選擇行動: ")
        
        if choice == "1":
            explore_beach(player)
        elif choice == "2":
            craft(player)
        elif choice == "3":
            rest(player)
        elif choice == "4":
            try_rescue(player)
        elif choice == "5":
            print("感謝遊玩荒島求生！")
            sys.exit()
        else:
            print("無效選擇，請重試。")

def main():
    intro()
    player = Player()
    main_menu(player)

if __name__ == "__main__":
    main()