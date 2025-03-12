# Pinterest ETF Analysis Dashboard

This project provides a comprehensive dashboard for analyzing Pinterest's stock performance against its peers using the SOCL ETF as a benchmark. Built with Streamlit, it features data loading, preprocessing, and visualization capabilities. Key functionalities include comparative analysis, correlation analysis, volatility forecasting, and key metrics overview. The dashboard leverages AWS services for data storage and processing, including S3, AWS Glue, and AWS Athena.

## Installation

Install the required packages with:

```sh
pip install -r requirements.txt
```

## Usage

Run the dashboard with:

```sh
streamlit run pinterest_dashboard.py
```

## Sample Dataset

```csv
"date","ticker","close","high","low","open","volume","etf"
"2024-03-21","RDDT","50.439998626708984","57.79999923706055","45.04999923706055"
"2024-03-22","RDDT","46.0","51.6","45.34000015258789","48.880001068115234","1598"
