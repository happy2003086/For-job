import random

# 玩家類別
class Player:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.health = 100
        self.attack = 20
        self.level = 1
        self.inventory = []

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} 受到 {damage} 傷害，剩餘生命值：{self.health}")

    def heal(self):
        if "Potion" in self.inventory:
            self.health += 30
            self.inventory.remove("Potion")
            print(f"{self.name} 使用咗生命藥水，恢復 30 生命值！")
        else:
            print("你冇生命藥水！")

    def level_up(self):
        self.level += 1
        self.attack += 5
        self.health = 100
        print(f"恭喜！{self.name} 升級到 {self.level} 級，攻擊力提升至 {self.attack}！")

    def is_alive(self):
        return self.health > 0

# 怪物類別
class Monster:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} 受咗 {damage} 傷害，剩餘生命值：{self.health}")

    def is_alive(self):
        return self.health > 0

# 道具類別
class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, player):
        if self.effect == "heal":
            player.heal()
        elif self.effect == "boost":
            player.attack += 5
            print(f"{player.name} 使用咗攻擊藥水，攻擊力增加 5！")

# 遊戲主邏輯
def game():
    print("=== 歡迎來到 RPG 冒險遊戲！===")
    name = input("請輸入你的名字：")
    gender = input("請輸入你的性別 (M/F)：")

    player = Player(name, gender)

    # 預設怪物
    monsters = [
        Monster("史萊姆", 50, 10),
        Monster("骷髏兵", 80, 15),
        Monster("魔王", 150, 25)
    ]

    print(f"\n{name}，準備開始你的冒險之旅！\n")

    for monster in monsters:
        print(f"⚔️ 你遇到咗一隻 {monster.name}！")

        while player.is_alive() and monster.is_alive():
            print(f"\n你的生命值: {player.health} | {monster.name} 的生命值: {monster.health}")
            action = input("你想做咩？1: 攻擊 2: 使用道具 3: 逃跑：")

            if action == "1":
                damage = random.randint(10, player.attack)
                monster.take_damage(damage)
                if monster.is_alive():
                    monster_damage = random.randint(5, monster.attack)
                    player.take_damage(monster_damage)
            elif action == "2":
                player.heal()
            elif action == "3":
                print("你選擇咗逃跑！遊戲結束！")
                return
            else:
                print("輸入錯誤，請重新選擇！")

        if not player.is_alive():
            print(f"\n💀 {player.name} 被 {monster.name} 擊敗，遊戲結束！")
            return
        else:
            print(f"\n🎉 你擊敗咗 {monster.name}！獲得獎勵！")
            player.level_up()
            player.inventory.append("Potion")

    print("\n🎊 恭喜你擊敗所有怪物，成為真正的勇者！")

# 開始遊戲
game()
