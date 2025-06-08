import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.title("TVZ 실험용 캔들차트")

ticker = st.text_input("종목 코드 입력", "AAPL")
data = yf.download(ticker, period="1mo", interval="1d")

# 인덱스 초기화 & 컬럼 이름 정리 (AAPL 제거)
data.reset_index(inplace=True)

# MultiIndex → 단일 컬럼 이름만 유지
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(0)

df = data.copy()

# 캔들차트 그리기
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']
)])
st.plotly_chart(fig)

st.write("📊 데이터 수집 결과")
st.write(df.head())
