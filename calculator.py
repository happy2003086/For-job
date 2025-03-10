def calculator():
    print("Welcome to the Python Calculator!")
    print("You can perform operations like +, -, *, /, ** (exponent), // (floor division), % (modulus)")
    print("Type 'exit' to quit the calculator.")
    
    while True:
        user_input = input("Enter your calculation: ")
        
        if user_input == "exit":
            print("Exiting the calculator. Goodbye!")
            break
        
        try:
            # Evaluate the expression
            result = eval(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}. Please enter a valid expression.")

if __name__ == "__main__":
    calculator()
