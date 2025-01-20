"""Third Party Imports."""
import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Date range for data extraction (past 7 days)
now = datetime.utcnow()
days_ago = now - timedelta(days=7)
days_ago_str = days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_video_data(search_query, max_results=50, max_retries=3, retry_delay=5):
    """
    Extract video data from the YouTube API for a given search query.
    
    Args:
        search_query (str): The game name or search term.
        max_results (int): Maximum number of results per page.
        max_retries (int): Maximum retries on request failure.
        retry_delay (int): Delay between retries in seconds.
        
    Returns:
        list: Raw video data (ID and details for transformation).
    """
    video_ids = []
    next_page_token = None

    while True:
        search_url = (
            f"https://www.googleapis.com/youtube/v3/search?part=snippet"
            f"&q=allintitle%3A{search_query}&type=video&maxResults={max_results}"
            f"&key={API_KEY}&publishedAfter={days_ago_str}"
        )
        if next_page_token:
            search_url += f"&pageToken={next_page_token}"

        for _ in range(max_retries):
            response = requests.get(search_url)
            if response.status_code == 200:
                break
            print(f"Error {response.status_code}: Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed to retrieve data for '{search_query}' after {max_retries} retries.")
            return []

        video_ids.extend(item["id"]["videoId"] for item in response.json().get("items", []))
        next_page_token = response.json().get("nextPageToken")
        if not next_page_token:
            break

    return video_ids


def transform_video_data(video_ids, max_retries=3, retry_delay=5):
    video_data = []
    if not video_ids:
        print("No video IDs found.")
        return video_data

    batch_size = 50
    for i in range(0, len(video_ids), batch_size):
        batch = video_ids[i:i + batch_size]
        stats_url = (
            f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics"
            f"&id={','.join(batch)}&key={API_KEY}"
        )
        
        for _ in range(max_retries):
            stats_response = requests.get(stats_url)
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                for item in stats_data.get("items", []):
                    video_id = item["id"]
                    snippet = item["snippet"]
                    stats = item.get("statistics", {})
                    video_data.append([
                        video_id,
                        snippet["publishedAt"],
                        snippet["title"],
                        stats.get("viewCount", 0),
                        stats.get("likeCount", 0),
                        stats.get("commentCount", 0),
                        snippet.get("channelTitle", ""),
                        stats.get("subscriberCount", 0)
                    ])
                break
            else:
                print(f"Error {stats_response.status_code}: {stats_response.text}")
                time.sleep(retry_delay)
        else:
            print(f"Failed to retrieve stats for batch: {batch}")
            continue

    return video_data



def extract_channel_data(channel_id, max_retries=3, retry_delay=5):
    """
    Extracts channel data (name and subscriber count) from YouTube API.
    
    Args:
        channel_id (str): Channel ID.
        max_retries (int): Maximum retries for API requests.
        retry_delay (int): Delay between retries.
        
    Returns:
        dict: Dictionary containing channel title and subscriber count.
    """
    channel_url = (
        f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics"
        f"&id={channel_id}&key={API_KEY}"
    )

    for _ in range(max_retries):
        channel_response = requests.get(channel_url)
        if channel_response.status_code == 200:
            break
        print(f"Error {channel_response.status_code}: Retrying channel data in {retry_delay} seconds...")
        time.sleep(retry_delay)
    else:
        print(f"Failed to retrieve channel data after {max_retries} retries.")
        return {}

    channel_info = channel_response.json().get("items", [{}])[0]
    return {
        "title": channel_info.get("snippet", {}).get("title"),
        "subscriberCount": channel_info.get("statistics", {}).get("subscriberCount")
    }


def load_to_csv(game, data):
    """
    Load transformed data to a CSV file.
    
    Args:
        game (str): The name of the game or search term.
        data (list): The data to load into CSV.
    """
    df = pd.DataFrame(data, columns=[
        "Video ID",
        "Published Date",
        "Title",
        "View Count",
        "Like Count",
        "Comment Count",
        "Channel Title",
        "Subscriber Count",
    ])
    game_name = game.replace(" ", "_")
    output_file = f"{game_name}.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    # Read games from CSV file
    game_df = pd.read_csv("youtube\game_list.csv")
    game_list = game_df['game'].tolist()

    for game in game_list:
        print(f"Extracting videos for '{game}'")
        video_ids = extract_video_data(game)
        if video_ids:
            print(f"Transforming data for '{game}'")
            video_data = transform_video_data(video_ids)
            print(f"Loading data for '{game}' into CSV")
            load_to_csv(game, video_data)