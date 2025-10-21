import finnhub
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import time 

def getTopMarketNews():
    try:
        # Note: API key is hardcoded here, which is generally bad practice. 
        # It's better to pass it or load it from an environment variable.
        finnhub_client = finnhub.Client(api_key="d1no9l1r01qovv8kh4n0d1no9l1r01qovv8kh4ng")
        urlLink = []
        noOfNews = 0
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
    report earnings within the current US market calendar day, suitable for a chat bot.
    
    The date is calculated using a time zone offset (SGT - 12 hours) to align 
    with the US Eastern Time calendar, making the results relevant for an SGT user.
    """
    print("--- Starting Earnings Calendar Fetch (via NASDAQ Data) ---")
    
    # ------------------------------------------------------------------
    # ADJUSTMENT FOR SGT TIME ZONE (Moved US_MARKET_OFFSET_HOURS here to resolve NameError)
    # ------------------------------------------------------------------
    # Approximate offset for US Eastern Time (ET) from SGT (UTC+8).
    # SGT (UTC+8) is 12 hours ahead of EDT (UTC-4)
    US_MARKET_OFFSET_HOURS = 12 
    
    # Get current time (SGT) and apply offset to find the current US market date.
    # This ensures that even early morning SGT runs fetch the correct day's data.
    current_sgt_datetime = datetime.now()
    us_market_datetime = current_sgt_datetime - timedelta(hours=US_MARKET_OFFSET_HOURS)
    today = us_market_datetime.date() # This is the US calendar date
    # ------------------------------------------------------------------
    
    # Check only today
    date_range = [today] 
    all_earnings = []
    
    # 1. Fetch data for each day in the range
    for i, date in enumerate(date_range):
        date_str = date.strftime("%Y-%m-%d")
        # Keep this print for console feedback during execution
        print(f"Checking earnings scheduled for {date_str} (US Market Date)...") 
        
        daily_earnings = fetch_earnings_data(date_str)
        
        # FIX: Ensure daily_earnings is iterable before calling extend()
        if daily_earnings is not None:
            all_earnings.extend(daily_earnings)
        else:
            # This logs an unexpected NoneType return, which should not happen 
            # with the current fetch_earnings_data implementation, but acts as 
            # a safeguard if the external function is modified or fails oddly.
            print(f"    - WARNING: fetch_earnings_data for {date_str} returned None, skipping extension.")

        # Add a small delay between requests to be polite to the server
        if i < len(date_range) - 1:
            time.sleep(1) 

    if not all_earnings:
        # Updated message to reflect checking only today
        return "✅ No earnings announcements found for today (US Market Date)."

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
        f"📅 Date Range (Based on US Market Calendar): {today.strftime('%b %d, %Y')}\n" 
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
