"""Third Party Imports."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Constants
DEFAULT_CSV_PATHS = {
    "main_data": 'csvs/SOV - SoV_YT.csv',
    "axie_vs_field": 'csvs/SOV - YT_axie_vs_field.csv',
    "ronin_games": 'csvs/SOV - YT_ronin_games.csv',
    "ronin_vs_field": 'csvs/SOV - YT_RVF.csv'
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
    for count_type in ['View Count', 'Like Count', 'Comment Count']:
        fig = px.line(data, x='Date', y=count_type, title=f'{count_type} Over Time')
        fig.update_layout(xaxis_title='Date', yaxis_title=count_type)
        st.plotly_chart(fig)

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
    st.title("YouTube Share of Voice Analysis")

    # Load and display Axie Infinity trend data
    st.subheader("Axie Infinity Trend")
    main_data = read_data(DEFAULT_CSV_PATHS["main_data"])
    generate_line_chart(main_data, "Axie Infinity Trend Over Time")

    # Define metrics options for charts
    metrics_options = ['View Count', 'Like Count', 'Comment Count']
    
    # Display Axie Infinity vs Field charts
    st.subheader("Axie Infinity vs Field")
    axie_vs_field_data = read_data(DEFAULT_CSV_PATHS["axie_vs_field"])
    generate_pie_chart(axie_vs_field_data, metrics_options, 'Select AVF Metrics', 'Axie Infinity VS Field')
    generate_bar_chart(axie_vs_field_data, metrics_options, 'Select AVF Metrics', 'Axie Infinity VS Field Bar Chart')

    # Display Ronin Games vs Each Other charts
    st.subheader("Ronin Games vs Each Other")
    ronin_games_data = read_data(DEFAULT_CSV_PATHS["ronin_games"])
    generate_pie_chart(ronin_games_data, metrics_options, 'Select Ronin Games Metrics', 'Ronin Games VS Each Other')
    generate_bar_chart(ronin_games_data, metrics_options, 'Select Ronin Games Metrics', 'Ronin Games VS Each Other Bar Chart')

    # Display Ronin Games vs Field charts
    st.subheader("Ronin Games vs Field")
    ronin_vs_field_data = read_data(DEFAULT_CSV_PATHS["ronin_vs_field"])
    generate_pie_chart(ronin_vs_field_data, metrics_options, 'Select RVF Metrics', 'Ronin Games VS Field')
    generate_bar_chart(ronin_vs_field_data, metrics_options, 'Select RVF Metrics', 'Ronin Games VS Field Bar Chart')

# Run main dashboard function
if __name__ == '__main__':
    display_dashboard()
