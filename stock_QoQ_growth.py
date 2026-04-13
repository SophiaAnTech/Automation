!pip install yfinance

# get the latest QoQ growth

import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]

def calculate_qoq_growth(ticker_list):
    growth_data = []
    
    for symbol in ticker_list:
        ticker = yf.Ticker(symbol)
        q_fin = ticker.quarterly_financials
        
        if q_fin.shape[1] >= 2:
            latest_rev = q_fin.iloc[:, 0].get("Total Revenue", 0)
            previous_rev = q_fin.iloc[:, 1].get("Total Revenue", 0)
            
            if previous_rev > 0:
                qoq_growth = ((latest_rev - previous_rev) / previous_rev) * 100
                
                growth_data.append({
                    "Ticker": symbol,
                    "Latest Quarter": q_fin.columns[0].strftime('%Y-%m-%d'),
                    "Prev Quarter": q_fin.columns[1].strftime('%Y-%m-%d'),
                    "Latest Rev ($B)": round(latest_rev / 1e9, 2),
                    "Prev Rev ($B)": round(previous_rev / 1e9, 2),
                    "QoQ Growth (%)": round(qoq_growth, 2)
                })
                
    df = pd.DataFrame(growth_data)
    return df.sort_values(by="QoQ Growth (%)", ascending=False)

df_growth = calculate_qoq_growth(tickers)
print(df_growth.to_string(index=False))
