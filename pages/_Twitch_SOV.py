"""Third Party Imports."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Constants
DEFAULT_CSV_PATHS = {
    "axie_trend": 'csvs/SOV - Twitch_SOV.csv',
    "7_days_sov": 'csvs/SOV - Twitch_axie_vs_field.csv',
    "90_days_sov": 'csvs/SOV - Twitch_90_day.csv'
}

# Data Loading Functions
def read_data(filename):
    """Read data from CSV and ensure 'Date' column is in datetime format if present."""
    df = pd.read_csv(filename)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

# Chart Generation Functions
def generate_line_chart(data, title="Trend Over Time"):
    """Generate line charts for selected count types."""
    st.dataframe(data)
    for count_type in ['Watch time (mins)', 'Stream time (mins)', 'Peak viewers']:
        fig = px.line(data, x='Date', y=count_type, title=f'{count_type} Over Time')
        fig.update_layout(xaxis_title='Date', yaxis_title=count_type)
        st.plotly_chart(fig)

def generate_pie_chart(data, options, widget_id, chart_title):
    """Generate pie chart for selected metrics."""
    selected_options = st.multiselect(widget_id, options, default=options, key=f"pie_chart_{widget_id}")
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
    selected_options = st.multiselect(widget_id, options, default=options, key=f"bar_chart_{widget_id}")
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
    st.title("Twitch Share of Voice Analysis")

    # Load and display Axie Infinity trend data
    st.subheader("Axie Infinity Trend")
    trend_data = read_data(DEFAULT_CSV_PATHS["axie_trend"])
    generate_line_chart(trend_data, "Axie Infinity Trend Over Time")

    # Define metrics options and titles for pie and bar charts
    metrics_options = ['Watch time (mins)', 'Stream time (mins)', 'Average viewers']
    
    # Display 7 Days Share of Voice (SOV) charts
    st.subheader("7 Days Share of Voice (SOV)")
    sov_7d_data = read_data(DEFAULT_CSV_PATHS["7_days_sov"])
    generate_pie_chart(sov_7d_data, metrics_options, 'Select 7 Day Metrics', '7 Days SOV')
    generate_bar_chart(sov_7d_data, metrics_options, 'Select 7 Day Metrics', '7 Days SOV Bar Chart')

    # Display 90 Days Share of Voice (SOV) charts
    st.subheader("90 Days Share of Voice (SOV)")
    sov_90d_data = read_data(DEFAULT_CSV_PATHS["90_days_sov"])
    generate_pie_chart(sov_90d_data, metrics_options, 'Select 90 Day Metrics', '90 Days SOV')
    generate_bar_chart(sov_90d_data, metrics_options, 'Select 90 Day Metrics', '90 Days SOV Bar Chart')

# Run main dashboard function
if __name__ == '__main__':
    display_dashboard()
