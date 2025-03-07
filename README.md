# Bike Sharing Data Dashboard

This project visualizes bike sharing data using Streamlit.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo-url.git
    cd your-repo-url
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```bash
    streamlit run dashboard1.py
    ```

## Data

The data is stored in `bike_sharing_data_cleaned.csv` and `hour.csv`. Make sure these files are in the same directory as `dashboard1.py`.

## Usage

The dashboard provides various visualizations and metrics for bike sharing data, including:

- **Monthly Trend of Bike Rentals**: A line chart showing the total number of bike rentals for each month, with the highest value highlighted.
- **Effect of Season on Bike Rentals**: A bar chart showing the total number of bike rentals for each season, with the highest value highlighted.
- **User Profile**: A pie chart showing the proportion of casual and registered users.
- **Effect of Holidays on Bike Rentals**: A bar chart showing the average number of bike rentals on holidays and non-holidays, with the highest value highlighted.
- **Mean Shift Clustering Analysis**: A scatter plot clustering the data based on environmental variables like temperature and windspeed.


## License

This project is licensed under the MIT License.
