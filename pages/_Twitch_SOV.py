"""Third party imports."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read data from CSV
def read_data(filename):
    """Read data from csv."""
    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime
    return df

def generate_line_chart(data, metrics1="", metrics2="", metrics3=""):
    """Generate Line charts."""
    chart_data = data.copy()
    chart_data['Date'] = pd.to_datetime(chart_data['Date'])
    chart_data['Date'] = chart_data['Date'].dt.strftime('%m-%d')

    # Plot the line charts
    if metrics1 in chart_data.columns:
        st.line_chart(data=chart_data,x='Date',y=metrics1)

    if metrics2 in chart_data.columns:
        st.line_chart(data=chart_data,x='Date',y=metrics2)

    if metrics3 in chart_data.columns:
        st.line_chart(data=chart_data,x='Date',y=metrics3)



def generate_pie_chart(data, widget_id, chart_title):
    """Generate Pie Chart."""
    options = ['Watch time (mins)', 'Stream time (mins)', 'Average viewers']
    selected_options = st.multiselect(widget_id, options, default=options)

    fig = go.Figure()

    for option in selected_options:
        fig.add_trace(go.Pie(labels=data['Game'], values=data[option], name=option, textinfo='label+percent', textposition='inside'))

    fig.update_layout(title=chart_title)

    st.plotly_chart(fig)

def generate_bar_chart(data,widget_id):
    """Generate Bar Chart."""
    options = ['Watch time (mins)', 'Stream time (mins)', 'Average viewers']
    selected_options = st.multiselect(widget_id, options, default=options)

    counts = data.groupby('Game')[selected_options].sum().reset_index()
    counts['Total'] = counts[selected_options].sum(axis=1)  # Calculate the sum of selected options as the 'Total' column
    counts_sorted = counts.sort_values(by='Total', ascending=True)  # Sort by the 'Total' column

    labels = counts_sorted['Game']
    values = counts_sorted[selected_options]

    fig = go.Figure()
    for option in selected_options:
        fig.add_trace(go.Bar(y=labels, x=values[option], orientation='h', name=option))

    fig.update_layout(title='Count of Watch time (mins), Stream time (mins), Average viewers',
                      xaxis_title='Count',
                      yaxis_title='Game',
                      barmode='stack')

    st.plotly_chart(fig, use_container_width=True)

# Main function
def main():
    """Initialize the program."""
    st.title("Twitch Share of Voice")
    
    # Read CSV file
    filename = 'csvs/SOV - Twitch_SOV.csv'
    data = read_data(filename)

    # Generate line chart
    st.subheader("Axie Infinity Trend")
    generate_line_chart(data,'Watch time (mins)', 'Stream time (mins)', 'Average viewers')

    piedf_sov = pd.read_csv('csvs/SOV - Twitch_axie_vs_field.csv')

    generate_pie_chart(piedf_sov,'Select 7 day Metrics','7 Days SOV')
    generate_bar_chart(piedf_sov,' ')

    pie90_df = pd.read_csv('csvs/SOV - Twitch_90_day.csv')

    generate_pie_chart(pie90_df,'Select 90 days Metrics','90 Days SOV')
    generate_bar_chart(pie90_df,'  ')

if __name__ == '__main__':
    main()
