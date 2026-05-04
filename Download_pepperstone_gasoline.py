from tvDatafeed import TvDatafeed, Interval # 匯入 TvDatafeed 套件及時間級別常數
import pandas as pd # 匯入 pandas 套件處理資料
import warnings # 匯入 warnings 套件處理警告

warnings.filterwarnings("ignore") # 忽略執行過程中的警告訊息

def main(): # 定義主函式
    print("初始化 TradingView 客戶端 (匿名登入)...") # 顯示初始化訊息
    tv = TvDatafeed() # 建立 TvDatafeed 實體 (匿名登入)
    
    symbol = 'GASOLINE' # 設定要抓取的商品代碼為 GASOLINE
    exchange = 'PEPPERSTONE' # 設定要抓取的交易所為 PEPPERSTONE
    
    intervals = { # 定義一個字典，存放不同時間級別與其對應的 TvDatafeed 常數
        '15m': Interval.in_15_minute, # 15分鐘 K 線
        '1h': Interval.in_1_hour, # 1小時 K 線
        '4h': Interval.in_4_hour, # 4小時 K 線
        '1d': Interval.in_daily # 日 K 線
    } # 字典定義結束
    
    for name, interval in intervals.items(): # 走訪每個時間級別
        print(f"正在下載 {exchange}:{symbol} 的 {name} K線資料...") # 顯示目前正在下載的級別
        df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=5000) # 呼叫 get_hist 下載歷史資料，最多約 5000 根
        
        if df is not None and not df.empty: # 檢查是否成功下載到資料且資料不為空
            df = df.reset_index() # 將原本為 datetime 的 index 轉換為一般欄位
            df = df.rename(columns={'datetime': 'timestamp'}) # 將 datetime 欄位重新命名為 timestamp
            
            df = df[['timestamp', 'open', 'high', 'low', 'close']] # 只保留我們需要的開高低收及時間欄位
            
            if name == '1d': # 若為日線資料
                df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d') # 只保留日期，去除時間部分
                
            filename = f"pepperstone_gasoline_{name}.csv" # 動態產生要存檔的 CSV 檔名
            df.to_csv(filename, index=False) # 將資料存成 CSV 檔案，不保留 index
            print(f"✅ 成功！資料已儲存為 {filename}\n") # 顯示成功儲存的訊息
        else: # 如果沒有下載到資料
            print(f"❌ 失敗！無法獲取 {name} 資料\n") # 顯示失敗訊息

if __name__ == "__main__": # 判斷是否為直接執行此腳本
    main() # 執行主函式
