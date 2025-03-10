from mpmath import mp

mp.dps = 10000  # 設定小數點後 10000 位
pi_value = str(mp.pi)  # 計算 π 並轉換為字串

# 記錄計算時間
import time
start_time = time.time()
pi_value = str(mp.pi)  # 計算 π
end_time = time.time()

print("計算時間:", end_time - start_time, "秒")
print("π 小數點後 10000 位數:", pi_value[:10002])  # 顯示完整 π 值
