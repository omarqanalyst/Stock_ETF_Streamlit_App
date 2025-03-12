# figures.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


import plotly.graph_objects as go

def create_normalized_price_figure(selected_data, competitor_data, benchmark_data,
                                   selected_ticker, competitor_ticker, benchmark_ticker,
                                   theme_colors):
    """
    Create a normalized price comparison figure with a benchmark ticker.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=selected_data['date'], y=selected_data['normalized_close'],
        name=selected_ticker, line=dict(color=theme_colors["primary"]),
        hovertemplate='Normalized Price: %{y:.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=competitor_data['date'], y=competitor_data['normalized_close'],
        name=competitor_ticker, line=dict(color='#BE8A09'),
        hovertemplate='Normalized Price: %{y:.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=benchmark_data['date'], y=benchmark_data['normalized_close'],
        name=benchmark_ticker, line=dict(color='gray'),
        hovertemplate='Normalized Price: %{y:.2f}<extra></extra>'
    ))

    # Increase text size in layout, set x-axis hoverformat and add unified hover mode
    fig.update_layout(
        title=dict(
            text=f'Normalized Price Comparison: {selected_ticker} vs {competitor_ticker} vs {benchmark_ticker}',
            font=dict(size=24)
        ),
        xaxis=dict(
            title="Date",
            titlefont=dict(size=18),
            tickfont=dict(size=16),
            hoverformat='%Y-%m-%d'  # Format x value in hover label
        ),
        yaxis=dict(
            title="Normalized Price",
            titlefont=dict(size=18),
            tickfont=dict(size=16)
        ),
        legend=dict(
            font=dict(size=16)
        ),
        hoverlabel=dict(
            font_size=14
        ),
        width=1200,
        height=400,
        hovermode='x unified'
    )

    return fig

def create_correlation_matrix_figure(corr_matrix):
    custom_scale = [
        [0.0, "white"],
        [0.5, "#ff6666"],
        [1.0, "#211A23"]  # Higher values from 0.5 to 1.0 transition to a deeper red
    ]
    
    fig = px.imshow(
        corr_matrix,
        text_auto=False,
        color_continuous_scale=custom_scale,
        title='Correlation of Daily Returns'
    )
    # Update the hover template to show the value with two decimals
    fig.update_traces(hovertemplate=' %{x} ↔ %{y}<br>r: %{z:.2f}')

    # Increase text size in layout
    fig.update_layout(

        xaxis=dict(
            title="Ticker",
            titlefont=dict(size=18),  # Increase x-axis title font size
            tickfont=dict(size=12)  # Increase x-axis tick font size
        ),
        yaxis=dict(
            title="Ticker",
            titlefont=dict(size=18),  # Increase y-axis title font size
            tickfont=dict(size=12)  # Increase y-axis tick font size
        ),
        legend=dict(
            font=dict(size=16)  # Increase legend font size
        ),
        hoverlabel=dict(
            font_size=14  # Increase hover text font size
        ),
        width=1000,  # Increase figure width
        height=800  # Increase figure height
    )

    return fig

def create_price_chart(ticker_data, selected_ticker, high_52w, low_52w):
    """
    Create a line chart for the ticker's closing prices with:
    - 50-day and 200-day moving averages
    - 52-week high & low horizontal lines (only for last 52 weeks)
    - Shaded gray area between 52-week high & low (only for last 52 weeks)
    """

    # Determine the start date for the last 52 weeks
    last_52_weeks_start = ticker_data['date'].max() - pd.Timedelta(weeks=52)

    # Filter data to include only the last 52 weeks
    recent_data = ticker_data[ticker_data['date'] >= last_52_weeks_start].copy()

    fig = go.Figure()

    # Closing Prices Line
    fig.add_trace(go.Scatter(
        x=ticker_data['date'], y=ticker_data['close'],
        mode='lines', name='Closing Price', line=dict(color='#007bff'),
        hovertemplate='%{y:.2f}'
    ))

    # 50-Day Moving Average Line
    if len(ticker_data) >= 50:
        ticker_data.loc[:, '50d_MA'] = ticker_data['close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=ticker_data['date'], y=ticker_data['50d_MA'],
            mode='lines', name='50-Day MA', line=dict(color='#ffcc00', dash='dot'),
            hovertemplate='%{y:.2f}'
        ))

    # 200-Day Moving Average Line
    if len(ticker_data) >= 200:
        ticker_data.loc[:, '200d_MA'] = ticker_data['close'].rolling(window=200).mean()
        fig.add_trace(go.Scatter(
            x=ticker_data['date'], y=ticker_data['200d_MA'],
            mode='lines', name='200-Day MA', line=dict(color='#ff6666', dash='dot'),
            hovertemplate='%{y:.2f}'
        ))

    # 52-Week High & Low Horizontal Lines (only for last 52 weeks)
    fig.add_trace(go.Scatter(
        x=[last_52_weeks_start, ticker_data['date'].max()], 
        y=[high_52w, high_52w], 
        mode='lines', 
        name='52-Week High', 
        line=dict(color='gray', width=2, dash='dash'),
        hovertemplate='%{y:.2f}'
    ))

    fig.add_trace(go.Scatter(
        x=[last_52_weeks_start, ticker_data['date'].max()], 
        y=[low_52w, low_52w], 
        mode='lines', 
        name='52-Week Low', 
        line=dict(color='gray', width=2, dash='dash'),
        hovertemplate='%{y:.2f}'
    ))

    # Shaded Area Between 52-Week High & Low (only for last 52 weeks)
    fig.add_trace(go.Scatter(
        x=[last_52_weeks_start, ticker_data['date'].max(), ticker_data['date'].max(), last_52_weeks_start],
        y=[low_52w, low_52w, high_52w, high_52w],
        fill='toself',
        fillcolor='rgba(128, 128, 128, 0.2)',  # Light gray shade
        line=dict(width=0), 
        name="52-Week Range",
        hoverinfo='skip'
    ))

    fig.update_layout(
    title=dict(text=f'{selected_ticker} Closing Prices', font=dict(size=24)),  # Increase title font size
    xaxis=dict(
        title="Date",
        titlefont=dict(size=18),  # Increase x-axis title font size
        tickfont=dict(size=16)  # Increase x-axis tick font size
    ),
    yaxis=dict(
        title="Price",
        titlefont=dict(size=18),  # Increase y-axis title font size
        tickfont=dict(size=16)  # Increase y-axis tick font size
    ),
    legend=dict(font=dict(size=16)),  # Increase legend font size
    hoverlabel=dict(font_size=14),  # Increase hover text font size
    width=1200,  # Increase figure width
    height=500,  # Increase figure height
    hovermode='x unified'
    )

    return fig