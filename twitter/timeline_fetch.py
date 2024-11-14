import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve bearer token from environment variables
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Check if the token is loaded
if BEARER_TOKEN is None:
    raise ValueError("Bearer token not found. Please set it in the .env file.")

# Set up headers for the request
headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

def get_user_id(username):
    """Retrieve Twitter user ID by username"""
    url = f'https://api.twitter.com/2/users/by/username/{username}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors
    user_data = response.json()
    return user_data['data']['id']

def fetch_tweets(user_id, start_date_str, end_date_str):
    """Fetch tweets within a given date range"""
    # Convert date strings to ISO 8601 format
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').isoformat() + 'Z'
    end_date = (datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)).isoformat() + 'Z'

    # Twitter API v2 endpoint for user tweets
    url = f'https://api.twitter.com/2/users/{user_id}/tweets'
    params = {
        'start_time': start_date,
        'end_time': end_date,
        'tweet.fields': 'id,created_at,text,public_metrics',  # Fields to fetch
        'max_results': 100  # Number of tweets to fetch per request (adjust as needed)
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Check for HTTP errors

    tweets = response.json().get('data', [])
    
    # Initialize list to store tweet data
    data = []

    for tweet in tweets:
        created_at = tweet['created_at']
        public_metrics = tweet['public_metrics']
        data.append({
            'tweet_id': tweet['id'],
            'date': created_at.split('T')[0],  # Extract date in YYYY-MM-DD format
            'content': tweet['text'],
            'likes': public_metrics['like_count'],
            'retweets': public_metrics['retweet_count']
        })

    return data

def main(username, start_date_str, end_date_str):
    """Main function to fetch and save tweets for given username and date range"""
    # Get the user ID from the username
    user_id = get_user_id(username)

    # Fetch tweet data
    tweet_data = fetch_tweets(user_id, start_date_str, end_date_str)

    # Convert the data to a DataFrame
    df = pd.DataFrame(tweet_data)

    # Save the DataFrame to a CSV file
    csv_filename = f'{username}_{start_date_str}_to_{end_date_str}.csv'
    df.to_csv(csv_filename, index=False)
    print(f'Saved tweet data to {csv_filename}')

    # Aggregate data by date
    aggregated_data = df.groupby('date').agg(
        Tweet_Count=('tweet_id', 'count'),
        Likes=('likes', 'sum'),
        Retweets=('retweets', 'sum')
    ).reset_index()

    # Save the aggregated data to a separate CSV file
    aggregated_csv_filename = f'{username}_{start_date_str}_to_{end_date_str}_aggregated.csv'
    aggregated_data.to_csv(aggregated_csv_filename, index=False)
    print(f'Saved aggregated tweet data to {aggregated_csv_filename}')

    return df  # Return dataframe for further analysis or visualization

if __name__ == "__main__":
    # Load the list of games from gamelist.csv
    games_df = pd.read_csv('gamelist.csv')

    # Loop through each game in the gamelist
    for index, row in games_df.iterrows():
        game_name = row['Game Name']
        print(f'Fetching tweets for {game_name}')

        # Replace with the desired start and end dates for each game
        start_date_str = '2024-09-04'
        end_date_str = '2024-09-09'
        
        # Run the main function for each game
        main(game_name, start_date_str, end_date_str)
