# Social Media Insights Dashboard

## Project Overview
This data engineering project focuses on providing insights and comparisons between a company product and its competitors on social media platforms—Twitter, Twitch, and YouTube. By leveraging social media data from these platforms, this project aims to visualize trends, engagement metrics, and overall social media presence to support business decision-making.

The project integrates several data sources, including the Twitter API, Google API V3, and Sullygnome (for Twitch data), to collect real-time and historical data. The collected data is processed and transformed using Python and Pandas, and presented in an interactive dashboard using Streamlit for easy client access and decision-making.

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

## Future Improvements
- **Real-Time Data Processing**: Implement real-time data collection and dashboard updates.
- **Sentiment Analysis**: Add sentiment analysis to track public opinion on the company product vs. competitors.
- **More Social Platforms**: Expand the project to include other social platforms like Instagram, Facebook, etc.

## License
This project is licensed under the MIT License - see the [LICENSE]([https://pages.github.com/](https://github.com/Cprogram06/smcp-dashboard/blob/main/LICENSE)) file for details.

## Acknowledgements
- **Twitter API**: For social media data collection.
- **Google API V3**: For gathering YouTube video data.
- **Sullygnome**: For Twitch streaming data.
- **Streamlit**: For creating the interactive dashboard.
