import os

# Get a list of files in the current directory
def list_files():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    return files

# Create a new file
def create_file():
    filename = input("Enter the file name: ")
    with open(filename, 'w') as file:
        content = input("Enter the content for the file: ")
        file.write(content)
    print(f"File '{filename}' created successfully.")

# View file content
def view_file():
    files = list_files()
    if not files:
        print("No files available to view.")
        return

    print("Select a file to view:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    choice = int(input("Enter the file number: ")) - 1
    if 0 <= choice < len(files):
        filename = files[choice]
        with open(filename, 'r') as file:
            content = file.read()
        print(f"Content of '{filename}':\n{content}")
    else:
        print("Invalid choice.")

# Edit file content
def edit_file():
    files = list_files()
    if not files:
        print("No files available to edit.")
        return

    print("Select a file to edit:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    choice = int(input("Enter the file number: ")) - 1
    if 0 <= choice < len(files):
        filename = files[choice]
        with open(filename, 'a') as file:
            content = input("Enter the content to append: ")
            file.write("\n" + content)
        print(f"Content added to '{filename}'.")
    else:
        print("Invalid choice.")

# Delete a file
def delete_file():
    files = list_files()
    if not files:
        print("No files available to delete.")
        return

    print("Select a file to delete:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    choice = int(input("Enter the file number: ")) - 1
    if 0 <= choice < len(files):
        filename = files[choice]
        os.remove(filename)
        print(f"File '{filename}' deleted successfully.")
    else:
        print("Invalid choice.")

# Main menu
def main():
    while True:
        print("\n--- Simple Notepad ---")
        print("1. Create File")
        print("2. View File")
        print("3. Edit File")
        print("4. Delete File")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            create_file()
        elif choice == '2':
            view_file()
        elif choice == '3':
            edit_file()
        elif choice == '4':
            delete_file()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()