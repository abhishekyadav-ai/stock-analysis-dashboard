import streamlit as st
import yfinance as yf
import altair as alt
import plotly.graph_objects as go

#using caching and fetching stock info through yfinance
@st.cache_data
def fetch_stock_info(symbol):
    #create a stock object for the company
    stock=yf.Ticker(symbol)
    return stock.info

#fetching quarterly financial data
@st.cache_data
def fetch_quarterly_financials(symbol):
    stock=yf.Ticker(symbol)
    return stock.quarterly_financials.T

#fetching annualy financial data
@st.cache_data
def fetch_annual_financials(symbol):
    stock=yf.Ticker(symbol)
    return stock.financials.T

#fetching weekly price history
@st.cache_data
def fetch_weekly_price_history(symbol):
    stock=yf.Ticker(symbol)
    return stock.history(period='1y', interval='1wk')

st.title("Stock Dashboard")
symbol=st.text_input("Enter a stock symbol", "AAPL")

#Fetching the stock information

information=fetch_stock_info(symbol)

st.header("Company information")

st.subheader(f"Name:{information["longName"]}")
st.subheader(f"Maket Cap:${information["marketCap"]:,}")
st.subheader(f"Sector:{information["sector"]}")

price_history=fetch_weekly_price_history(symbol)
st.header("Chart")

#Date is actually the index and not the separate column so we make it a column
price_history=price_history.rename_axis("Date").reset_index()

#preparing candlestick chart for visualization
candle_stick_chart=go.Figure(data=[go.Candlestick(x=price_history["Date"],
                               open=price_history["Open"], high=price_history["High"],
                               low=price_history["Low"], close=price_history["Close"])])

st.plotly_chart(candle_stick_chart, use_container_width=True)


#fetching quarterly and annual financial data for the company
quarterly_financials= fetch_quarterly_financials(symbol)
annual_financials=fetch_annual_financials(symbol)

st.header("Financials")
#Adding a segmeted control
selection=st.segmented_control(label="Period", options=["Quarterly", "Annual"], default="Quarterly")

#If you want to see the quarterly financial report
if selection=="Quarterly":
    quarterly_financials=quarterly_financials.rename_axis("Quarter").reset_index()
    quarterly_financials["Quarter"]=quarterly_financials["Quarter"].astype(str)
    revenue_chart=alt.Chart(quarterly_financials).mark_bar().encode(x="Quarter:O",
    y="Total Revenue")

    net_income_chart=alt.Chart(quarterly_financials).mark_bar().encode(
        x="Quarter:O",
        y="Net Income"
    )
    
    st.altair_chart(revenue_chart, use_container_width=True)
    st.altair_chart(net_income_chart, use_container_width=True)

#If you want to see the annual financial data
if selection=="Annual":
    annual_financials=annual_financials.rename_axis("Year").reset_index()
    annual_financials["Year"]=annual_financials["Year"].astype(str).transform(lambda year:year.split('-')[0])
    revenue_chart=alt.Chart(annual_financials).mark_bar().encode(x="Year:O",
    y="Total Revenue")

    net_income_chart=alt.Chart(annual_financials).mark_bar().encode(
        x="Year:O",
        y="Net Income"
    )
    
    st.altair_chart(revenue_chart, use_container_width=True)
    st.altair_chart(net_income_chart, use_container_width=True)