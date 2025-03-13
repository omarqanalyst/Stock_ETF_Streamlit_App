def _build_message(forecast_date_str, trend_direction, forecast_min, forecast_max, latest_prediction, action_type):
    """
    Build a forecast message.
    """
    base = (
        f"As of {forecast_date_str}, the overall trend is {trend_direction} with forecasted volatility "
        f"ranging from {forecast_min:.2f} to {forecast_max:.2f}. The latest prediction of {latest_prediction:.2f} indicates "
    )
    if action_type == "ALERT":
        return base + "above-normal risk. Suggest enacting hedges."
    elif action_type == "MONITOR":
        return base + "moderate volatility. Continue monitoring."
    return "No forecast data found. Continue to observe market conditions."

def generate_forecasting_advice(forecast_data, historical_data, threshold=0.6):
    """
    Generate a dynamic recommendation string and action label based on volatility forecast.
    
    Returns:
        tuple: (action, message, last_date)
    """
    last_date = historical_data['date'].max()
    forecast_data_after_last_date = forecast_data[forecast_data['ds'] >= last_date]

    if forecast_data_after_last_date.empty:
        return "MONITOR", "No forecast data found. Continue to observe market conditions.", last_date

    first_forecasted_row = forecast_data_after_last_date.iloc[0]
    latest_prediction = first_forecasted_row['yhat'] # first prediction after historical data ends
    forecast_date_str = first_forecasted_row['ds'].strftime('%b %d, %Y')

    forecast_min = forecast_data_after_last_date['yhat'].min()
    forecast_max = forecast_data_after_last_date['yhat'].max()

    trend_difference = (
        forecast_data_after_last_date['yhat'].iloc[-1]
        - forecast_data_after_last_date['yhat'].iloc[0]
    ) # could improve or make it more fine grained
    trend_direction = "increasing" if trend_difference > 0 else "decreasing"

    action = "ALERT" if latest_prediction > threshold else "MONITOR"
    message = _build_message(forecast_date_str, trend_direction, forecast_min, forecast_max, latest_prediction, action)

    return action, message, last_date