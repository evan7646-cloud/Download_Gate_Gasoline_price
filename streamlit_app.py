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

    # 轉換時間格式 (移除 UTC 轉換以保留原始本地時間)
    gate_df['time'] = pd.to_datetime(gate_df['time'], errors='coerce')
    pepper_df['time'] = pd.to_datetime(pepper_df['time'], errors='coerce')
    
    # 統一去除時區資訊以免 Plotly 顯示格式異常
    if gate_df['time'].dt.tz is not None:
        gate_df['time'] = gate_df['time'].dt.tz_localize(None)
        
    # Pepperstone 預設抓下來是券商伺服器時間 (EET, 包含日光節約時間)
    # 我們將它轉換為台北時間 (+8)
    if pepper_df['time'].dt.tz is None:
        pepper_df['time'] = pepper_df['time'].dt.tz_localize('EET').dt.tz_convert('Asia/Taipei').dt.tz_localize(None)
    else:
        pepper_df['time'] = pepper_df['time'].dt.tz_convert('Asia/Taipei').dt.tz_localize(None)

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

    # 根據 timeframe 決定時間顯示格式
    x_format = "%Y-%m-%d" if selected_tf == '1d' else "%Y-%m-%d %H:%M"

    # 介面與游標互動設定
    fig.update_layout(
        title_text=f"Gasoline 走勢比較 ({selected_tf.upper()})",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(x=0.01, y=0.99),
        yaxis_title="報價 (Price)",
        xaxis=dict(
            title="時間",
            tickformat=x_format,
            hoverformat=x_format,
            rangeslider=dict(visible=True, thickness=0.1),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1天", step="day", stepmode="backward"),
                    dict(count=3, label="3天", step="day", stepmode="backward"),
                    dict(count=1, label="1週", step="week", stepmode="backward"),
                    dict(count=1, label="1個月", step="month", stepmode="backward"),
                    dict(step="all", label="全部")
                ]),
                bgcolor="#f0f2f6",
                activecolor="#c0c2c6"
            )
        ),
        height=600 # 加高圖表尺寸讓觀察更舒適
    )

    # 6. 利用 Streamlit 渲染圖表
    st.plotly_chart(fig, use_container_width=True)

    # 7. 計算價差並建立第二張圖表
    # 根據 timeframe 設定時間容許誤差 (tolerance)
    if selected_tf == '15m':
        tol = pd.Timedelta('15m')
    elif selected_tf == '1h':
        tol = pd.Timedelta('1h')
    elif selected_tf == '4h':
        tol = pd.Timedelta('4h')
    else:
        tol = pd.Timedelta('1d')

    # 使用 merge_asof 以最近的時間點對齊，避免 4h / 1d 時區或開盤時間不完全一致而導致合併為空
    merged_df = pd.merge_asof(gate_df, pepper_df, on='time', direction='nearest', tolerance=tol)
    merged_df = merged_df.dropna(subset=['close_pepper', 'close_gate']) # 移除沒有對應到的資料
    merged_df['spread'] = merged_df['close_pepper'] - merged_df['close_gate']

    fig_spread = go.Figure()
    fig_spread.add_trace(
        go.Scatter(x=merged_df['time'], y=merged_df['spread'], name="Spread (Pepper - Gate)", line=dict(color='#2ca02c', width=1.5), fill='tozeroy', fillcolor='rgba(44, 160, 44, 0.2)')
    )
    
    fig_spread.update_layout(
        title_text=f"報價差異 (Pepperstone - Gate) ({selected_tf.upper()})",
        hovermode="x unified",
        template="plotly_white",
        yaxis_title="價差 (Spread)",
        xaxis=dict(
            title="時間",
            tickformat=x_format,
            hoverformat=x_format,
            rangeslider=dict(visible=True, thickness=0.1),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1天", step="day", stepmode="backward"),
                    dict(count=3, label="3天", step="day", stepmode="backward"),
                    dict(count=1, label="1週", step="week", stepmode="backward"),
                    dict(count=1, label="1個月", step="month", stepmode="backward"),
                    dict(step="all", label="全部")
                ]),
                bgcolor="#f0f2f6",
                activecolor="#c0c2c6"
            )
        ),
        height=400
    )
    st.plotly_chart(fig_spread, use_container_width=True)
else:
    st.error(f"找不到對應的 CSV 檔案：\n- {gate_file}\n- {pepper_file}\n請先確認資料是否已下載完成。")
