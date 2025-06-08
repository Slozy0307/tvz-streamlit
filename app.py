import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.title("TVZ 실험용 캔들차트")

ticker = st.text_input("종목 코드 입력", "AAPL")
data = yf.download(ticker, period="1mo", interval="1d")

df = data.copy()

# ✅ 튜플 컬럼 처리
df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

# ✅ 확인 출력
st.write("📌 컬럼 확인:", df.columns)

fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']
)])
st.plotly_chart(fig)

st.write("📊 데이터 수집 결과")
st.write(df.head())
