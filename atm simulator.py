class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance is {self.balance}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def check_balance(self):
        print(f"Account balance: {self.balance}")


def atm_interface(account):
    while True:
        print("\nATM Options:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Exit")

        option = input("Choose an option: ")

        if option == '1':
            amount = float(input("Enter amount to deposit: "))
            account.deposit(amount)
        elif option == '2':
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount)
        elif option == '3':
            account.check_balance()
        elif option == '4':
            print("Thank you for using the ATM!")
            break
        else:
            print("Invalid option. Please try again.")

# Example usage
if __name__ == "__main__":
    account = BankAccount("John Doe", 1000)  # Initial balance of 1000
    atm_interface(account)
