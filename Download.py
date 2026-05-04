import requests
import pandas as pd
import warnings

# 隱藏惱人的 Mac SSL 警告
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

def get_gate_candlesticks(symbol, interval='1d', limit=10):
    url = "https://api.gateio.ws/api/v4/futures/usdt/candlesticks"
    
    params = {
        'contract': symbol,
        'interval': interval,
        'limit': limit
    }
    
    print(f"正在抓取 {symbol} 的 {interval} K線資料...\n")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 檢查是否有抓到資料
        if not data:
            print("API 請求成功，但回傳為空陣列。請確認 symbol 代碼是否正確！")
            return None
            
        print("✅ 成功獲取資料！原始資料長相 (第一筆)：")
        print(data[0], "\n")
        
        # 將資料轉為 DataFrame
        df = pd.DataFrame(data)
        
        # Gate 的 key 通常是縮寫：t(時間), v(量), c(收盤), h(最高), l(最低), o(開盤)
        # 我們將其重新命名為標準名稱
        rename_map = {'t': 'timestamp', 'v': 'volume', 'c': 'close', 'h': 'high', 'l': 'low', 'o': 'open'}
        df = df.rename(columns=rename_map)
        
        # 轉換時間與數值格式
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col])
                
        # 依時間先後排序
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df
    else:
        print(f"抓取失敗，錯誤碼: {response.status_code}")
        print(response.text)
        return None

# 執行測試
# 注意：GAS_USDT 是加密貨幣的 NEO Gas 代幣。如果您要抓傳統金融的汽油，
# 必須用 F12 找出真正的代碼 (例如 US_RBOB_Gasoline_Jun) 與正確的 URL 端點。
df_result = get_gate_candlesticks(symbol='GAS', interval='1d', limit=10)

if df_result is not None:
    print(df_result[['timestamp', 'open', 'high', 'low', 'close']])