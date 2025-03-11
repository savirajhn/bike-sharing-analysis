import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import numpy as np

# Set Seaborn style
sns.set(style='darkgrid')

# Load cleaned data
df = pd.read_csv('bike_sharing_data_cleaned.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

# Sidebar filters
st.sidebar.header('Explore Data by Season and Weather')

# Season filter
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
selected_season = st.sidebar.selectbox('Select Season', 
    ['All'] + list(season_map.values()))

# Weather filter  
weather_map = {
    1: 'Clear', 
    2: 'Mist/Cloudy', 
    3: 'Light Rain/Snow', 
    4: 'Heavy Rain/Snow'
}
selected_weather = st.sidebar.selectbox('Select Weather Condition',
    ['All'] + list(weather_map.values()))

# Create filtered dataframe based on selections
if selected_season != 'All' or selected_weather != 'All':
    st.sidebar.subheader('Filtered Data Analysis')
    
    filtered_df = df.copy()
    if selected_season != 'All':
        season_id = [k for k, v in season_map.items() if v == selected_season][0]
        filtered_df = filtered_df[filtered_df['season_x'] == season_id]
    if selected_weather != 'All':
        weather_id = [k for k, v in weather_map.items() if v == selected_weather][0]
        filtered_df = filtered_df[filtered_df['weathersit_x'] == weather_id]
    
    # Display metrics with more precise formatting
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Average Rentals", f"{filtered_df['cnt_x'].mean():.1f}")
    with col2:
        st.metric("Total Rentals", f"{filtered_df['cnt_x'].sum():,.0f}")

    # Add hourly pattern plot in sidebar
    st.sidebar.write('Hourly Rental Pattern')
    hourly_avg = filtered_df.groupby('hr')['cnt_x'].mean().reset_index()
    fig_sidebar = plt.figure(figsize=(8, 3))
    sns.lineplot(data=hourly_avg, x='hr', y='cnt_x')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Rentals')
    st.sidebar.pyplot(fig_sidebar)

# Main dashboard
st.title('Bike Sharing Data Analysis Dashboard')

# Monthly trend visualization
st.write('### Monthly Trend of Bike Rentals')
monthly_trend = df.groupby('mnth_x')['cnt_x'].sum().reset_index()
fig = plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_trend, x='mnth_x', y='cnt_x', marker='o')
plt.title('Monthly Trend of Bike Rentals', pad=20)
plt.xlabel('Month')
plt.ylabel('Total Rentals')

# Add value labels
max_value = monthly_trend['cnt_x'].max()
max_month = monthly_trend[monthly_trend['cnt_x'] == max_value]['mnth_x'].values[0]
plt.annotate(f'Max: {max_value:,.0f}', 
            xy=(max_month, max_value),
            xytext=(max_month, max_value + max_value*0.05),
            ha='center',
            arrowprops=dict(facecolor='black', shrink=0.05))
st.pyplot(fig)

# Seasonal analysis
st.write('### Effect of Season on Bike Rentals')
season_effect = df.groupby('season_x')['cnt_x'].sum().reset_index()
season_effect['season_x'] = season_effect['season_x'].map(season_map)
fig = plt.figure(figsize=(10, 6))
sns.barplot(data=season_effect, x='season_x', y='cnt_x', palette='viridis')
plt.title('Seasonal Distribution of Bike Rentals', pad=20)
plt.xlabel('Season')
plt.ylabel('Total Rentals')

# Add value labels
for i, v in enumerate(season_effect['cnt_x']):
    plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom')
st.pyplot(fig)

# User profile analysis
st.write('### User Profile Distribution')
user_profile = pd.DataFrame({
    'User Type': ['Casual', 'Registered'],
    'Count': [df['casual_x'].sum(), df['registered_x'].sum()]
})
fig = plt.figure(figsize=(8, 8))
plt.pie(user_profile['Count'], 
        labels=user_profile['User Type'],
        autopct='%1.1f%%',
        colors=sns.color_palette('Set3'))
plt.title('Distribution of Casual vs Registered Users', pad=20)
st.pyplot(fig)

# Time-based analysis 
st.header('Time-Based Usage Patterns')
st.write('Analysis of rental patterns throughout the day')

def group_by_time(hour):
    if 6 <= hour < 12:
        return 'Pagi'
    elif 12 <= hour < 18:
        return 'Siang'
    elif 18 <= hour < 24:
        return 'Sore'
    else:  # 0-5
        return 'Malam'

# Create time groups
df['time_group'] = df['hr'].apply(group_by_time)

# Calculate rentals by time group with proper ordering
custom_order = ['Malam', 'Pagi', 'Siang', 'Sore']
time_group_rentals = df.groupby('time_group')['cnt_x'].sum().reset_index()
time_group_rentals['time_group'] = pd.Categorical(
    time_group_rentals['time_group'],
    categories=custom_order,
    ordered=True
)
time_group_rentals = time_group_rentals.sort_values('time_group')

# Create visualization
fig = plt.figure(figsize=(10, 6))
sns.barplot(
    data=time_group_rentals,
    x='time_group',
    y='cnt_x',
    palette='viridis'
)
plt.title('Jumlah Penyewaan Sepeda per Kelompok Waktu', pad=20)
plt.xlabel('Kelompok Waktu')
plt.ylabel('Jumlah Penyewaan')

# Add formatted value labels
for i, v in enumerate(time_group_rentals['cnt_x']):
    plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom')

st.pyplot(fig)

# Display detailed numbers with formatting
st.write('#### Detailed Rental Numbers by Time Period')
time_group_rentals['cnt_x'] = time_group_rentals['cnt_x'].map('{:,.0f}'.format)
st.dataframe(time_group_rentals)

# Add download button for filtered data
if selected_season != 'All' or selected_weather != 'All':
    st.sidebar.header('Download Filtered Data')
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f"bike_rentals_{selected_season}_{selected_weather}.csv",
        mime="text/csv",
    )