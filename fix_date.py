import pandas as pd # 匯入 pandas 處理資料
import ast  # 匯入 ast 用來將字串轉回字典
import os # 匯入 os 檢查檔案是否存在

def process_file(interval): # 定義處理單一檔案的函式
    file_name = f"gate_tradfi_gas_{interval}.csv" # 動態建立輸入檔名
    
    if not os.path.exists(file_name): # 檢查檔案是否存在
        print(f"❌ 找不到檔案 {file_name}，跳過處理。\n") # 不存在則顯示錯誤並跳過
        return # 離開函式
        
    df_raw = pd.read_csv(file_name) # 讀取原始資料
    print(f"正在處理 {file_name}，原始欄位：{df_raw.columns.tolist()}") # 顯示目前正在處理的檔案與欄位
    
    # 解析資料：如果資料被包在 'list' 欄位裡
    if 'list' in df_raw.columns: # 如果欄位中有 'list'
        # 將 'list' 欄位裡的字串轉成真正的字典清單
        data_list = [ast.literal_eval(row) for row in df_raw['list']] # 將字串還原為字典陣列
        # 重新建立成乾淨的 DataFrame
        df = pd.DataFrame(data_list) # 轉成新的 DataFrame
    else: # 否則
        df = df_raw # 直接沿用
    
    # 檢查轉換後的欄位 (此時應該有 o, h, l, c, t 了)
    if 't' not in df.columns: # 若沒有時間標記
        print(f"❌ {file_name} 找不到時間標籤，目前欄位有：{df.columns.tolist()}\n") # 顯示錯誤
        return # 離開函式
    
    # 日期轉換：Unix 秒數 -> 台北時間 -> 指定格式
    df['Time'] = pd.to_datetime(df['t'], unit='s') # 將秒數轉換為 datetime
    df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei') # 從 UTC 轉為台北時區
    
    if interval == '1d': # 若為日線
        df['Formatted_Time'] = df['Time'].dt.strftime('%Y/%m/%d') # 只保留日期
    else: # 其他級別
        df['Formatted_Time'] = df['Time'].dt.strftime('%Y/%m/%d %H:%M:%S') # 保留日期與時間
    
    # 格式調整：字串轉數字並更名
    rename_map = {'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'} # 準備欄位重命名字典
    df = df.rename(columns=rename_map) # 將欄位更名
    for col in ['Open', 'High', 'Low', 'Close']: # 走訪這四個欄位
        df[col] = pd.to_numeric(df[col], errors='coerce') # 強制轉為數字格式
    
    # 整理最終表格
    final_df = df[['Formatted_Time', 'Open', 'High', 'Low', 'Close']] # 只保留整理過後的五個欄位
    
    output_file = f"gate_tradfi_gas_{interval}_final.csv" # 動態建立輸出檔名
    final_df.to_csv(output_file, index=False) # 匯出成 CSV 檔案
    print(f"✅ {interval} 檔案已成功處理並儲存至: {output_file}\n") # 顯示處理成功訊息

if __name__ == "__main__": # 如果是直接執行此腳本
    intervals = ['15m', '1h', '4h', '1d'] # 定義要處理的四個時間級別
    for interval in intervals: # 走訪每個級別
        process_file(interval) # 進行資料清洗及格式轉換