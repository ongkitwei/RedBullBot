import finnhub
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import time 

def getTopMarketNews():
    try:
        finnhub_client = finnhub.Client(api_key="d1no9l1r01qovv8kh4n0d1no9l1r01qovv8kh4ng")
        urlLink = []
        noOfNews = 0
        # allNews = json.dumps(finnhub_client.general_news('general', min_id=0), indent=2)
        rawNews = finnhub_client.general_news('general', min_id=0)

        for x in rawNews:
            if x["source"] == "CNBC":
                if noOfNews < 4:
                    urlLink.append({"headline": x["headline"], "url": x["url"]})
                    noOfNews+=1
                else:
                    break
        print(urlLink)
        return urlLink
    except requests.exceptions.ReadTimeout:
            print("⚠️ Finnhub request timed out. Skipping news fetch.")
            return []

    except Exception as e:
        print(f"⚠️ Unexpected error fetching news: {e}")
        return []

def fetch_earnings_data(date_str):
    """
    Fetches earnings data for a single specified date from the NASDAQ earnings API.
    
    Args:
        date_str (str): Date in YYYY-MM-DD format.
        
    Returns:
        list: A list of dicts containing earnings data, or an empty list on failure.
    """
    url = "https://api.nasdaq.com/api/calendar/earnings"
    headers = {
        # Using a standard User-Agent to mimic a browser and avoid blocking
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.nasdaq.com",
        "Referer": "https://www.nasdaq.com/market-activity/earnings"
    }
    
    params = {
        'date': date_str,
        'region': 'US'
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        
        # Check the nested data structure
        if data and 'data' in data and 'rows' in data['data']:
            return data['data']['rows']
        
        return []

    except requests.exceptions.RequestException as e:
        print(f"    - Error fetching data for {date_str}: {e}")
        return []
    except json.JSONDecodeError:
        print(f"    - Error decoding JSON response for {date_str}. The endpoint might be temporarily unstable.")
        return []

def find_upcoming_earnings():
    """
    Fetches and returns a single formatted string of all stocks scheduled to 
    report earnings within the current calendar day, suitable for a chat bot.
    (Approximating a 24-hour window: run time until midnight tonight.)
    """
    print("--- Starting Earnings Calendar Fetch (via NASDAQ Data) ---")
    
    # Define the date range: Only Today (Approximates 24 hours from run time)
    today = datetime.now().date()
    
    # Check only today
    date_range = [today] 
    all_earnings = []
    
    # 1. Fetch data for each day in the range
    for i, date in enumerate(date_range):
        date_str = date.strftime("%Y-%m-%d")
        # Keep this print for console feedback during execution
        print(f"Checking earnings scheduled for {date_str}...") 
        
        daily_earnings = fetch_earnings_data(date_str)
        all_earnings.extend(daily_earnings)
        
        # Add a small delay between requests to be polite to the server
        if i < len(date_range) - 1:
            time.sleep(1) 

    if not all_earnings:
        # Updated message to reflect checking only today
        return "✅ No earnings announcements found for today."

    # 2. Process Data
    
    earnings_df = pd.DataFrame(all_earnings)
    
    # Define the columns we want to select and their desired display names
    base_columns = ['symbol', 'name', 'time', 'fiscalQuarterEnding']
    optional_columns = {'epsEstimate': 'EPS Est.'}
    
    # Check which columns actually exist in the DataFrame (robustness against KeyError)
    available_columns = [col for col in base_columns if col in earnings_df.columns]
    
    final_columns = available_columns
    column_mapping = {
        'symbol': 'Ticker',
        'name': 'Company Name',
        'time': 'Release Time',
        'fiscalQuarterEnding': 'Fiscal Qtr.'
    }
    
    for api_col, display_col in optional_columns.items():
        if api_col in earnings_df.columns:
            final_columns.append(api_col)
            column_mapping[api_col] = display_col

    results = earnings_df[final_columns].copy() 
    results.rename(columns=column_mapping, inplace=True)

    results['Release Time'] = results['Release Time'].replace({
        'BMO': 'Before Market Open', 
        'AMC': 'After Market Close', 
        'Time Not Supplied': 'Time Not Specified'
    })
    
    results = results.fillna('N/A')

    # 3. Format output for return string
    
    formatted_lines = [
        "<b>📈 Upcoming Earnings Announcements📈</b>",
        # Updated header to reflect only today's date
        f"📅 Date Range: {today.strftime('%b %d, %Y')}\n" 
    ]
    
    for index, row in results.iterrows():
        
        # Build the main line with Ticker and Company Name
        ticker_line = f"▶️ <b>{row['Ticker']}</b> ({row['Company Name']})"
        
        # Build the detail line with other data
        details = [
            f"Time: {row['Release Time']}",
            f"Qtr: {row['Fiscal Qtr.']}"
        ]
        
        # Conditionally add EPS Est.
        if 'EPS Est.' in results.columns:
            details.append(f"EPS Est.: {row['EPS Est.']}")
            
        details_line = "  - " + " | ".join(details)
        
        formatted_lines.append(ticker_line)
        formatted_lines.append(details_line)
        formatted_lines.append("") # Empty line for separation

    # Return the clean, joined output string
    return '\n'.join(formatted_lines).strip()
