import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.title("TVZ 실험용 캔들차트")

ticker = st.text_input("종목 코드 입력", "AAPL")
data = yf.download(ticker, period="1mo", interval="1d")

fig = go.Figure(data=[go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
)])
st.plotly_chart(fig)

st.write("데이터 수집 결과")
st.write(data.head())
