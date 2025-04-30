import math
import cmath
import statistics
import numpy as np
from sympy import symbols, Eq, solve

def super_calculator():
    print("Welcome to the Super Calculator!")
    print("Available operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exponentiation (^ or **) ")
    print("6. Square root (sqrt)")
    print("7. Trigonometric functions (sin, cos, tan)")
    print("8. Logarithms (log, log10)")
    print("9. Factorial (fact)")
    print("10. Mean (mean)")
    print("11. Median (median)")
    print("12. Standard Deviation (stdev)")
    print("13. Complex number operations")
    print("14. Matrix operations")
    print("15. Solve algebraic equations")
    print("0. Exit")

    while True:
        operation = input("Please enter an operation number (or '0' to exit): ").strip()

        if operation == "0":
            print("Exiting the calculator.")
            break

        if operation == "1" or operation.lower() == "addition" or operation == "+":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a + b}")
        
        elif operation == "2" or operation.lower() == "subtraction" or operation == "-":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a - b}")
        
        elif operation == "3" or operation.lower() == "multiplication" or operation == "*":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a * b}")
        
        elif operation == "4" or operation.lower() == "division" or operation == "/":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            if b != 0:
                print(f"Result: {a / b}")
            else:
                print("Error! Division by zero.")
        
        elif operation == "5" or operation.lower() == "exponentiation" or operation == "^" or operation == "**":
            a = float(input("Enter the base number: "))
            b = float(input("Enter the exponent: "))
            print(f"Result: {a ** b}")
        
        elif operation == "6" or operation.lower() == "sqrt" or operation.lower() == "square root":
            a = float(input("Enter the number: "))
            if a >= 0:
                print(f"Result: {math.sqrt(a)}")
            else:
                print("Error! Cannot calculate the square root of a negative number.")
        
        elif operation in ["7", "sin", "cos", "tan"]:
            angle = float(input("Enter the angle in degrees: "))
            angle_rad = math.radians(angle)  # Convert degrees to radians
            if operation == "sin":
                print(f"Result: {math.sin(angle_rad)}")
            elif operation == "cos":
                print(f"Result: {math.cos(angle_rad)}")
            elif operation == "tan":
                print(f"Result: {math.tan(angle_rad)}")
        
        elif operation == "8" or operation.lower() == "log":
            a = float(input("Enter the number: "))
            if a > 0:
                print(f"Result: {math.log(a)}")
            else:
                print("Error! Logarithm undefined for non-positive values.")
        
        elif operation == "9" or operation.lower() == "log10":
            a = float(input("Enter the number: "))
            if a > 0:
                print(f"Result: {math.log10(a)}")
            else:
                print("Error! Logarithm (base 10) undefined for non-positive values.")
        
        elif operation == "10" or operation.lower() == "fact" or operation.lower() == "factorial":
            a = int(input("Enter the number: "))
            if a >= 0:
                print(f"Result: {math.factorial(a)}")
            else:
                print("Error! Factorial is only defined for non-negative integers.")
        
        elif operation == "11" or operation.lower() == "mean":
            numbers = list(map(float, input("Enter a list of numbers (separated by spaces): ").split()))
            print(f"Mean: {statistics.mean(numbers)}")

        elif operation == "12" or operation.lower() == "median":
            numbers = list(map(float, input("Enter a list of numbers (separated by spaces): ").split()))
            print(f"Median: {statistics.median(numbers)}")
        
        elif operation == "13" or operation.lower() == "stdev":
            numbers = list(map(float, input("Enter a list of numbers (separated by spaces): ").split()))
            print(f"Standard Deviation: {statistics.stdev(numbers)}")

        elif operation == "14" or operation.lower() == "complex":
            real = float(input("Enter the real part of the complex number: "))
            imag = float(input("Enter the imaginary part of the complex number: "))
            complex_num = complex(real, imag)
            print(f"Complex number: {complex_num}")
            print(f"Conjugate: {complex_num.conjugate()}")
            print(f"Modulus: {abs(complex_num)}")
        
        elif operation == "15" or operation.lower() == "matrix":
            rows = int(input("Enter the number of rows: "))
            cols = int(input("Enter the number of columns: "))
            matrix = []
            for i in range(rows):
                row = list(map(float, input(f"Enter row {i+1} (space-separated): ").split()))
                matrix.append(row)
            np_matrix = np.array(matrix)
            print(f"Matrix:\n{np_matrix}")
            print(f"Determinant: {np.linalg.det(np_matrix)}")
            print(f"Inverse:\n{np.linalg.inv(np_matrix) if np.linalg.det(np_matrix) != 0 else 'No Inverse (Singular Matrix)'}")
        
        elif operation == "16" or operation.lower() == "solve":
            x = symbols('x')
            equation = input("Enter the equation (e.g., x**2 - 4 = 0): ")
            lhs, rhs = equation.split("=")
            equation = Eq(eval(lhs), eval(rhs))
            solutions = solve(equation, x)
            print(f"Solutions: {solutions}")
        
        else:
            print("Invalid operation. Please try again.")

# Run the super calculator
super_calculator()
