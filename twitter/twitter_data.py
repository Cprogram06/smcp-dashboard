"""Third-party imports."""
import tweepy
import configparser
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

def authenticate_twitter(bearer_token):
    """
    Authenticate with Twitter using a bearer token.
    
    Args:
        bearer_token (str): Twitter API bearer token.
    
    Returns:
        tweepy.Client: Authenticated Twitter API client.
    """
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

def load_game_list(file_path):
    """
    Load a list of games from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing the game list.
    
    Returns:
        list: List of games from the CSV file.
    """
    game_df = pd.read_csv(file_path)
    return game_df['game'].tolist()

def search_tweets(client, game, limit=10000, max_retries=3, retry_delay=5):
    """
    Search tweets about a specific game and save results to a CSV file.
    
    Args:
        client (tweepy.Client): Authenticated Twitter API client.
        game (str): The game name or hashtag to search for.
        limit (int): Maximum number of tweets to retrieve.
        max_retries (int): Maximum number of retries for request failures.
        retry_delay (int): Delay between retries in seconds.
    
    Returns:
        pd.DataFrame: DataFrame containing retrieved tweet information.
    """
    columns = ["Time", "User", "Tweet", "Coordinates", "User Data", "Retweet Count", "Likes Count", "Language"]
    data = []

    retries_left = max_retries
    while retries_left > 0:
        try:
            tweets = tweepy.Paginator(
                client.search_recent_tweets, query=f"#{game}", max_results=100,
                tweet_fields=["created_at", "text", "lang", "public_metrics", "geo"], 
                user_fields=["username"]
            ).flatten(limit=limit)
            break  # Exit the loop if tweets are retrieved successfully
        except tweepy.TweepyException as e:
            print(f"An error occurred: {str(e)}. Retrying in {retry_delay} seconds...")
            retries_left -= 1
            time.sleep(retry_delay)
    else:
        print(f"Failed to retrieve tweets for '{game}' after {max_retries} retries.")
        return pd.DataFrame(columns=columns)

    for tweet in tweets:
        likes_count = tweet.public_metrics.get("like_count", 0)
        retweet_count = tweet.public_metrics.get("retweet_count", 0)
        
        data.append([
            tweet.created_at,
            tweet.author_id,  # User ID as user details are limited with bearer token
            tweet.text,
            tweet.geo,
            None,  # Placeholder for unavailable user data
            retweet_count,
            likes_count,
            tweet.lang
        ])

    df = pd.DataFrame(data, columns=columns)
    output_file = f"{game}_Tweets.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    return df

if __name__ == "__main__":
    # Authenticate Twitter API using bearer token
    client = authenticate_twitter(BEARER_TOKEN)

    # Load game list from CSV
    games_file = 'twitter/game_list.csv'
    game_list = load_game_list(games_file)

    # Loop through each game and retrieve tweets
    for game in game_list:
        print(f"Searching tweets for '{game}'")
        search_tweets(client, game)
