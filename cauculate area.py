import math

def calculate_circle_area(radius):
  """
  Calculates the area of a circle.

  Args:
    radius: The radius of the circle.

  Returns:
    The area of the circle.
  """
  return math.pi * radius ** 2

def calculate_square_area(side):
  """
  Calculates the area of a square.

  Args:
    side: The length of one side of the square.

  Returns:
    The area of the square.
  """
  return side ** 2

def calculate_rectangle_area(length, width):
  """
  Calculates the area of a rectangle.

  Args:
    length: The length of the rectangle.
    width: The width of the rectangle.

  Returns:
    The area of the rectangle.
  """
  return length * width

def get_positive_float(prompt):
  """
  Gets a positive floating-point number from the user.

  Args:
    prompt: The message to display to the user.

  Returns:
    The entered positive floating-point number.

  Raises:
    ValueError: If the input is not a valid number or is negative.
  """
  while True:
    try:
      value = float(input(prompt))
      if value <= 0:
        raise ValueError("Please enter a positive value.")
      return value
    except ValueError as e:
      print(f"Invalid input: {e}")

def main():
  """
  Gets user input and calculates areas of circle, square, or rectangle.
  """
  while True:
    print("\nChoose a shape:")
    print("1. Circle")
    print("2. Square")
    print("3. Rectangle")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
      radius = get_positive_float("Enter the radius of the circle: ")
      area = calculate_circle_area(radius)
      print(f"Area of the circle: {area:.2f}")
    elif choice == '2':
      side = get_positive_float("Enter the side length of the square: ")
      area = calculate_square_area(side)
      print(f"Area of the square: {area:.2f}")
    elif choice == '3':
      length = get_positive_float("Enter the length of the rectangle: ")
      width = get_positive_float("Enter the width of the rectangle: ")
      area = calculate_rectangle_area(length, width)
      print(f"Area of the rectangle: {area:.2f}")
    elif choice == '4':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
  main()