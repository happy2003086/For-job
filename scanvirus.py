import os
import hashlib
from datetime import datetime

# 假設的病毒特徵碼資料庫（實際應用中應該從外部文件或資料庫讀取）
VIRUS_SIGNATURES = {
    "e4d909c290d0fb1ca068ffaddf22cbd0": "Trojan.Generic.123",
    "d41d8cd98f00b204e9800998ecf8427e": "Virus.Test.File",
    "5d41402abc4b2a76b9719d911017c592": "Worm.Exploit.456"
}

def scan_file(file_path):
    """掃描單個文件"""
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        # 計算文件的MD5雜湊值
        file_hash = hashlib.md5(content).hexdigest()
        
        # 檢查是否匹配已知病毒特徵碼
        if file_hash in VIRUS_SIGNATURES:
            return True, VIRUS_SIGNATURES[file_hash]
        else:
            return False, None
    
    except PermissionError:
        print(f"權限不足，無法掃描: {file_path}")
        return False, None
    except Exception as e:
        print(f"掃描文件時出錯 {file_path}: {str(e)}")
        return False, None

def delete_file(file_path):
    """刪除被感染的文件"""
    try:
        os.remove(file_path)
        print(f"已成功刪除感染文件: {file_path}")
        return True
    except Exception as e:
        print(f"刪除文件 {file_path} 失敗: {str(e)}")
        return False

def scan_directory(directory, auto_delete=False):
    """掃描整個目錄"""
    infected_files = []
    total_files = 0
    deleted_files = 0
    
    print(f"開始掃描目錄: {directory}")
    print(f"掃描時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if auto_delete:
        print("警告: 自動刪除模式已啟用!")
    print("-" * 50)
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_files += 1
            is_infected, virus_name = scan_file(file_path)
            
            if is_infected:
                print(f"發現病毒! 文件: {file_path} | 病毒名稱: {virus_name}")
                infected_files.append((file_path, virus_name))
                
                if auto_delete:
                    if delete_file(file_path):
                        deleted_files += 1
    
    print("-" * 50)
    print(f"掃描完成!")
    print(f"總共掃描文件數: {total_files}")
    print(f"發現感染文件數: {len(infected_files)}")
    if auto_delete:
        print(f"已刪除感染文件數: {deleted_files}")
    
    return infected_files

def main():
    print("增強版病毒掃描程式 (含刪除功能)")
    print("=" * 50)
    
    # 讓用戶輸入要掃描的目錄
    target_dir = input("請輸入要掃描的目錄路徑 (留空則掃描當前目錄): ").strip()
    
    if not target_dir:
        target_dir = os.getcwd()
    
    if not os.path.isdir(target_dir):
        print("錯誤: 指定的路徑不是有效的目錄")
        return
    
    # 詢問用戶是否要自動刪除病毒文件
    delete_option = input("是否要自動刪除發現的病毒文件? (y/n): ").strip().lower()
    auto_delete = delete_option == 'y'
    
    infected = scan_directory(target_dir, auto_delete)
    
    # 將結果保存到日誌文件
    log_file = "virus_scan_log.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"病毒掃描報告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"掃描目錄: {target_dir}\n")
        f.write(f"自動刪除模式: {'開啟' if auto_delete else '關閉'}\n")
        f.write(f"總文件數: {len(infected)}\n")
        f.write("感染文件列表:\n")
        for file, virus in infected:
            f.write(f"{file} - {virus}\n")
    
    print(f"掃描結果已保存到 {log_file}")

    # 如果沒有自動刪除但發現了病毒，提供手動刪除選項
    if not auto_delete and infected:
        choice = input("\n檢測到感染文件但未自動刪除，是否要現在處理? (y/n): ").strip().lower()
        if choice == 'y':
            print("\n感染文件列表:")
            for i, (file, virus) in enumerate(infected, 1):
                print(f"{i}. {file} - {virus}")
            
            try:
                selection = input("\n輸入要刪除的文件編號 (多個用逗號分隔，或輸入 'all' 刪除所有): ").strip()
                if selection.lower() == 'all':
                    deleted_count = 0
                    for file, _ in infected:
                        if delete_file(file):
                            deleted_count += 1
                    print(f"已刪除 {deleted_count} 個文件")
                else:
                    indices = list(map(int, selection.split(',')))
                    deleted_count = 0
                    for idx in indices:
                        if 1 <= idx <= len(infected):
                            if delete_file(infected[idx-1][0]):
                                deleted_count += 1
                    print(f"已刪除 {deleted_count} 個文件")
            except ValueError:
                print("輸入無效，請輸入數字或'all'")

if __name__ == "__main__":
    main()