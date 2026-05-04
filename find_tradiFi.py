import requests

def radar_scan_by_price():
    print("啟動雷達：正在掃描全站商品，尋找價格約在 3.4 附近的標的...\n")
    
    # 掃描現貨與期貨的所有端點
    endpoints = [
        "https://api.gateio.ws/api/v4/futures/usdt/tickers",
        "https://api.gateio.ws/api/v4/spot/tickers"
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                for item in data:
                    symbol = item.get('contract', item.get('currency_pair', ''))
                    price_str = item.get('last', '0')
                    
                    try:
                        price = float(price_str)
                        
                        # 條件 1：名字包含常見的天然氣代號
                        is_ng_name = any(keyword in symbol.upper() for keyword in ['NATGAS', 'NG_', 'XNG'])
                        
                        # 條件 2：價格剛好在 3.3 ~ 3.5 之間
                        is_target_price = 3.3 <= price <= 3.5
                        
                        if is_ng_name or is_target_price:
                            print(f"🎯 發現嫌疑目標: {symbol}")
                            print(f"💰 目前報價: {price}")
                            print(f"📍 資料來源: {url}\n")
                            
                    except ValueError:
                        continue
        except Exception as e:
            print(f"連線錯誤 {url}: {e}")

if __name__ == "__main__":
    radar_scan_by_price()