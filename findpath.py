import os

def find_file(filename, search_path="/storage/emulated/0/"):
    """
    在指定的目錄（及其子目錄）中搜尋檔案，並回傳完整路徑
    """
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

# 讓使用者輸入檔案名稱
file_name = input("請輸入檔案名稱（包含副檔名，例如 example.mp3）：")

# 搜尋檔案
file_path = find_file(file_name)

# 顯示結果
if file_path:
    print(f"檔案找到！完整路徑：{file_path}")
else:
    print("找不到該檔案，請確認名稱是否正確。")
