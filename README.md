# Social Media Insights Dashboard

## Project Overview
This data engineering project focuses on providing insights and comparisons between a company product and its competitors on social media platforms—Twitter, Twitch, and YouTube. By leveraging social media data from these platforms, this project aims to visualize trends, engagement metrics, and overall social media presence to support business decision-making.

The project integrates several data sources, including the Twitter API, Google API V3, and Sullygnome (for Twitch data), to collect real-time and historical data. The collected data is processed and transformed using Python and Pandas, and presented in an interactive dashboard using Streamlit for easy client access and decision-making.

You can interact with [the demo here](https://smcp-sov.streamlit.app)!

## Data Sources
- **Twitter**: Data is collected using the Twitter API to monitor engagement metrics, such as tweets, retweets, and likes for both the company product and its competitors.
- **Twitch**: The project pulls Twitch data via Sullygnome, an online service that provides data and statistics for Twitch streams.
- **YouTube**: Data for YouTube is gathered using the Google API V3, providing insights into video performance metrics, including views, likes, comments, and more.

## Key Features
- **Real-time Social Media Monitoring**: Collects and analyzes data from Twitter, Twitch, and YouTube.
- **Data Pipeline**: Uses Python and Pandas to clean, process, and transform raw social media data into actionable insights.
- **Data Visualization**: The processed data is displayed in interactive charts and graphs using Streamlit.
  - **Line Charts**: For tracking trends over time (e.g., number of tweets, likes, retweets).
  - **Pie Charts**: For visualizing proportions and comparisons between different metrics.
  - **Bar Charts**: For comparing metrics between the company product and its competitors.

## Technologies Used
- **Python**: For data collection, processing, and analysis.
- **Pandas**: For data manipulation and transformation.
- **Streamlit**: For building an interactive web dashboard.
- **Plotly**: For interactive data visualizations.
- **Twitter API**: To gather data about tweets, likes, and retweets.
- **Google API V3**: For gathering YouTube video data.
- **Sullygnome**: For obtaining Twitch statistics and data.

## Features Walkthrough

### Twitter Share of Voice
- **Line Chart**: Visualizes the trend of tweets, retweets, and likes over time for both the company product and its competitors.
- **Pie Chart**: Compares the share of tweets, retweets, and likes between different competitors.
- **Bar Chart**: Provides a stacked bar chart of tweets, retweets, and likes by game or competitor.

### Twitch Data Insights
- **View Count**, **Like Count**, and **Comment Count**: Track and visualize the growth and performance of streams over time.

### YouTube Data Insights
- **Views**, **Likes**, and **Comments**: Monitor the performance of videos, with comparisons between the company product's channel and competitors.

## Scripts
- **[get_tweet_count](twitter/get_tweet_count.py)**: Get the total tweet count of a handle on the game list based on the set data.
- **[timeline_fetch](twitter/timeline_fetch.py)**: Get the recent tweets data of a handle.
- **[twitter_data](twitter/twitter_data.py)**: Get all the data of a tweet mentioning a handle, including tweet count, likes count, retweet count, and reply count.
- **[youtube_data](youtube/youtube_data.py)**: Get the data of a video using the game search endpoint.
- **[transform_yt_data](youtube/transform_yt_data.py)**: Transform gathered youtube data for visualization use.

## Setup and Deployment on Streamlit Cloud

Follow these steps to deploy this project on Streamlit Cloud:

### Step 1: Push Your Project to GitHub
- If you haven’t already, push your project to a GitHub repository. This includes all the necessary project files like `Twitter_SOV.py`, `requirements.txt`, and the folder structure with your scripts.

### Step 2: Sign Up/Login to Streamlit Cloud
- Go to [Streamlit Cloud](https://share.streamlit.io) and sign up for a new account or log in to your existing account.

### Step 3: Connect Streamlit to GitHub
- Once you are logged into your Streamlit account, click on **New App**.
- Choose **GitHub** as your source and grant Streamlit access to your GitHub repositories.
- Select the repository that contains your project and click on it.

### Step 4: Configure the App
- Choose the branch (usually `main` or `master`) where your `Twitter_SOV.py` file is located.
- Ensure `Twitter_SOV.py` is the main file that runs the Streamlit app.
- Optionally, configure environment variables or settings (if needed).

### Step 5: Deploy the App
- Click on **Deploy** to build and deploy your app.
- Streamlit will automatically install the dependencies listed in your `requirements.txt` file, and the app will be up and running.

### Step 6: Access the Dashboard
- Once deployed, Streamlit will provide you with a unique URL to access your app. You can share this link with others or use it to embed the dashboard in your documentation.

### Troubleshooting:
- If there are issues with dependencies or missing packages, make sure that all required libraries are listed in `requirements.txt`.
- If there are errors related to the APIs (Twitter, YouTube, or Twitch), ensure you have the correct API keys and access tokens in place.

## Future Improvements
- **Real-Time Data Processing**: Implement real-time data collection and dashboard updates.
- **More Social Platforms**: Expand the project to include other social platforms like Instagram, Facebook, etc.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- **Twitter API**: For social media data collection.
- **Google API V3**: For gathering YouTube video data.
- **Sullygnome**: For Twitch streaming data.
- **Streamlit**: For creating the interactive dashboard.
