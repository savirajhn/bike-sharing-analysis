import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from sklearn.cluster import MeanShift
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import numpy as np

sns.set(style='darkgrid')

# Load data
df = pd.read_csv(r'D:\semester 6\sepeda\Dashboard\bike_sharing_data_cleaned.csv')

# Streamlit app
st.title('Bike Sharing Data Dashboard')

# Plotting
st.subheader('Visualizations')

# Line chart for monthly trend
st.write('### Monthly Trend of Bike Rentals')
st.write('This chart shows the total number of bike rentals for each month.')
monthly_trend = df.groupby('mnth_x')['cnt_x'].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_trend, x='mnth_x', y='cnt_x', ax=ax, marker='o', color='b')
max_value = monthly_trend['cnt_x'].max()
max_month = monthly_trend[monthly_trend['cnt_x'] == max_value]['mnth_x'].values[0]
ax.annotate(f'Max: {max_value}', xy=(max_month, max_value), xytext=(max_month, max_value + 500),
            arrowprops=dict(facecolor='black', shrink=0.05))
ax.set_title('Monthly Trend of Bike Rentals')
ax.set_xlabel('Month')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Bar chart for season effect
st.write('### Effect of Season on Bike Rentals')
st.write('This chart shows the total number of bike rentals for each season.')
season_effect = df.groupby('season_x')['cnt_x'].sum().reset_index()
season_effect['season_x'] = season_effect['season_x'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
fig, ax = plt.subplots()
colors = sns.color_palette("viridis", len(season_effect))
sns.barplot(data=season_effect, x='season_x', y='cnt_x', ax=ax, palette=colors)
max_value = season_effect['cnt_x'].max()
max_season = season_effect[season_effect['cnt_x'] == max_value]['season_x'].values[0]
ax.annotate(f'Max: {max_value}', xy=(max_season, max_value), xytext=(max_season, max_value + 5000),
            arrowprops=dict(facecolor='black', shrink=0.05))
ax.set_title('Effect of Season on Bike Rentals')
ax.set_xlabel('Season')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Pie chart for user profile
st.write('### User Profile')
st.write('This chart shows the proportion of casual and registered users.')
user_profile = df[['casual_x', 'registered_x']].sum().reset_index()
user_profile.columns = ['User Type', 'Count']
fig, ax = plt.subplots()
colors = sns.color_palette("pastel")
ax.pie(user_profile['Count'], labels=user_profile['User Type'], autopct='%1.1f%%', startangle=90, colors=colors)
ax.set_title('User Profile: Casual vs Registered')
st.pyplot(fig)

# Bar chart for holiday effect
st.write('### Effect of Holidays on Bike Rentals')
st.write('This chart shows the average number of bike rentals on holidays and non-holidays.')
holiday_effect = df.groupby('holiday_x')['cnt_x'].mean().reset_index()
holiday_effect['holiday_x'] = holiday_effect['holiday_x'].map({0: 'Non-Holiday', 1: 'Holiday'})
fig, ax = plt.subplots()
colors = sns.color_palette("muted")
sns.barplot(data=holiday_effect, x='holiday_x', y='cnt_x', ax=ax, palette=colors)
max_value = holiday_effect['cnt_x'].max()
max_holiday = holiday_effect[holiday_effect['cnt_x'] == max_value]['holiday_x'].values[0]
ax.annotate(f'Max: {max_value:.2f}', xy=(max_holiday, max_value), xytext=(max_holiday, max_value + 50),
            arrowprops=dict(facecolor='black', shrink=0.05))
ax.set_title('Effect of Holidays on Bike Rentals')
ax.set_xlabel('Day Type')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

# Mean Shift Clustering
st.write('### Mean Shift Clustering Analysis')
st.write('This analysis clusters the data based on environmental variables like temperature and windspeed.')

# Select relevant features for clustering
features = ['temp_x', 'windspeed_x', 'cnt_x']
X = df[features]

# Standardize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize and fit Mean Shift model
clustering = MeanShift(bandwidth=0.8)  # Adjust bandwidth if needed
clustering.fit(X_scaled)

# Get cluster labels
labels = clustering.labels_
df['cluster_meanshift'] = labels

# Visualize clustering results with legend
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(df['temp_x'], df['cnt_x'], c=df['cluster_meanshift'], cmap='viridis')

# Get unique cluster labels
unique_labels = np.unique(df['cluster_meanshift'])

# Create handles and labels for legend
handles, _ = scatter.legend_elements(prop="colors")
legend_labels = [f'Cluster {label}' for label in unique_labels]

# Add legend to plot
ax.legend(handles, legend_labels, title="Clusters", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_title('Mean Shift Clustering for Bike Rental Patterns')
ax.set_xlabel('Temperature (temp_x)')
ax.set_ylabel('Number of Rentals (cnt_x)')
st.pyplot(fig)