import requests

def find_product_id():
    # Gate.io 取得 USDT 結算的所有合約清單 API
    url = "https://api.gateio.ws/api/v4/futures/usdt/contracts"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        contracts = response.json()
        
        print("🔍 正在尋找包含 'GAS' 的商品 ID...\n")
        print("-" * 40)
        for c in contracts:
            # 比對合約名稱中是否包含 GAS
            if 'GAS' in c['name'].upper():
                print(f"✅ 找到商品 ID (name) : {c['name']}")
                print(f"   槓桿倍數 (leverage): {c.get('leverage_min')}x - {c.get('leverage_max')}x")
                print(f"   商品類型 (type)    : {c.get('type')}")
                print("-" * 40)
                
    except Exception as e:
        print(f"API 請求失敗: {e}")

find_product_id()