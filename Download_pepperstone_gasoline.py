import os
import time
os.environ['TZ'] = 'UTC'
if hasattr(time, 'tzset'):
    time.tzset()

from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def main():
    print("初始化 TradingView 客戶端 (匿名登入)...")
    tv = TvDatafeed()
    
    symbol = 'GASOLINE'
    exchange = 'PEPPERSTONE'
    
    intervals = {
        '15m': Interval.in_15_minute,
        '1h': Interval.in_1_hour,
        '4h': Interval.in_4_hour,
        '1d': Interval.in_daily
    }
    
    for name, interval in intervals.items():
        print(f"正在下載 {exchange}:{symbol} 的 {name} K線資料...")
        df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=5000)
        
        if df is not None and not df.empty:
            df = df.reset_index()
            # 確保取得的時間為 UTC，並轉換為台北時間
            df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei')
            
            df = df.rename(columns={'datetime': 'timestamp'})
            df = df[['timestamp', 'open', 'high', 'low', 'close']]
            
            if name == '1d':
                df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            else:
                df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
            filename = f"pepperstone_gasoline_{name}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ 成功！資料已儲存為 {filename}\n")
        else:
            print(f"❌ 失敗！無法獲取 {name} 資料\n")

if __name__ == "__main__":
    main()
