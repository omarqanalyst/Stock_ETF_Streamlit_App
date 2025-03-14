def generate_trade_advice(
    closing_price,
    fifty_day_ma,
    two_hundred_day_ma,
    wk52_high,
    wk52_low,
    recent_3d_high=None,
    below_50dma_3days=False
):
    """
    Generate a dynamic recommendation string and an action label based on momentum trading rules without volume data.
    """

    wk52_range = wk52_high - wk52_low
    wk52_midpoint = wk52_low + 0.5 * wk52_range

    action = "HOLD"
    message = ""

    uptrend = fifty_day_ma > two_hundred_day_ma and closing_price > fifty_day_ma and closing_price > two_hundred_day_ma
    bullish_breakout = closing_price >= wk52_high * 1.02 and closing_price >= wk52_low + 0.9 * wk52_range

    # --- Uptrend scenarios ---
    if uptrend:
        if bullish_breakout:
            action = "BUY"
            message = (
                f"STRONG BUY: The 50-day moving average ({fifty_day_ma:.2f}) is above the 200-day average ({two_hundred_day_ma:.2f}), "
                f"and the closing price ({closing_price:.2f}) broke 2% above the 52-week high ({wk52_high:.2f})."
            )
        elif closing_price >= wk52_midpoint:
            action = "BUY"
            message = (
                f"MODERATE BUY: The 50-day moving average ({fifty_day_ma:.2f}) remains above the 200-day ({two_hundred_day_ma:.2f}), "
                f"and the price ({closing_price:.2f}) is above the 52-week midpoint ({wk52_midpoint:.2f}). "
                "This implies continued positive momentum, though monitoring short-term pullbacks is recommended."
            )
        else:
            action = "WAIT"
            message = (
                "WAIT: Price and averages suggest an uptrend; however, no clear breakout has formed. "
                "Keep an eye on price behavior near recent resistance levels for potential entry."
            )

    # --- Ambiguous or bearish scenarios ---
    elif fifty_day_ma < two_hundred_day_ma:
        # If price is still above the 50-day, we treat it as ambiguous and WAIT
        if closing_price >= fifty_day_ma:
            action = "WAIT"
            message = (
                f"WAIT: The 50-day average ({fifty_day_ma:.2f}) is below the 200-day ({two_hundred_day_ma:.2f}), "
                f"but the closing price ({closing_price:.2f}) remains above the 50-day. "
                "This setup is ambiguous; monitor for either a breakdown below support or a breakout above resistance"
            )
        # Otherwise, check existing strong or moderate sell signals
        elif (closing_price < fifty_day_ma and closing_price < two_hundred_day_ma) or (
            recent_3d_high and closing_price <= recent_3d_high * 0.95
        ):
            if below_50dma_3days or closing_price < wk52_midpoint:
                action = "SELL"
                message = (
                    f"STRONG SELL: The 50-day average ({fifty_day_ma:.2f}) is below the 200-day ({two_hundred_day_ma:.2f}), "
                    f"and the closing price ({closing_price:.2f}) indicates a downward shift. "
                    "Exiting now may prevent deeper losses, but reevaluate if support levels hold."
                )
            elif closing_price <= wk52_low * 0.98:
                action = "SELL"
                message = (
                    f"MODERATE SELL: The price ({closing_price:.2f}) is at least 2% below the 52-week low ({wk52_low:.2f}). "
                    "Signals potential further downside risk."
                )
            else:
                action = "WAIT"
                message = (
                    "Momentum shows bearish signs, but not conclusive for an immediate exit. "
                    "Consider waiting for a clearer breakdown."
                )
        else:
            action = "HOLD"
            message = (
                "HOLD: The 50-day is below the 200-day, but current price action doesn’t conclusively confirm more downside. "
                "Observe whether the trend strengthens or weakens from here."
            )
    else:
        action = "HOLD"
        message = (
            f"The closing price ({closing_price:.2f}) is near the 50-day or 200-day averages, "
            "suggesting a sideways market."
        )

    return action, message