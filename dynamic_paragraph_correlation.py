import pandas as pd

def generate_correlation_advice(corr_matrix, selected_ticker):
    """
    Generate a dynamic recommendation string based on the correlation analysis.
    
    Parameters:
        corr_matrix (pd.DataFrame): A correlation matrix with tickers as index & columns.
        selected_ticker (str): The ticker selected by the user.
        
    Returns:
        tuple: (top_table DataFrame, bottom_table DataFrame, error message or None)
    """
    if selected_ticker not in corr_matrix.index:
        return None, None, "Correlation data is not available for the selected ticker."
    
    correlations = corr_matrix.loc[selected_ticker].drop([selected_ticker, 'SOCL'], errors='ignore')
    if correlations.empty:
        return None, None, "Not enough data available to compare correlations."
    
    # Get top 3 and bottom 3 correlations rounded to two decimals
    top_3_corr = correlations.nlargest(3).round(2)
    bottom_3_corr = correlations.nsmallest(3).round(2)
    
    # Build top table with combined ticker and correlation values
    top_table = pd.DataFrame({
        'Ticker': top_3_corr.index,
        'Correlation': top_3_corr.values
    })
    top_table = top_table.sort_values(by='Correlation', ascending=False)
    top_table['Correlation'] = top_table['Correlation'].map('{:.2f}'.format)
    
    # Create combined column in the format "TICKER (0.XX)"
    top_table['Combined'] = top_table['Ticker'] + ' (' + top_table['Correlation'] + ')'
    
    # Keep only the Combined column and rename it
    top_table = top_table[['Combined']]
    top_table.columns = ['Ticker']
    
    # Remove the index and start it at 1
    top_table.reset_index(drop=True, inplace=True)
    top_table.index += 1
    top_table.index.name = "Rank"
    
    # Build bottom table with combined ticker and correlation values
    bottom_table = pd.DataFrame({
        'Ticker': bottom_3_corr.index,
        'Correlation': bottom_3_corr.values
    })
    bottom_table = bottom_table.sort_values(by='Correlation', ascending=True)
    bottom_table['Correlation'] = bottom_table['Correlation'].map('{:.2f}'.format)
    
    # Create combined column in the format "TICKER (0.XX)"
    bottom_table['Combined'] = bottom_table['Ticker'] + ' (' + bottom_table['Correlation'] + ')'
    
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
    import streamlit as st
    
    st.markdown(f"**Top Correlations:**  {top_str}")
    st.markdown(f"**Lowest Correlations:**  {bottom_str}")