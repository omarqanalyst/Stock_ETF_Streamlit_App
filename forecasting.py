# forecasting.py
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

def create_volatility_forecast(data, periods=90):
    """
    Create a 90-day volatility forecast using Prophet.
    """
    # Prepare data for Prophet
    volatility = data[['date', '30d_volatility']].rename(columns={'date': 'ds', '30d_volatility': 'y'})
    volatility['ds'] = pd.to_datetime(volatility['ds'])
    
    # Build and fit the model
    model = Prophet(seasonality_mode='additive')
    model.fit(volatility)
    
    # Create future dataframe and predict
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Build the Plotly figure for historical and forecasted volatility
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=volatility['ds'], 
        y=volatility['y'], 
        name='Historical Volatility',
        line=dict(color='#3B6A6A'),
        hovertemplate='Date: %{x|%Y-%m-%d}<br>Volatility: %{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast['ds'], 
        y=forecast['yhat'], 
        name='Forecasted Volatility',
        line=dict(color='#9D2A2E'),
        hovertemplate='Date: %{x|%Y-%m-%d}<br>Forecast: %{y:.2f}<extra></extra>'
    ))
    
    # Hide hover for the upper bound trace
    fig.add_trace(go.Scatter(
        x=forecast['ds'], 
        y=forecast['yhat_upper'], 
        fill=None, 
        mode='lines', 
        line=dict(width=0), 
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Uncertainty Interval trace with custom hover formatting
    fig.add_trace(go.Scatter(
        x=forecast['ds'], 
        y=forecast['yhat_lower'], 
        fill='tonexty', 
        mode='lines', 
        line=dict(width=0), 
        name='Uncertainty Interval',
        fillcolor='rgba(255, 0, 0, 0.2)',
        hovertemplate='Date: %{x|%Y-%m-%d}<br>Uncertainty: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='90-Day Volatility Forecast', font=dict(size=24)),  # Increased title font size
        xaxis=dict(
            title='Date',
            titlefont=dict(size=18),  # Increased x-axis title font size
            tickfont=dict(size=16)  # Increased x-axis tick font size
        ),
        yaxis=dict(
            title='Volatility',
            titlefont=dict(size=18),  # Increased y-axis title font size
            tickfont=dict(size=16)  # Increased y-axis tick font size
        ),
        hovermode='x unified',
        legend=dict(font=dict(size=12)),  # Increased legend font size
        hoverlabel=dict(font_size=14),  # Increased hover text font size
        width=1200,  # Increased figure width
        height=500  # Increased figure height
    )

    
    return fig
