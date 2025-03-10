# -*- coding:utf-8 -*-

# Main Page   /DONE/
# Make a LORE /DONE/
# GH potions in shop /DONE/
# different attacks /DONE/
# mini quests/something to earn coins /TASKS GIVEN/ /3 DONE/ /0 LEFT/
# Monster Class - objects being different monsters /DONE/
# web /NOT doing because don't know how to implement Save file/Load file in web mode/
# uh locations system ig /Not Doing or maybe I shall/ /Acutally Did it/

# to do 
# potions bug (no. not changing after use) /DONE/

# changes compared to prev version: (3/7/22 to 4/7/22)
"""
1.made Weapons_in_Shop carry tuple (cost,attack)
2.made Monster Class, with objects being different species
3.made changes in entire project regarding the points 1 and 2.
4.Location system with new monsters per location added 
  > (character moves to new loc based on count value)
  > (location changes in victory() function)
  > (Location visual added as loc_image() function)
  > (We can now traverse to previously unlocked Locations via the loc_change() function)
5.linked Monsters with different locations
  > 3 monsters per location (for now)
"""

import sys
import os
import pickle
import random
import time

Mini_Games_List = ["Impossible Tic Tac Toe", "Snake Game", "Conquer the Maze"]

Weapons_in_Shop = {"Steel Sword": (50, 15), "Silver Sword": (100, 30), "Blaze Sword": (200, 50), "Z - Sword": (500, 60), "God Killer": (700, 80)}  # Weapons shop category
Potions_in_Shop = {"Potion": 5, "Greater Healing Potion": 20}  # health potions shop category

Locations = {0: "Void Cave", 1: "Forest of Elves", 2: "Heavenly Skies"}  # used to change locations in victory()

count = 0

new_loc_1 = False
new_loc_2 = False


class Player:  # player overlay
    def __init__(self, name):
        self.name = name
        self.MaxHealth = 100
        self.health = self.MaxHealth
        self.MaxMana = 20
        self.mana = self.MaxMana
        self.coins = 30
        self.potions = {"Potion": 3, "Greater Healing Potion": 0}
        self.base_attack = 10
        self.weapons = ["Fists", "Wooden Sword"]
        self.currentWeapon = "Fists"
        self.currLocation = "Void Cave"

    @property
    def attack(self):
        attack = self.base_attack
        if self.currentWeapon == "Fists":
            attack = self.base_attack
        elif self.currentWeapon == "Wooden Sword":
            attack += 5
        elif self.currentWeapon == "Steel Sword":
            attack += Weapons_in_Shop["Steel Sword"][1]
        elif self.currentWeapon == "Silver Sword":
            attack += Weapons_in_Shop["Silver Sword"][1]
        elif self.currentWeapon == "Blaze Sword":
            attack += Weapons_in_Shop["Blaze Sword"][1]
        elif self.currentWeapon == "Z - Sword":
            attack += Weapons_in_Shop["Z - Sword"][1]
        elif self.currentWeapon == "God Killer":
            attack += Weapons_in_Shop["God Killer"][1]

        return attack


class Monster:
    def __init__(self, name, maxh, attack, gcoins, splatk):
        self.name = name
        self.MaxHealth = maxh
        self.health = self.MaxHealth
        self.attack = attack
        self.Gaincoins = gcoins
        self.splAttack = splatk


Rat = Monster("RatMan", 50, 5, 10, "Spear Throw")
Vamp = Monster("Vampire Lazarus", 70, 7, 20, "X - Slash")
BigBat = Monster("Big Bat", 100, 12, 25, "Super Sonic")

Archer_Elf = Monster("Archer Elf", 150, 20, 40, "Lightning Arrow")
War_Elf = Monster("Warrior Elf", 175, 30, 40, "Thunder Bagua")
Elf_Chief = Monster("Elf Chief Horith", 250, 50, 50, "Arcane Magic")

Giant_Eagle = Monster("Giant Eagle", 375, 70, 80, "Hurricane")
Wind_Dragon = Monster("Wind Dragon", 500, 80, 85, "Air Cutter")
Sky_Monarch = Monster("Sky Monarch", 700, 100, 100, "Incinerate!!!")

lis = {"Void Cave": [Rat, Vamp, BigBat], "Forest of Elves": [Archer_Elf, War_Elf, Elf_Chief], "Heavenly Skies": [Giant_Eagle, Wind_Dragon, Sky_Monarch]}
# lis is used to choose which monster is enemy


def main():
    ####MAIN TITLE EDIT

    os.system('cls')

    print("\n\n\n")

    print("\t\t\t███████████████████████████████████████████████████████████████████████▀█")
    print("\t\t\t█─▄▄▄▄█─▄▄─█▄─▄███─▄▄─███▄─▄███▄─▄▄─█▄─█─▄█▄─▄▄─█▄─▄███▄─▄█▄─▀█▄─▄█─▄▄▄▄█")
    print("\t\t\t█▄▄▄▄─█─██─██─██▀█─██─████─██▀██─▄█▀██▄▀▄███─▄█▀██─██▀██─███─█▄▀─██─██▄─█")
    print("\t\t\t▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄▄▄▄▀▀▀▄▀▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀")

    time.sleep(3)

    os.system('cls')
    print("----------------------------")
    print("Welcome to Solo Leveling\n".upper())
    print("1.Start\n2.Load\n3.Exit")
    print("----------------------------")

    option = input(">>>> ")
    if option == "1":
        new_game()
    elif option == "2":
        if os.path.exists("savefile"):
            os.system('cls')
            with open('savefile', 'rb') as file:
                global PlayerA
                PlayerA = pickle.load(file)
            print("Loading Save state...")
            option = input(' ')
            game1()
        else:
            print("You have no savefile.\n")
            option = input(' ')
            main()
    elif option == "3":
        sys.exit()
    else:
        main()


def new_game():  # new game
    os.system('cls')
    print("------------------")
    print("Enter your name: ")
    option = input(">>>> ")
    global PlayerA
    PlayerA = Player(option)
    lore()


def lore():  # intro before game
    os.system('cls')
    lorestr1 = "A Long time ago, this World was very peaceful...\nBut One day, A Portal opened into our world, and Monsters came pouring out of it.\nA Small group of Humans suddenly started Awakening! They came together to Defeat the monsters and save Humanity."
    lorestr2 = "\n\nYou are one of the gifted Heroes who was Awakened with SuperHuman Powers and Strength! Now go kill some Monsters!"
    lorestr = lorestr1 + lorestr2

    for l in lorestr:
        print(l, end='')
        time.sleep(0.05)
    print("...")
    time.sleep(3)
    game1()


def loc_image():  # prints visuals of location
    if PlayerA.currLocation == Locations[0]:
        print("/================\\")
        print("|      /\\        |")
        print("|     /  \\       |")
        print("|  /\/     \     |")
        print("| /   ---   \/\  |")
        print("|/   |   |     \\ |")
        print("\================/")
    if PlayerA.currLocation == Locations[1]:
        print("/===================\\")
        print("|        _-_        |")
        print("|     /~~   ~~\     |")
        print("|  /~~         ~~\  |")
        print("| {  ~   ~~~   ~  } |")
        print("|  \   _-   -_   /  |")
        print("|    ~ \\   // ~     |")
        print("|       |   |       |")
        print("|       |   |       |")
        print("|     //     \\      |")
        print("\===================/")
    if PlayerA.currLocation == Locations[2]:
        print("/=========================\\")
        print("|   ,--.                  |")
        print("|       )                 |")
        print("|      _'-. _             |")
        print("|     (    ) ),--.        |")
        print("|                 )-.__   |")
        print("|______________________)  |")
        print("|                         |")
        print("\=========================/")


def game1():  # main menu for game
    os.system('cls')
    i = 1
    print("----------------------------------------")
    print("Name: %s" % PlayerA.name)
    print("Attack: %i 🗡️" % PlayerA.attack)
    print("coins: %i 🪙" % PlayerA.coins)
    print("Mana: %i 🔥 " % PlayerA.mana)
    print("Health: %i/%i ❤️" % (PlayerA.health, PlayerA.MaxHealth))
    print("Mana: %i/%i 💙" % (PlayerA.mana, PlayerA.MaxMana))

    for key, value in PlayerA.potions.items():
        print("\t" + str(i) + ") " + key + ": 🧪 " + str(value))
        i += 1

    print("Weapons: %s\n" % PlayerA.weapons)
    print("Current Weapon: %s" % PlayerA.currentWeapon)

    print("Location: " + PlayerA.currLocation)
    print("----------------------------------------")

    loc_image()

    print("----------------------------------------")
    print(" ")
    if new_loc_1 or new_loc_2:
        print("1.Fight\n2.Shop\n3.Inventory\n4.Mini-Games\n5.Save\n6.Exit\n7.Move Locations\n")
    else:
        print("1.Fight\n2.Shop\n3.Inventory\n4.Mini-Games\n5.Save\n6.Exit\n")
    print("----------------------------------------")
    option = input(">>>> ")
    if option == "1":
        prepare_to_fight()
    elif option == "2":
        shop()
    elif option == "3":
        inventory()
    elif option == "4":
        minigame()
    elif option == "5":
        os.system('cls')
        with open('savefile', 'wb') as file:
            pickle.dump(PlayerA, file)
            print("Save State Loaded")
            option = input(' ')
            game1()
    elif option == "6":
        sys.exit()
    elif option == "7":
        loc_change()
    else:
        game1()


def loc_change():
    global new_loc_1, new_loc_2
    print("Available locations:")
    available = []
    if new_loc_2:
        available = [0, 1, 2]
        print("0. Void Cave\n1. Forest of Elves\n2. Heavenly Skies")
    elif new_loc_1:
        available = [0, 1]
        print("0. Void Cave\n1. Forest of Elves")
    else:
        print("No new locations unlocked!")
        time.sleep(2)
        game1()
        return

    option = input("Enter location number: ")
    try:
        ch = int(option)
        if ch in available:
            if PlayerA.currLocation == Locations[ch]:
                print(f"You are already in {Locations[ch]}!")
            else:
                PlayerA.currLocation = Locations[ch]
                print(f"Moved to {Locations[ch]}!")
        else:
            print("Invalid location!")
    except ValueError:
        print("Please enter a number.")
    time.sleep(2)
    game1()


def prepare_to_fight():
    global enemy

    no = [0, 1, 2]
    ch = random.choice(no)
    enemy = lis[PlayerA.currLocation][ch]
    fight()


def fight():
    if PlayerA.mana < 0:
        PlayerA.mana = 0

    os.system('cls')

    print("    %s        vs        %s" % (PlayerA.name, enemy.name))
    print("---------------------------------------------------------")
    print("%s's Health: %i/%i  %s's Health: %i/%i" % (PlayerA.name, PlayerA.health, PlayerA.MaxHealth, enemy.name, enemy.health, enemy.MaxHealth))
    print("%s's Mana: %i/%i" % (PlayerA.name, PlayerA.mana, PlayerA.MaxMana))
    print("Potions: %s" % PlayerA.potions)
    print("---------------------------------------------------------")
    print("1.Attack\n2.Drink Potion\n3.Run\n")
    option = input(">>>> ")
    if option == "1":
        pre_attack()
    elif option == "2":
        potion()
    elif option == "3":
        run()
    else:
        fight()


def pre_attack():
    print("-----------------------------------")
    print("1.Basic Attack\n2.Special Attack")
    print("-----------------------------------")
    attack_input = input(">>>> ")
    if attack_input == "1":
        attack()
    elif attack_input == "2":
        special_attack()
    else:
        print("That move doesn't exist!!!")
        time.sleep(2)
        fight()


def special_attack():
    SPA = random.randint(15, 25)  # special player attack damage

    if PlayerA.mana >= 10:
        PlayerA.mana -= 10
        enemy.health -= SPA
        print("You have used Fire Strike!")
        print("You have dealt %i damage" % SPA)
        time.sleep(2)

        if enemy.health <= 0:
            victory()

    else:
        print("You don't have enough mana!")
        time.sleep(1)
        fight()

    SEA = 0
    if PlayerA.currLocation == "Void Cave":
        SEA = random.randint(7, 15)
    elif PlayerA.currLocation == "Forest of Elves":
        SEA = random.randint(10, 20)
    elif PlayerA.currLocation == "Heavenly Skies":
        SEA = random.randint(10, 25)

    if SEA > 13:
        PlayerA.health -= SEA
        print("%s has used %s" % (enemy.name, enemy.splAttack))
        print("%s has dealt %i damage to you" % (enemy.name, SEA))
        time.sleep(2)

        if PlayerA.health <= 0:
            defeat()
        else:
            fight()

    else:
        EDamage = random.randint(int(enemy.attack / 3), enemy.attack)
        if EDamage == int(enemy.attack / 3):
            print("%s's Attack Missed!" % enemy.name)
            time.sleep(2)
        else:
            PlayerA.health -= EDamage
            print("%s has dealt %i damage to you" % (enemy.name, EDamage))
            time.sleep(2)

        if PlayerA.health <= 0:
            defeat()

        else:
            fight()


def attack():
    PDamage = random.randint(int(PlayerA.attack / 3), PlayerA.attack)
    EDamage = random.randint(int(enemy.attack / 3), enemy.attack)

    if PDamage == int(PlayerA.attack / 3):
        print("Your Attack Missed!")
        time.sleep(1)
    else:
        enemy.health -= PDamage
        print("You have dealt %i damage" % PDamage)
        time.sleep(1)

    if enemy.health <= 0:
        victory()

    if EDamage == int(enemy.attack / 3):
        print("%s's Attack Missed!" % enemy.name)
        time.sleep(2)
    else:
        PlayerA.health -= EDamage
        print("%s has dealt %i damage to you" % (enemy.name, EDamage))
        time.sleep(2)

    if PlayerA.health <= 0:
        defeat()

    else:
        fight()


def potion():
    potion1()
    fight()


def potion1():
    potions = list(PlayerA.potions.items())
    print("------------------------------------")
    print("Which potion do you want to use?")
    for i, (potion, qty) in enumerate(potions, 1):
        print(f"{i}) {potion}: {qty}")
    print("------------------------------------")
    option = input("Enter the number: ")
    try:
        choice = int(option) - 1
        if 0 <= choice < len(potions):
            potion_name, quantity = potions[choice]
            if quantity > 0:
                if potion_name == "Potion":
                    PlayerA.health += 30
                    if PlayerA.health > PlayerA.MaxHealth:
                        PlayerA.health = PlayerA.MaxHealth
                elif potion_name == "Greater Healing Potion":
                    PlayerA.health += 80
                    if PlayerA.health > PlayerA.MaxHealth:
                        PlayerA.health = PlayerA.MaxHealth
                PlayerA.potions[potion_name] -= 1
                print(f"You used a {potion_name}!")
            else:
                print(f"You don't have any {potion_name} left!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
    time.sleep(2)


def run():
    if PlayerA.coins > 5:
        PlayerA.coins -= 5
        print("You ran away \n")
        time.sleep(2)
        game1()
    else:
        print("You Don't have enough 🪙 to run away!")
        time.sleep(2)
        fight()


def victory():
    PlayerA.coins += enemy.Gaincoins
    enemy.health = enemy.MaxHealth
    print("You have defeated the enemy %s" % enemy.name)
    time.sleep(2)
    print("You have obtained %i 🪙  gold coins!" % enemy.Gaincoins)
    print("=================================")
    time.sleep(2)
    global count, new_loc_1, new_loc_2
    count += 1
    if count == 5:
        PlayerA.currLocation = Locations[1]
        PlayerA.MaxHealth += 150
        PlayerA.MaxMana += 20
        PlayerA.health = PlayerA.MaxHealth
        print("Congratulations! You have moved to a new Location [Forest of Elves]!")
        new_loc_1 = True
        time.sleep(3)
    if count == 15:
        PlayerA.currLocation = Locations[2]
        PlayerA.MaxHealth += 400
        PlayerA.MaxMana += 50
        PlayerA.health = PlayerA.MaxHealth
        print("Congratulations! You have moved to a new Location [Heavenly Skies]!")
        new_loc_2 = True
        time.sleep(3)
    PlayerA.mana = PlayerA.MaxMana
    game1()


def defeat():
    PlayerA.coins -= 10
    print("YOU HAVE BEEN DEFEATED")
    time.sleep(2)
    PlayerA.health = PlayerA.MaxHealth
    PlayerA.mana = PlayerA.MaxMana
    game1()


def inventory():
    os.system('cls')
    i = 1
    print("-----------------------------")
    print("Weapons: ")
    for weap in PlayerA.weapons:
        print(str(i) + ') ' + weap)
        i += 1
    print("-----------------------------")
    i = 1
    print("Potions: ")
    for key, value in PlayerA.potions.items():
        print(str(i) + ") " + key + ": " + str(value))
        i += 1
    print("-----------------------------")

    time.sleep(2)
    print('What do you want to do?\n')
    print("1.Choose Weapon\n2.Close Inventory\n")
    print("-----------------------------")
    option = input(">>>> ")
    if option == "1":
        equip()
    elif option == "2":
        game1()


def equip():
    os.system('cls')
    print("-----------------------------")
    print("Choose Weapon to equip: ")
    for idx, weap in enumerate(PlayerA.weapons, 1):
        print(f"{idx}) {weap}")
    print("Type 'Back' to go back")
    print("-----------------------------")
    option = input(">>>> ")
    if option.lower() == 'back':
        inventory()
    else:
        try:
            choice = int(option)
            if 1 <= choice <= len(PlayerA.weapons):
                selected_weapon = PlayerA.weapons[choice - 1]
                PlayerA.currentWeapon = selected_weapon
                print(f"Equipped {selected_weapon}!")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")
        time.sleep(2)
        inventory()


def shop():
    os.system('cls')
    print("-----------------------------")
    print("Welcome to the Shop!")
    print("1.Weapons\n2.Potions\n3.Exit")
    print("-----------------------------")
    option = input(">>>> ")
    if option == "1":
        print("-----------------------------")
        print("Weapons Available:")
        for weapon, (cost, attack) in Weapons_in_Shop.items():
            print(f"{weapon}: {cost} coins (Attack: +{attack})")
        print("-----------------------------")
        print("Enter the name of the weapon you want to buy (or 'Back' to return):")
        choice = input(">>>> ")
        if choice.lower() == 'back':
            shop()
        elif choice in Weapons_in_Shop:
            if choice in PlayerA.weapons:
                print("You already own this weapon!")
            else:
                cost = Weapons_in_Shop[choice][0]
                if PlayerA.coins >= cost:
                    PlayerA.coins -= cost
                    PlayerA.weapons.append(choice)
                    print(f"You bought the {choice}!")
                else:
                    print("You don't have enough coins!")
            time.sleep(2)
            shop()
        else:
            print("Invalid weapon!")
            time.sleep(2)
            shop()
    elif option == "2":
        print("-----------------------------")
        print("Potions Available:")
        for potion, cost in Potions_in_Shop.items():
            print(f"{potion}: {cost} coins")
        print("-----------------------------")
        print("Enter the name of the potion you want to buy (or 'Back' to return):")
        choice = input(">>>> ")
        if choice.lower() == 'back':
            shop()
        elif choice in Potions_in_Shop:
            cost = Potions_in_Shop[choice]
            if PlayerA.coins >= cost:
                PlayerA.coins -= cost
                PlayerA.potions[choice] += 1
                print(f"You bought a {choice}!")
            else:
                print("You don't have enough coins!")
            time.sleep(2)
            shop()
        else:
            print("Invalid potion!")
            time.sleep(2)
            shop()
    elif option == "3":
        game1()
    else:
        shop()


def minigame():
    os.system('cls')
    print("-----------------------------")
    print("Mini-Games Available:")
    for idx, game in enumerate(Mini_Games_List, 1):
        print(f"{idx}) {game}")
    print("-----------------------------")
    print("Enter the number of the mini-game you want to play (or 'Back' to return):")
    option = input(">>>> ")
    if option.lower() == 'back':
        game1()
    else:
        try:
            choice = int(option) - 1
            if 0 <= choice < len(Mini_Games_List):
                print(f"Playing {Mini_Games_List[choice]}...")
                time.sleep(2)
                print("Mini-game completed! Here are your rewards!")
                PlayerA.coins += 50
                print("You earned 50 coins!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number.")
        time.sleep(2)
        game1()


if __name__ == "__main__":
    main()