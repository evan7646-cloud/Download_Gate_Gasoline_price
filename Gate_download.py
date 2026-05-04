import requests # 匯入 requests 套件發送 API 請求
import pandas as pd # 匯入 pandas 處理資料
import time # 匯入 time 處理時間戳
import urllib3 # 匯入 urllib3 處理憑證警告

# 關閉 Mac 上的 SSL 警告
urllib3.disable_warnings() # 關閉憑證警告

def fetch_tradfi_gas_klines(kline_type="1d", target_bars=5000): # 增加 kline_type 與目標筆數參數
    all_klines = [] # 用來存放所有抓到的 K 線資料
    current_end_time = int(time.time()) # 初始結束時間為現在時間戳
    
    url = f"https://www.gate.com/apiw/v2/tradfi-api/v1/symbols/GAS/klines" # API 網址
    
    # 🚨 完全移植自您瀏覽器的 Request Headers
    headers = { # 定義請求頭
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.gate.com/zh-tw/tradfi/trade/GAS",
        "csrftoken": "63304a56794365546b50794d49593343324d6b626e5979306d4948656e694345474272796c5131415334584a4f4f4e7661554b6d675931725357427052425568",
        "sub_website_id": "0",
        "x-gate-applang": "tw",
        "x-gate-auth-time": str(int(time.time() * 1000)), # 模擬時間戳
        "x-gate-device-type": "0",
        # 下方是您登入狀態的 Cookie
        "Cookie": "lang=tw; auth_sub_website_id=0; signup_invite_source=ref; _fbp=fb.1.1777336446110.85473889441789234; ref_uid=VQCXAF9WVQ; ref_click_time=1777336446; ref_share_id=197230; ref_type=103; _dx_uzZo5y=38fd7adcc30609591ed243c48870cc0ae7f07317ec47e21696d1089ef003de0b81dffe56; seo_lang=%2Fzh-tw; _web3_curMediaSize=xl; _ga=GA1.2.865376032.1777336679; login_notice_check=%2F; finger_print=69f15200fE7MZwqhsf5BGJKSN5k6NrQFLLyWNkO1; _gid=GA1.2.429858182.1777427133; engine_web_id=7633601909558900748; engine_ssid=8395156e-0749-4584-a74b-3b2b4a6d6f2f; _tt_enable_cookie=1; _ttp=01KQBEKG55PVD6QJ1SKQ4E3V8H_.tt.1; uid=52429298; nickname=evan7646%40gmail.com; is_on=1; pver_ws=51b8c2f2cc7b7efb41650214ca74eddd; csrftoken=63304a56794365546b50794d49593343324d6b626e5979306d4948656e694345474272796c5131415334584a4f4f4e7661554b6d675931725357427052425568; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3Nzc0MjgyODUsImlwIjoiWjdBWGR6TDQ3OW1VZ1pJWVZKYkx1UjE4TVk4cWZpQmMzUmgvRUlGNHA4UVp2ZmNBY3VLMStTaz0iLCJpcFJlc3RyaWN0IjoicnFQcjFSaDB2QmxmVDA2aUJMTUw0M1pkZHV2ZE1SbXBIb3l2Z3VFPSIsImRldmljZVR5cGUiOiJMT3hzelFGeGtvUjlOaDVzZUVCMFpyazFYM2p5b2RUeVFqMHVxaE09IiwiZGV2aWNlSWQiOiI5V2FyTzhSUUZ2YXN5K1UvVDRLYndsVzZlSDlUYnJUMy9vK21WUT09IiwidWlkIjoiREV5RXhMT2VTaklia0ppZGZ1U2RRRk11OGVaeHJ6UDN6S0xTQ0pEYmlDRjZXRlFQIiwid2Vic2l0ZUlEIjoiSG5DeUcxWWd6TDdzQ3NNUmhTcVlxQzliOEFqUllOV3NyUkpSVFZVPSJ9._Q6-KcX9Hjfebyi0qzw4n8z3kUmVJNAyO5c20L9y5GU; token_type=Bearer; is_login=1; sub_website_id=0; _ga_JNHPQJS9Q4=GS2.2.s1777431422$o3$g1$t1777431952$j60$l0$h0; useReg=0; lasturl=%2Fmyaccount%2Fprofile%2Fapi-key%2Fmanage; ttcsid=1777427136679::EehF68xnDGlbuh0rqX1e.1.1777431958512.0::0.4815434.4821575::3166489.26.111.88::2441818.13.9; ttcsid_D65BHLJC77UC4VISU8BG=1777427136678::PUgOyCo8PntvO9aMCwy9.1.1777431958512.1; RT=\"z=1&dm=www.gate.com&si=0a03a6c5-8f68-4923-ac21-8307a4e2b75e&ss=moje80hd&sl=d&tt=w9&obo=c&rl=1&nu=1it3l65k&cl=2vr5b\""
    }

    print(f"正在下載 GAS ({kline_type}) K線資料，目標 {target_bars} 筆...") # 顯示下載訊息
    
    while len(all_klines) < target_bars: # 若尚未達到目標筆數則繼續抓
        params = { # 定義 API 參數
            "sub_website_id": "0", # 子網站 ID
            "kline_type": kline_type, # 動態傳入時間級別
            "end_time": current_end_time,  # 結束時間
            "limit": "500" # 每次限制筆數
        }
        
        try: # 嘗試執行請求
            # verify=False 用來忽略 SSL 憑證警告
            response = requests.get(url, params=params, headers=headers, verify=False) # 發送 API 請求
            
            if response.status_code == 200: # 若回傳狀態為 200 (成功)
                data = response.json() # 將回傳資料轉成 JSON 格式
                
                # 取出 klines 陣列
                if isinstance(data, dict) and 'data' in data: # 如果是 dict 且包含 data
                    if isinstance(data['data'], dict) and 'list' in data['data']: # Gate 某些 API 回傳 data 裡面還包一層 list
                        klines_data = data['data']['list']
                    else:
                        klines_data = data['data'] # 取出真正的資料
                else: # 否則
                    klines_data = data # 資料本身就是我們需要的
                    
                if not klines_data: # 如果回傳資料為空
                    break # 結束迴圈
                    
                # 將新抓到的資料加到整體資料的最前面 (因為是越抓越舊)
                all_klines = klines_data + all_klines
                print(f"已獲取 {len(all_klines)} 筆...")
                
                # 取出這批資料最舊的時間戳 (第一筆)，再減去 1 當作下一次的 end_time
                oldest_time = int(klines_data[0]['t'])
                current_end_time = oldest_time - 1
                
                # 如果這批抓到的筆數小於 500，代表伺服器已經沒更舊的資料了
                if len(klines_data) < 500:
                    break
                    
                time.sleep(0.5) # 暫停 0.5 秒避免被 API 封鎖
            else: # 若非 200
                print(f"❌ 下載失敗，狀態碼: {response.status_code}") # 顯示失敗碼
                break # 發生錯誤中斷迴圈
                
        except Exception as e: # 捕捉程式例外
            print(f"❌ 發生錯誤: {e}") # 顯示錯誤訊息
            break # 發生錯誤中斷迴圈
            
    # 若抓到的筆數超過目標筆數，則截斷最前面(最舊)多餘的部分
    if len(all_klines) > target_bars:
        all_klines = all_klines[-target_bars:]
        
    if all_klines: # 若有成功抓到資料
        df = pd.DataFrame(all_klines) # 轉成 DataFrame
        print(f"✅ 下載完成！共 {len(df)} 筆資料。") # 顯示成功
        return df # 回傳 DataFrame
    else:
        return None # 回傳 None

if __name__ == "__main__": # 若為主程式
    intervals = ['15m', '1h', '4h', '1d'] # 定義四種時間級別
    for interval in intervals: # 走訪每個級別
        gas_df = fetch_tradfi_gas_klines(kline_type=interval) # 下載資料
        if gas_df is not None and not gas_df.empty: # 如果有資料
            filename = f"gate_tradfi_gas_{interval}.csv" # 動態定義檔名
            gas_df.to_csv(filename, index=False) # 存成 csv
            print(f"✅ 資料已儲存為 {filename}\n") # 顯示儲存成功