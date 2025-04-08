# Pinterest ETF Analysis Dashboard

View here: https://pinterest.streamlit.app/

![Screenshot 2025-04-08 135813](https://github.com/user-attachments/assets/0a371397-740c-4a21-8329-bca5d870baa8)

This project is a Streamlit dashboard that analyzes Pinterest’s stock performance relative to its peers, using the SOCL ETF as a benchmark.

## Key Features

- **Comparative analysis**: See how Pinterest stacks up against other social media stocks.  
- **Correlation analysis**: Explore relationships between stock movements.  
- **Volatility forecasting**: Anticipate potential price swings.  
- **Key metrics overview**: Get a snapshot of financial and performance indicators.  

## Tech Stack

- **Frontend**: Built with Streamlit for quick development and interactive visuals.  
- **Data pipeline**:  
  - Data stored in **AWS S3**  
  - Processed using **AWS Glue**  
  - Queried via **AWS Athena**

## Why It Matters

This project demonstrates how to integrate multiple technologies into a single, user-friendly dashboard.

## View the Dashboard

[https://pinterest.streamlit.app/](https://pinterest.streamlit.app/)


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
