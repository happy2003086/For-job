import os

# 創建新文件
def create_file():
    filename = input("Enter the file name: ")
    with open(filename, 'w') as file:
        content = input("Enter the content for the file: ")
        file.write(content)
    print(f"File '{filename}' created successfully.")

# 查看文件內容
def view_file():
    filename = input("Enter the file name to view: ")
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            content = file.read()
        print(f"Content of '{filename}':\n{content}")
    else:
        print(f"File '{filename}' does not exist.")

# 編輯文件內容
def edit_file():
    filename = input("Enter the file name to edit: ")
    if os.path.exists(filename):
        with open(filename, 'a') as file:
            content = input("Enter the content to append: ")
            file.write("\n" + content)
        print(f"Content added to '{filename}'.")
    else:
        print(f"File '{filename}' does not exist.")

# 刪除文件
def delete_file():
    filename = input("Enter the file name to delete: ")
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' deleted successfully.")
    else:
        print(f"File '{filename}' does not exist.")

# 主菜單
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
