# Restaurant menu data
menu = {
    "Appetizers": ["Spring Rolls", "Salad", "Soup"],
    "Main Courses": ["Chicken Steak", "Beef Steak", "Seafood Fried Rice", "Vegetarian Pasta"],
    "Desserts": ["Chocolate Cake", "Ice Cream", "Fruit Platter"],
    "Drinks": ["Coke", "Orange Juice", "Beer"]
}

# Display menu
def display_menu():
    print("Please choose a category:")
    for category in menu:
        print(f"{category}: {', '.join(menu[category])}")

# Get user's order
def get_order():
    while True:
        category = input("Enter a menu category (Appetizers, Main Courses, Desserts, Drinks): ").strip()
        if category in menu:
            print(f"{category} options are: {', '.join(menu[category])}")
            dish = input(f"Choose a {category} dish: ").strip()
            if dish in menu[category]:
                print(f"You selected {dish}!")
                break
            else:
                print("This dish is not on the menu, please try again.")
        else:
            print("Invalid category, please select a valid one.")

# Main program
def main():
    print("Welcome to the restaurant!")
    display_menu()
    get_order()

# Run the main program
if __name__ == "__main__":
    main()
