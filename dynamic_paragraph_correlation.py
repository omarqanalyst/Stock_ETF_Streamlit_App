import pandas as pd
import streamlit as st

def generate_correlation_advice(corr_matrix, selected_ticker):
    """
    Generate a dynamic recommendation string based on the correlation analysis.
    
    Parameters:
        corr_matrix (pd.DataFrame): A correlation matrix with tickers as index & columns.
        selected_ticker (str): The ticker selected by the user.
        
    Returns:
        tuple: (top_table DataFrame, bottom_table DataFrame, error message or None)
    """
    selected_corr = corr_matrix.get(selected_ticker)
    if selected_corr is None:
        return None, None, "Correlation data is not available for the selected ticker."
    
    try:
        correlations = corr_matrix.loc[selected_ticker].drop([selected_ticker, 'SOCL'])
    except KeyError as e:
        return None, None, f"Error: {e} - It looks like a column name might be misspelled or missing."
    
    if correlations.empty:
        return None, None, "Not enough data available to compare correlations."
    
    num_correlations = 3  # Number of correlations to retrieve
    # Get top and bottom correlations rounded to two decimals
    top_corr = correlations.nlargest(num_correlations).round(2)
    bottom_corr = correlations.nsmallest(num_correlations).round(2)
    
    # Build top table with combined ticker and correlation values
    top_table = pd.DataFrame({
        'Ticker': top_corr.index,
        'Correlation': top_corr.values
    })
    top_table = top_table.sort_values(by='Correlation', ascending=False)
    top_table['Correlation'] = top_table['Correlation'].map('{:.2f}'.format)
    
    top_table['Combined'] = top_table.apply(lambda row: f"{row['Ticker']} ({row['Correlation']})", axis=1)
    
    # Keep only the Combined column and rename it
    top_table = top_table[['Combined']]
    top_table.columns = ['Ticker']
    
    # Remove the index and start it at 1
    top_table.reset_index(drop=True, inplace=True)
    top_table.index += 1
    top_table.index.name = "Rank"
    
    # Build bottom table with combined ticker and correlation values
    bottom_table = pd.DataFrame({
        'Ticker': bottom_corr.index,
        'Correlation': bottom_corr.values
    })
    bottom_table = bottom_table.sort_values(by='Correlation', ascending=True)
    bottom_table['Correlation'] = bottom_table['Correlation'].map('{:.2f}'.format)
    
    bottom_table['Combined'] = bottom_table.apply(lambda row: f"{row['Ticker']} ({row['Correlation']})", axis=1)
    
    # Keep only the Combined column and rename it
    bottom_table = bottom_table[['Combined']]
    bottom_table.columns = ['Ticker']
    
    # Remove the index and start it at 1
    bottom_table.reset_index(drop=True, inplace=True)
    bottom_table.index += 1
    bottom_table.index.name = "Rank"
    
    return top_table, bottom_table, None

def display_correlation_tables(top_str, bottom_str):
    """
    Display correlation tables as formatted text.

    Parameters:
        top_str (str): Formatted text for top correlations (e.g., "SNAP (0.38) META (0.29) YALA (0.27)")
        bottom_str (str): Formatted text for lowest correlations (similar format)
    """
    
    st.markdown(f"**Top Correlations:**  {top_str}")
    st.markdown(f"**Lowest Correlations:**  {bottom_str}")