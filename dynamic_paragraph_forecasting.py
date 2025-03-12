def generate_forecasting_advice(forecast_data, historical_data):
    """
    Generate a dynamic recommendation string and action label based on volatility forecast.
    
    Parameters:
        forecast_data (pd.DataFrame): The forecast DataFrame from Prophet, containing columns like
                                      'yhat', 'yhat_lower', 'yhat_upper', and 'ds'.
        historical_data (pd.DataFrame): The historical DataFrame containing past data with a 'date' column.

    Returns:
        tuple: (action, message, last_date)
            action (str): One of "MONITOR", "ALERT", or another suitable label.
            message (str): Explanation of the forecast, recommending steps or actions.
            last_date: The latest historical date.
    """
    # Get the last date in historical data
    last_date = historical_data['date'].max()

    # Find the first forecasted row starting from that date
    forecast_row = forecast_data[forecast_data['ds'] >= last_date].iloc[0]
    latest_prediction = forecast_row['yhat']
    forecast_date = forecast_row['ds']
    # Format forecast_date as "Mar 03, 2025"
    forecast_date_formatted = forecast_date.strftime('%b %d, %Y')

    # Find forecast range and trend
    forecast_sub = forecast_data[forecast_data['ds'] >= last_date]
    forecast_min = forecast_sub['yhat'].min()
    forecast_max = forecast_sub['yhat'].max()
    trend_calc = forecast_sub['yhat'].iloc[-1] - forecast_sub['yhat'].iloc[0]
    trend_direction = "increasing" if trend_calc > 0 else "decreasing"

    # Example logic: if final forecasted volatility exceeds a threshold, switch action from MONITOR to ALERT
    if not forecast_sub.empty:
        if latest_prediction > 0.6:
            action = "ALERT"
            message = (
                f"As of {forecast_date_formatted}, the overall trend is {trend_direction} with forecasted volatility "
                f"ranging from {forecast_min:.2f} to {forecast_max:.2f}. The latest prediction of {latest_prediction:.2f} indicates "
                f"above-normal risk. Suggest enacting hedges."
            )
        else:
            action = "MONITOR"
            message = (
                f"As of {forecast_date_formatted}, the overall trend is {trend_direction} with forecasted volatility "
                f"ranging from {forecast_min:.2f} to {forecast_max:.2f}. The latest prediction of {latest_prediction:.2f} indicates "
                f"moderate volatility. Continue monitoring."
            )
    else:
        action = "MONITOR"
        message = "No forecast data found. Continue to observe market conditions."

    return action, message, last_date