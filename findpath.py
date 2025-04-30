import os

def find_file(file_name, search_path):
    # 遍歷指定目錄及其子目錄，查找指定檔案
    for dirpath, dirnames, filenames in os.walk(search_path):
        if file_name in filenames:
            # 找到檔案後，輸出完整路徑
            return os.path.join(dirpath, file_name)
    return None  # 如果找不到檔案，返回 None

# 範例用法
search_path = '/storage/emulated/0/'  # 你想搜尋的起始目錄
file_name = 'ufo.mp3'  # 你要找的檔案名稱

file_path = find_file(file_name, search_path)
if file_path:
    print(f"檔案找到啦！路徑是: {file_path}")
else:
    print("檔案未找到。")
