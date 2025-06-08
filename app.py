import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 🔹 앱 제목
st.title("📊 TVZ 실험용 캔들차트")

# 🔹 사이드바 메뉴 구성
st.sidebar.header("🛠 설정")
ticker = st.sidebar.text_input("종목 코드", "AAPL")
data_source = st.sidebar.selectbox("데이터 소스", ["Yahoo Finance"])  # 이후 Polygon 추가 예정
interval = st.sidebar.selectbox("데이터 주기", ["1d", "1wk", "1mo"])
tvz_period = st.sidebar.slider("TVZ 기간 (일)", min_value=5, max_value=100, value=20)

# 🔹 데이터 수집
@st.cache_data(show_spinner=False)
def load_yahoo_data(ticker, interval):
    try:
        data = yf.download(ticker, period="1mo", interval=interval)
        data.reset_index(inplace=True)
        return data
    except:
        return pd.DataFrame()

if data_source == "Yahoo Finance":
    df = load_yahoo_data(ticker, interval)

# 🔹 컬럼 정리
if not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)

    # 🔹 캔들차트 그리기
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'] if 'Date' in df.columns else df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candles"
    )])

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🔹 데이터 테이블 출력
    st.markdown("### 📋 데이터 미리보기")
    st.dataframe(df.tail(10), use_container_width=True)
else:
    st.warning("❗ 데이터를 불러올 수 없습니다. 종목 코드 또는 API 상태를 확인하세요.")
