import streamlit as st
from stock_utility_handler import fetch_stock_data, generate_chart
from ai_insights_handler import AIInsights
import os

# API Keys for different AI models
GEMINI_API_KEY = "AIzaSyAVi1v80vt41mTjZED6BaMs5-74HKFkSk0"
OPENAI_API_KEY = "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"
CLAUDE_API_KEY = "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"

# Streamlit UI
st.title("AI-Powered Technical Analysis")

# User inputs
stock_symbol = st.text_input("Enter Stock Symbol:", value="AAPL")
model_choice = st.selectbox("Choose AI Model:", ["Gemini", "OpenAI", "Claude"])
analyze_button = st.button("Analyze")

# Initialize AI model with the correct API key
def get_ai_model():
    if model_choice == "Gemini":
        return AIInsights(GEMINI_API_KEY, model_choice)
    elif model_choice == "OpenAI":
        return AIInsights(OPENAI_API_KEY, model_choice)
    elif model_choice == "Claude":
        return AIInsights(CLAUDE_API_KEY, model_choice)

if analyze_button:
    if stock_symbol:
        st.write(f"Fetching data for {stock_symbol}...")
        stock_data = fetch_stock_data(stock_symbol)

        if stock_data is not None:
            chart_path = generate_chart(stock_data, stock_symbol)
            st.image(chart_path, caption="Stock Price Chart")

            ai_insights_obj = get_ai_model()
            analysis = ai_insights_obj.get_analysis(stock_symbol)
            st.write("### AI Analysis")
            st.write(analysis)

            # Provide options for download
            with open(chart_path, "rb") as file:
                st.download_button("Download Chart", file, file_name=f"{stock_symbol}_chart.png")

            analysis_text = f"Stock Analysis for {stock_symbol}\n\n{analysis}"
            st.download_button("Download Analysis", analysis_text, file_name=f"{stock_symbol}_analysis.txt")

            # Back button
            if st.button("Back"):
                st.experimental_rerun()
    else:
        st.error("Please enter a stock symbol.")



'''

                stock_api_obj = StockAPI("1UJ6ACYM0P4MHORZ")
                stock_analyzer_obj = StockAnalyzer()
                ai_insights_obj = AIInsights("AIzaSyAVi1v80vt41mTjZED6BaMs5-74HKFkSk0", model_choice)
'''
