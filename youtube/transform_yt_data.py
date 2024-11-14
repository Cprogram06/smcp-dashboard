import os
import glob
import pandas as pd

def load_csv_files():
    """
    Load all CSV files from the current directory, add a 'Game' column for each,
    and return a concatenated DataFrame.
    
    Returns:
        pd.DataFrame: Concatenated DataFrame of all CSV files with 'Game' column.
    """
    csv_files = glob.glob('*.csv')
    dataframes = []

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, index_col=0)
            # Use the file name to set the 'Game' column
            df["Game"] = os.path.basename(csv_file).split(' ')[0]
            dataframes.append(df)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
            continue

    return pd.concat(dataframes, ignore_index=True)


def preprocess_dataframe(df):
    """
    Preprocess the DataFrame by formatting the 'Published Date' as a 'Time' column 
    in datetime format and filter data after a specific date.
    
    Args:
        df (pd.DataFrame): The original DataFrame with raw data.
    
    Returns:
        pd.DataFrame: Filtered DataFrame with 'Time' column formatted as datetime.
    """
    df["Time"] = pd.to_datetime(df["Published Date"]).dt.strftime("%m-%d-%y")
    df["Time"] = pd.to_datetime(df["Time"])
    # Filter to include only data after '02-06-23'
    return df[df["Time"] > '02-06-23']


def save_filtered_game_data(df, game_name, file_path):
    """
    Save filtered data for a specific game to a CSV file.
    
    Args:
        df (pd.DataFrame): The DataFrame with filtered data.
        game_name (str): The name of the game to filter on.
        file_path (str): Path where the CSV file will be saved.
    """
    df[df["Game"] == game_name].to_csv(file_path)


def aggregate_metrics(df):
    """
    Aggregate metrics by 'Game' and calculate the sum for each relevant column.
    
    Args:
        df (pd.DataFrame): The filtered DataFrame with social media data.
    
    Returns:
        pd.DataFrame: Aggregated DataFrame with summed metrics by 'Game'.
    """
    return df.groupby("Game").agg({
        "View Count": "sum", 
        "Like Count": "sum", 
        "Comment Count": "sum", 
        "Subscriber Count": "sum"
    })


def calculate_share_of_voice(df):
    """
    Calculate the Share of Voice (SoV) for each metric in the DataFrame.
    
    Args:
        df (pd.DataFrame): Aggregated DataFrame with metrics.
    
    Returns:
        pd.DataFrame: DataFrame with additional SoV columns for each metric.
    """
    df['SoV_Views'] = df['View Count'] / df['View Count'].sum() * 100
    df['SoV_Likes'] = df['Like Count'] / df['Like Count'].sum() * 100
    df['SoV_Comments'] = df['Comment Count'] / df['Comment Count'].sum() * 100
    df['SoV_Subscriber'] = df['Subscriber Count'] / df['Subscriber Count'].sum() * 100
    return df.apply(pd.to_numeric, errors='coerce')


def export_top_n_with_other(df, metric, n=9):
    """
    Export the top N values for a given SoV metric, along with an 'Other' category
    representing the sum of the remaining values, to a CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame with SoV metrics.
        metric (str): The metric to rank by (e.g., 'SoV_Views').
        n (int): Number of top entries to include.
    """
    top_n = df.nlargest(n, metric)
    other_sum = df.loc[~df.index.isin(top_n.index), metric].sum()
    top_n.loc['Other'] = other_sum
    top_n.to_csv(f'./{metric}.csv')


def main():
    # Load and preprocess data
    raw_data = load_csv_files()
    filtered_data = preprocess_dataframe(raw_data)
    
    # Save specific game data to CSV
    save_filtered_game_data(filtered_data, "SoRare_youtube_stats", "../monkahmm.csv")
    
    # Aggregate metrics and calculate Share of Voice (SoV)
    aggregated_data = aggregate_metrics(filtered_data)
    sov_data = calculate_share_of_voice(aggregated_data)
    
    # Export top N entries with 'Other' for each SoV metric
    for metric in ['SoV_Views', 'SoV_Likes', 'SoV_Comments', 'SoV_Subscriber']:
        export_top_n_with_other(sov_data, metric)

if __name__ == "__main__":
    main()
