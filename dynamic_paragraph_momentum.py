def generate_trade_advice(CP, ma50, ma200, wk52_high, wk52_low, recent_high_3d=None, cp_below_50_consecutive=False):
    """
    Generate a dynamic recommendation string and an action label based on momentum trading rules without volume data.
    
    Parameters:
        CP (float): Current closing price.
        ma50 (float): 50-day moving average.
        ma200 (float): 200-day moving average.
        wk52_high (float): 52-week high.
        wk52_low (float): 52-week low.
        recent_high_3d (float, optional): The highest closing price over the past 3 days.
        cp_below_50_consecutive (bool): True if CP has closed below the 50DMA for three consecutive days.
        
    Returns:
        tuple: (action, message)
            action (str): One of "BUY", "SELL", "WAIT", or "HOLD".
            message (str): Recommendation explanation without explicit “BUY”/“SELL” labels.
    """
    wk52_range = wk52_high - wk52_low
    wk52_midpoint = wk52_low + 0.5 * wk52_range
    
    action = "HOLD"
    message = ""  # Explanation text

    # --- Buy Conditions (Uptrend Confirmation) ---
    if ma50 > ma200 and CP > ma50 and CP > ma200:
        if CP >= wk52_high * 1.02 and CP >= wk52_low + 0.9 * wk52_range:
            action = "BUY"
            message = (
                f"The 50-day moving average ({ma50:.2f}) is above the 200-day average ({ma200:.2f}), "
                f"with the closing price ({CP:.2f}) breaking at least 2% above the 52-week high ({wk52_high:.2f}), "
                "indicating a strong bullish breakout. Consider a stop-loss below the 50-day average."
            )
        elif CP >= wk52_midpoint:
            action = "BUY"
            message = (
                f"The 50-day moving average ({ma50:.2f}) remains above the 200-day ({ma200:.2f}). "
                f"The price ({CP:.2f}) is above both and has held above the 52-week midpoint ({wk52_midpoint:.2f}), "
                "suggesting ongoing bullish momentum. A stop-loss near support may help manage risk."
            )
        else:
            action = "WAIT"
            message = (
                "While price and averages suggest an uptrend, there is no clear breakout or confirmed rebound. "
                "Monitor for stronger bullish signals before committing."
            )

    # --- Sell Conditions (Momentum Breakdown) ---
    elif (ma50 < ma200 and CP < ma50 and CP < ma200) or (recent_high_3d and CP <= recent_high_3d * 0.95):
        if (cp_below_50_consecutive or CP < wk52_midpoint) or (recent_high_3d and CP <= recent_high_3d * 0.95):
            action = "SELL"
            trigger = []
            if recent_high_3d and CP <= recent_high_3d * 0.95:
                trigger.append(f"price is over 5% below the recent high of {recent_high_3d:.2f}")
            if cp_below_50_consecutive or CP < wk52_midpoint:
                trigger.append("price remains weak below the 50-day average or 52-week midpoint")

            joined_triggers = " and ".join(trigger)
            message = (
                f"The 50-day average ({ma50:.2f}) is below the 200-day ({ma200:.2f}), "
                f"and the closing price ({CP:.2f}) is under both. Additionally, {joined_triggers}, "
                "indicating a clear downward shift. Exiting the position now can protect against further losses."
            )
        elif CP <= wk52_low * 0.98:
            action = "SELL"
            message = (
                f"The price ({CP:.2f}) is at least 2% below the 52-week low ({wk52_low:.2f}), "
                "signaling a potential bearish move. Reducing or closing the position may safeguard capital."
            )
        else:
            action = "WAIT"
            message = (
                "Bearish indicators appear, but not conclusively enough for immediate action. "
                "Watch for further downside confirmation before making a decision."
            )

    # --- Hold Conditions (Sideways or Indecisive Market) ---
    else:
        action = "HOLD"
        message = (
            f"The closing price ({CP:.2f}) is moving between the 50-day and 200-day averages, "
            "with momentum remaining neutral. Waiting for a clear breakout or breakdown is prudent."
        )

    return action, message