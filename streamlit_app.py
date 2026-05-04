import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. 設定頁面配置 (寬螢幕、標題)
st.set_page_config(page_title="Gasoline Price Comparison", layout="wide")

st.title("Gate Tradfi vs Pepperstone Gasoline")
st.markdown("比較 Gate.io 傳統金融汽油合約與 Pepperstone 的報價差異。")

# 2. 用 Radio 按鈕讓使用者選擇 Timeframe
timeframes = ['15m', '1h', '4h', '1d']
selected_tf = st.radio("請選擇想查看的 Timeframe：", timeframes, horizontal=True)

# 3. 根據選擇動態組裝檔名
gate_file = f'gate_tradfi_gas_{selected_tf}_final.csv'
pepper_file = f'pepperstone_gasoline_{selected_tf}.csv'

# 4. 讀取並處理資料
if os.path.exists(gate_file) and os.path.exists(pepper_file):
    gate_df = pd.read_csv(gate_file)
    pepper_df = pd.read_csv(pepper_file)

    # 欄位重新命名與清理
    gate_df = gate_df.rename(columns={'Formatted_Time': 'time', 'Close': 'close_gate'})
    if 'timestamp' in pepper_df.columns:
        pepper_df = pepper_df.rename(columns={'timestamp': 'time', 'close': 'close_pepper'})

    # 轉換時間格式為 UTC 並排序
    gate_df['time'] = pd.to_datetime(gate_df['time'], errors='coerce', utc=True)
    pepper_df['time'] = pd.to_datetime(pepper_df['time'], errors='coerce', utc=True)

    gate_df = gate_df.dropna(subset=['time']).sort_values('time')
    pepper_df = pepper_df.dropna(subset=['time']).sort_values('time')

    # 5. 建立 Plotly 圖表 (共用同一 Y 軸)
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=gate_df['time'], y=gate_df['close_gate'], name="Gate Tradfi Gas", line=dict(color='#1f77b4', width=1.5))
    )

    fig.add_trace(
        go.Scatter(x=pepper_df['time'], y=pepper_df['close_pepper'], name="Pepperstone Gasoline", line=dict(color='#d62728', width=1.5), opacity=0.8)
    )

    # 介面與游標互動設定
    fig.update_layout(
        title_text=f"Gasoline 走勢比較 ({selected_tf.upper()})",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(x=0.01, y=0.99),
        yaxis_title="報價 (Price)",
        height=600 # 加高圖表尺寸讓觀察更舒適
    )

    # 6. 利用 Streamlit 渲染圖表
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error(f"找不到對應的 CSV 檔案：\n- {gate_file}\n- {pepper_file}\n請先確認資料是否已下載完成。")
