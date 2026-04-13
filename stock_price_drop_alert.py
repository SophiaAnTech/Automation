import yfinance as yf
import time
from datetime import datetime

# Configuration
WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]
CHECK_INTERVAL = 60  
DROP_THRESHOLD = 0.05  

def get_prices(tickers):
    # Use group_by='ticker' to make the data easier to parse
    data = yf.download(tickers, period="1d", interval="1m", progress=False, group_by='ticker')
    
    current_prices = {}
    for ticker in tickers:
        # Get the very last valid price for each ticker
        # We handle the multi-index by accessing [ticker]['Close']
        ticker_stats = data[ticker]['Close']
        current_prices[ticker] = ticker_stats.dropna().iloc[-1]
        
    return current_prices

def monitor_watchlist():
    print(f"Monitoring {len(WATCHLIST)} stocks for a {DROP_THRESHOLD*100}% drop...")
    
    try:
        # Initial baselines
        baselines = get_prices(WATCHLIST)
        for ticker, price in baselines.items():
            print(f"Initial {ticker}: ${price:.2f}")
    except Exception as e:
        print(f"Error during initialization: {e}")
        return

    while True:
        try:
            current_prices = get_prices(WATCHLIST)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n--- Update: {timestamp} ---")

            for ticker in WATCHLIST:
                current_p = current_prices[ticker]
                baseline_p = baselines[ticker]
                
                change = (current_p - baseline_p) / baseline_p
                
                print(f"{ticker:5}: ${current_p:>8.2f} | Change: {change:>7.2%}")

                if change <= -DROP_THRESHOLD:
                    print(f"!!! ALERT: {ticker} dropped by {abs(change):.2%} !!!")
                    baselines[ticker] = current_p 
                
                elif current_p > baseline_p:
                    baselines[ticker] = current_p

        except Exception as e:
            print(f"Error during check: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_watchlist()
