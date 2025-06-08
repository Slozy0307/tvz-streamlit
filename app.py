import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.title("TVZ 실험용 캔들차트")

ticker = st.text_input("종목 코드 입력", "AAPL")
data = yf.download(ticker, period="1mo", interval="1d")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(0)

df = data.copy()

# 👇 여기 추가!
df.columns = [col.capitalize() for col in df.columns]

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
st.write("🔎 현재 컬럼:", df.columns)  # 👈 이거 꼭 확인
