import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# 🔹 사이드바 메뉴 구성
st.sidebar.header("🛠 설정")
ticker = st.sidebar.text_input("종목 코드", "AAPL")
data_source = st.sidebar.selectbox("데이터 소스", ["Yahoo Finance"])  # 이후 Polygon 추가 예정
interval = st.sidebar.selectbox("데이터 주기", ["1d", "1wk", "1mo"])
tvz_period = st.sidebar.slider("TVZ 기간 (일)", min_value=5, max_value=100, value=20)

data_source = st.sidebar.selectbox("데이터 소스", ["Yahoo Finance"])


# Yahoo Finance 선택 시
if source == "Yahoo Finance":
    data = yf.download(ticker, interval=interval, start="1980-01-01")  # 가장 과거부터 불러오기

    if data.empty:
        st.warning("📭 데이터가 없습니다. 종목 코드, 주기 등을 확인해주세요.")
        st.stop()  # 더 이상 아래 코드 실행 안 함

    # 이후 데이터 처리...
    df = data.copy()
    df.index = pd.to_datetime(df.index)

# 🔹 데이터 수집
@st.cache_data(show_spinner=False)
def load_yahoo_data(ticker, interval):
    try:
        data = yf.download(ticker, period="max", interval=interval)
        data.reset_index(inplace=True)
        return data
    except:
        return pd.DataFrame()

if data_source == "Yahoo Finance":
    df = load_yahoo_data(ticker, interval)

# 🔹 컬럼 정리
if not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        # 다중 인덱스일 경우: 첫 번째 계층명을 유지하고 두 번째 계층명을 제거
        df.columns = df.columns.get_level_values(0)

    if 'Open' in df.columns:
        fig = go.Figure(data=[go.Candlestick(
            x=df['Date'] if 'Date' in df.columns else df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )]) 
    else:
        st.error("🛑 'Open' 컬럼이 없습니다. 데이터 소스를 확인해주세요.")

    # 🔹 캔들차트 그리기
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'] if 'Date' in df.columns else df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candles"
    )])
     # 마우스 휠 기준 범위 설정
    if len(df.index) >= 2:
        x_range = [df.index[max(0, len(df.index) - 200)], df.index[-1]]
    else:
        x_range = None  # 또는 차트를 표시하지 않음

    fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=False),
        range=x_range,
        fixedrange=False,
        autorange=False,
    ),
    margin=dict(l=0, r=0, t=30, b=10),
    height=760,
    plot_bgcolor='white',
    dragmode='pan'
)


    st.plotly_chart(fig, use_container_width=True)
    st.write("인덱스 타입:", type(df.index))

else:
    st.error("🛑 'Open' 컬럼이 없습니다. 데이터 소스를 확인해주세요.")