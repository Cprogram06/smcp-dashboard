import requests
import csv
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

def get_handles_from_csv(file_path):
    """
    Load Twitter handles from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing Twitter handles.
    
    Returns:
        list: List of Twitter handles from the CSV file.
    """
    handles = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            handles.extend(row)
    return handles

def get_tweet_count(query, start_time, end_time):
    """
    Get the count of tweets for a specified query within a time range.
    
    Args:
        query (str): Twitter handle or search query.
        start_time (datetime): Start time of the query.
        end_time (datetime): End time of the query.
    
    Returns:
        int: Total count of tweets for the given query and time range.
    """
    endpoint_url = "https://api.twitter.com/2/tweets/counts/recent"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent": "TwitterDevSampledStreamQuickStartPython",
        "Content-Type": "application/json"
    }
    
    # Convert datetime objects to ISO format strings
    iso_start_time = start_time.isoformat() + "Z"
    iso_end_time = end_time.isoformat() + "Z"
    
    params = {
        "query": query,
        "start_time": iso_start_time,
        "end_time": iso_end_time
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(endpoint_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("meta", {}).get("total_tweet_count", 0)

        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:  # Rate limit exceeded
                reset_time = int(response.headers.get("x-rate-limit-reset", time.time()))
                wait_time = max(reset_time - time.time(), 0)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            elif response.status_code == 400:
                print(f"Bad request for {query} on {start_time.date()}: {err}")
                return None
            else:
                print(f"HTTP error occurred: {err}")
                break
        except Exception as err:
            print(f"Other error occurred: {err}")
            break
    
    print(f"Failed to fetch tweet count for '{query}' after {max_retries} retries.")
    return None

def save_to_csv(filename, data):
    """
    Save collected data to a CSV file.
    
    Args:
        filename (str): Name of the CSV file.
        data (list): List of data rows to be saved.
    """
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header if the file does not exist
        if not file_exists:
            csvwriter.writerow(['Query', 'Date', 'Tweet Count'])
        
        # Write data rows
        csvwriter.writerows(data)

if __name__ == "__main__":
    # Load queries from CSV file
    handles_file = "twitter/game_list.csv.csv"
    queries = get_handles_from_csv(handles_file)

    # Define the date range
    start_date = datetime(2024, 11, 10)
    end_date = datetime(2024, 11, 11)
    csv_filename = f"Data_pull_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.csv"

    # Collect tweet count data
    all_data = []
    for query in queries:
        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            tweet_count = get_tweet_count(query, current_date, next_date)
            
            if tweet_count is not None:
                all_data.append([query, current_date.date(), tweet_count])
                print(f"Number of tweets mentioning '{query}' on {current_date.date()}: {tweet_count}")
            else:
                print(f"Failed to fetch tweet count for '{query}' on {current_date.date()}.")
            
            current_date = next_date

    # Save data to CSV
    save_to_csv(csv_filename, all_data)
    print(f"Data saved to {csv_filename}")
