"""Third Party Imports."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Constants for file paths
CSV_PATHS = {
    "main_data": 'csvs/SOV - SoV_twitter.csv',
    "axie_vs_field": 'csvs/SOV - Twitter_axie_vs_field.csv',
    "ronin_vs_field": 'csvs/SOV - Ronin_vs_field.csv',
    "ronin_games": 'csvs/SOV - Twitter_ronin_games.csv',
    "ronin_games_vs_field": 'csvs/SOV - Twitter_RVF.csv'
}

# Data Loading Functions
def read_data(filename):
    """Read data from CSV and ensure 'Date' column is in datetime format if present."""
    df = pd.read_csv(filename)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

# Chart Generation Functions
def generate_line_chart(data, metric_columns):
    """Generate a line chart for selected metrics over time."""
    chart_data = data.set_index('Date')  # Set 'Date' column as index

    options = st.multiselect('Select Counts to Display', metric_columns, default=metric_columns)
    selected_columns = [option for option in options if option in chart_data.columns]

    if selected_columns:
        fig = go.Figure()
        for column in selected_columns:
            fig.add_trace(go.Scatter(x=chart_data.index, y=chart_data[column], mode='lines', name=column))
        fig.update_layout(
            title="Twitter Share of Voice",
            xaxis_title="Date",
            yaxis_title="Count",
            xaxis=dict(tickformat='%m-%d')  # Format x-axis ticks to display month-day
        )
        st.plotly_chart(fig)
    else:
        st.write("Please select at least one count to display.")

def generate_pie_chart(data, options, widget_id, chart_title):
    """Generate pie chart for selected metrics."""
    selected_options = st.multiselect(widget_id, options, default=options)
    fig = go.Figure()

    for option in selected_options:
        fig.add_trace(go.Pie(
            labels=data['Game'], values=data[option],
            name=option, textinfo='label+percent', textposition='inside'
        ))
    fig.update_layout(title=chart_title)
    st.plotly_chart(fig)

def generate_bar_chart(data, options, widget_id, chart_title="Bar Chart of Metrics"):
    """Generate a stacked bar chart of selected metrics."""
    selected_options = st.multiselect(widget_id, options, default=options)
    grouped_data = data.groupby('Game')[selected_options].sum().reset_index()
    grouped_data['Total'] = grouped_data[selected_options].sum(axis=1)
    sorted_data = grouped_data.sort_values(by='Total', ascending=True)
    
    fig = go.Figure()
    for option in selected_options:
        fig.add_trace(go.Bar(
            y=sorted_data['Game'], x=sorted_data[option], orientation='h', name=option
        ))
    fig.update_layout(
        title=chart_title,
        xaxis_title='Count',
        yaxis_title='Game',
        barmode='stack'
    )
    st.plotly_chart(fig, use_container_width=True)

# Main Dashboard UI
def display_dashboard():
    """Displays the main dashboard with interactive visualizations."""
    st.title("Twitter Share of Voice Analysis")

    # Define metrics options for charts
    metrics_options = ['Tweet', 'Retweet Count', 'Likes Count']

    # Load and display main trend data for Axie Infinity
    st.subheader("Axie Infinity Trend")
    main_data = read_data(CSV_PATHS["main_data"])
    generate_line_chart(main_data, metrics_options)

    # Display Axie Infinity vs Field charts
    display_comparison_charts("Axie Infinity vs Field", CSV_PATHS["axie_vs_field"], metrics_options)

    # Display Ronin Network vs Other Chains charts
    display_comparison_charts("Ronin Network vs Other Chains", CSV_PATHS["ronin_vs_field"], metrics_options)

    # Display Ronin Games vs Each Other charts
    display_comparison_charts("Ronin Games vs Each Other", CSV_PATHS["ronin_games"], metrics_options)

    # Display Ronin Games vs Field charts
    display_comparison_charts("Ronin Games vs Field", CSV_PATHS["ronin_games_vs_field"], metrics_options)

def display_comparison_charts(title, data_path, metrics_options):
    """Helper function to display pie and bar charts for comparison data."""
    st.subheader(title)
    comparison_data = read_data(data_path)
    generate_pie_chart(comparison_data, metrics_options, f'Select {title} metrics', f'{title} Pie Chart')
    generate_bar_chart(comparison_data, metrics_options, f'Select {title} metrics', f'{title} Bar Chart')

# Run main dashboard function
if __name__ == '__main__':
    display_dashboard()
