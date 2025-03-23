from stock_utility_handler import StockAPI, StockAnalyzer
from ai_insights_handler import AIInsights
import streamlit as st

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "page1"
    st.session_state.ticker = "TATAMOTORS.BSE"
    st.session_state.market = "BSE"
    st.session_state.image_path = ""
    st.session_state.ai_insights = ""
    st.session_state.chat_history = []

def page1():
    st.title('Stock AI Chatbot')

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.ticker = st.text_input("Enter Stock Ticker Symbol", value=st.session_state.ticker, key="ticker_input")
    with col2:
        st.session_state.market = st.selectbox("Select Market", ["BSE", "NASDAQ"], index=["BSE", "NASDAQ"].index(st.session_state.market), key="market_input")

    st.sidebar.header("About")
    st.sidebar.write("This is a stock analysis chatbot platform.")

    st.markdown("---")

    if st.button('Submit'):
        st.session_state.page = "page2"
        st.rerun()

def page2():
    st.title(f"Chat with Stock AI for {st.session_state.ticker}")

    stock_api_obj = StockAPI("1UJ6ACYM0P4MHORZ")
    ai_insights_obj = AIInsights("AIzaSyAVi1v80vt41mTjZED6BaMs5-74HKFkSk0")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Ask about the stock...")

    if user_input:
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process query
        if "price" in user_input.lower():
            market_data = stock_api_obj.get_stock_info(st.session_state.ticker, st.session_state.market)
            try:
                latest_date = list(market_data['Time Series (Daily)'].keys())[0]
                latest_price = market_data['Time Series (Daily)'][latest_date]['4. close']
                bot_reply = f"The latest closing price of {st.session_state.ticker} is ₹{latest_price}."
            except KeyError:
                bot_reply = "I am unable to fetch the stock price right now."
        else:
            response = ai_insights_obj.get_ai_insights(st.session_state.image_path, st.session_state.ticker, st.session_state.market)
            bot_reply = response.candidates[0].content.parts[0].text if response.candidates else "I couldn't generate an insight."

        # Display bot reply
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    if st.button("Back"):
        st.session_state.page = "page1"
        st.rerun()

# Navigation
if st.session_state.page == "page1":
    page1()
elif st.session_state.page == "page2":
    page2()
