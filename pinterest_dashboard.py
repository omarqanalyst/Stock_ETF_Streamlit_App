#!/usr/bin/env python
# dashboard.py
import streamlit as st
import pandas as pd
from dynamic_paragraph_momentum import generate_trade_advice
from dynamic_paragraph_forecasting import generate_forecasting_advice

from data_utils import load_data, calculate_mutual_dates, calculate_correlation_matrix, calculate_52_week_high_low, calculate_relative_strength, calculate_moving_averages
from forecasting import create_volatility_forecast
from figures import create_normalized_price_figure, create_correlation_matrix_figure, create_price_chart
from get_theme import get_theme_colors


# Define the data file path here for easy reference
DATA_PATH = 'ETF_SOCL_Holdings.csv'
theme_colors = get_theme_colors()
secondary_bg = theme_colors["secondary_bg"]



def main():
    # Load and preprocess data using the specified file path
    df = load_data(DATA_PATH)
    earliest_mutual_date, latest_mutual_date = calculate_mutual_dates(df)
    
    # Sidebar controls for user input
    st.sidebar.header("Stock Market Analytics Dashboard")
    st.sidebar.markdown("This dashboard analyzes Pinterest's stock performance against publicly traded peers, using the SOCL ETF and its holdings as benchmarks.")

    st.sidebar.header("Controls")
    
    tickers = df['ticker'].unique()

    # Convert tickers to a list for easier index lookup
    tickers_list = list(tickers)
    # Determine the default index for "PINS" and "RDDT"
    default_index = tickers_list.index("PINS") if "PINS" in tickers_list else 0
    competitor_index = tickers_list.index("RDDT") if "RDDT" in tickers_list else (1 if len(tickers_list) > 1 else 0)

    selected_ticker = st.sidebar.selectbox('Select Your Stock', tickers, index=default_index)
    competitor_ticker = st.sidebar.selectbox('Select Competitor Stock', tickers, index=competitor_index)    


    st.sidebar.header("Data Architecture & Foundations")
    st.sidebar.markdown(f"""
    :blue[**Infrastructure & Storage**]  
    ✓ **AWS SAM** for streamlined serverless app deployment  
    ✓ Collected & stored data in **S3** using AWS cloud services  

    :blue[**Data Processing & ETL**]  
    ✓ Processed **11,000 tickers** with **PySpark**  
    ✓ Atomated **ETL workflows** using **AWS Glue**

    :blue[**Analysis & Insights**]   
    ✓ **AWS Athena** for fast, serverless data querying and analysis  
    ✓ Analyzed **{len(df['ticker'].unique())} SOCL holdings**  
    """)






    
    st.title(":primary[Pinterest] Stock Market Analytics: SOCL ETF Insights", help="Analysis moves from macro to micro, starting with peer comparisons and then focusing on Pinterest")
 
    st.markdown(
        """
        <style>
        /* Target the tooltip container rendered by Base Web */
        .stTooltipContent{
            background-color: #CDECE4 !important;  /* desired background color */
            color: #1C6B6C !important;              /* adjust text color if needed */
            border: 1px solid #ccc;               /* optional border */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
        
    # Comparative Analysis Section: Normalized Price Comparison
    st.header("Comparative Analysis",  help="A side-by-side comparison of PINS, SOCL ETF, and a competitor stock")
    st.subheader("Normalized Price Comparison", help="Normalization removes scale differences, enabling a clear comparison of growth trajectories")
    
    selected_data = df[df['ticker'] == selected_ticker].copy()
    competitor_data = df[df['ticker'] == competitor_ticker].copy()
    benchmark_data = df[df['ticker'] == 'SOCL'].copy()

    # Normalize the closing prices for comparison
    selected_data['normalized_close'] = selected_data['close'] / selected_data['close'].iloc[0]
    competitor_data['normalized_close'] = competitor_data['close'] / competitor_data['close'].iloc[0]
    benchmark_data['normalized_close'] = benchmark_data['close'] / benchmark_data['close'].iloc[0]

    
    norm_fig = create_normalized_price_figure(
        selected_data, competitor_data, benchmark_data,
        selected_ticker, competitor_ticker, "SOCL",
        theme_colors
    )
    st.plotly_chart(norm_fig, use_container_width=True)
        
    # Correlation Analysis Section
    st.header("Correlation Analysis", help="Identifies how closely Pinterest moves with peers in SOCL ETF")
    corr_matrix = calculate_correlation_matrix(df, earliest_mutual_date, latest_mutual_date)
    corr_fig = create_correlation_matrix_figure(corr_matrix)
    st.plotly_chart(corr_fig, use_container_width=True)
    
    # Volatility Forecasting Section
    st.header("Volatility Forecasting", help="Provides early warnings of price swings using the Prophet model")
    if not selected_data.empty:
        forecast_fig, forecast_df = create_volatility_forecast(selected_data)
        st.plotly_chart(forecast_fig, use_container_width=True)

        forecast_action, forecast_advice, last_date = generate_forecasting_advice(forecast_df, selected_data)
        st.markdown(f":blue[**Recommended Action**]: {forecast_action}", help="Dynamic Analysis for Volatility Forecast. Dates and values are dynamic")
        st.markdown(forecast_advice)

    
    # Ticker Overview Section: Price Chart and Key Metrics
    st.header("Ticker Overview: Pinterest", help="Provides stakeholders with a snapshot of performance and risk metrics")
    ticker_data = df[df['ticker'] == selected_ticker]

    # 🚀 Compute Financial Metrics
    latest_volatility = ticker_data['30d_volatility'].iloc[-1]
    sharpe_ratio = ticker_data['sharpe_ratio'].iloc[-1]
    high_52w, low_52w = calculate_52_week_high_low(df, selected_ticker)
    moving_averages = calculate_moving_averages(df, selected_ticker, windows=[50, 100, 200])
    relative_strength = calculate_relative_strength(df, selected_ticker)

    def round_diff(close_price, reference):
        return round(close_price - reference, 2)

    # Extract Latest Row (Most Recent Date)
    latest_row = ticker_data.iloc[-1]
    latest_close = latest_row['close']

    # Display the Price Chart at the Top
    st.subheader("Historical Price Trend", help="An interactive line chart showing historical closing prices, incorporating key momentum benchmarks")
    price_chart_fig = create_price_chart(ticker_data, selected_ticker, high_52w, low_52w)
    st.plotly_chart(price_chart_fig, use_container_width=True)

    # --- Add dynamic trade advice paragraph below the price chart ---
    recent_high_3d = ticker_data['high'].tail(3).max()
    cp_below_50_consecutive = False  # Replace with actual logic if available.
    action, advice_message = generate_trade_advice(
        CP=latest_close,
        ma50=moving_averages.get(50, latest_close),
        ma200=moving_averages.get(200, latest_close),
        wk52_high=high_52w,
        wk52_low=low_52w,
        recent_high_3d=recent_high_3d,
        cp_below_50_consecutive=cp_below_50_consecutive
    )

    # Add the blue bold text
    st.markdown(f":blue[**Recommended Action**]: {action}", help="Dynamic Analysis: Implementing Kragger's principles in Python")
    st.markdown(advice_message)

    # Load Theme Colors
    secondary_bg = theme_colors["secondary_bg"]

    def get_delta_value(value, reference):
        return value - reference

    def get_delta_color(value, reference):
        if value > reference:
            return "normal"
        elif value < reference:
            return "inverse"
        else:
            return "off"

    # 🚀 **New Row: Latest Stock Data**
    st.subheader("Latest Stock Data", help="Latest stock data provides a snapshot of PINS’ daily performance, empowering stakeholders to make data-driven decisions using real-time price and volume trends")

    # Extract the latest available row for the selected ticker
    latest_date = latest_row['date'].strftime('%Y-%m-%d')
    latest_ticker = latest_row['ticker']

    # Display Ticker & Date at the Top (as Markdown)
    st.markdown(f"**Ticker:** {latest_ticker} | **Date:** {latest_date}")

    # Create a practical column layout
    col1, col2, col3 = st.columns([1, 1, 1])

    # Price Metrics (Close, Open, High, Low)
    with col1:
        st.metric("Close", f"${latest_close:.2f}")

        st.metric("Open", f"${latest_row['open']:.2f}")

    with col2:
        st.metric("High", f"${latest_row['high']:.2f}")

        st.metric("Low", f"${latest_row['low']:.2f}")

    with col3:
        st.metric("Volume", f"{latest_row['volume']:,.0f}")

    
    def style_header_box(text):
        """
        Returns styled HTML with your secondary background color for section headers.
        """
        return f"""
        <div style="
            background-color: {secondary_bg};
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
        ">
            {text}
        </div>
        """


    # 📊 **Key Metrics Section**
    st.subheader("Key Metrics", help="Enables rapid assessment of whether a ticker aligns with investment or advertising goals")
    colA, colB, colC = st.columns(3)

    with colA:
        # Instead of st.markdown("**52-Week High / Low**"), do:
        st.markdown(style_header_box("52-Week High / Low"), unsafe_allow_html=True)
        diff_high = round_diff(latest_close, high_52w)
        st.metric("52-Week High", f"${high_52w:.2f}", diff_high, delta_color="normal")

        diff_low = round_diff(latest_close, low_52w)
        st.metric("52-Week Low", f"${low_52w:.2f}", diff_low, delta_color="normal")

    with colB:
        st.markdown(style_header_box("Volatility & Risk"), unsafe_allow_html=True)
        st.metric("30-Day Volatility", f"{latest_volatility:.2f}")
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

    with colC:
        st.markdown(style_header_box("Moving Averages"), unsafe_allow_html=True)
        diff_50 = round_diff(latest_close, moving_averages.get(50, 0))
        st.metric("50-Day MA", f"${moving_averages.get(50, 'N/A'):.2f}", diff_50, delta_color="normal")

        diff_100 = round_diff(latest_close, moving_averages.get(100, 0))
        st.metric("100-Day MA", f"${moving_averages.get(100, 'N/A'):.2f}", diff_100, delta_color="normal")

        diff_200 = round_diff(latest_close, moving_averages.get(200, 0))
        st.metric("200-Day MA", f"${moving_averages.get(200, 'N/A'):.2f}", diff_200, delta_color="normal")

        if relative_strength:
            st.markdown(style_header_box("Relative Strength"), unsafe_allow_html=True)
            st.metric("Relative Strength", f"{relative_strength:.2f}")


if __name__ == "__main__":
    main()
