import plotly.express as px
from dash import Input, Output, callback
import pandas as pd

from data import df
from util.filters import filter_by_neighbourhood_group, filter_outliers

# Explicitly make a copy of the DataFrame after filter
filtered_df = filter_outliers(df, 'price').copy()

# Replace 'No rating' with None, then convert to numeric
filtered_df['rating'] = filtered_df['rating'].replace('No rating', None)
filtered_df['price'] = pd.to_numeric(filtered_df['price'], errors='coerce')
filtered_df['rating'] = pd.to_numeric(filtered_df['rating'], errors='coerce')

# Drop rows with NaN values in price or rating
filtered_df = filtered_df.dropna(subset=['price', 'rating'])


@callback(
    Output('price-rating-line-chart', 'figure'),
    Input('area-select', 'value')
)
def update_price_rating_scatter(selected_area):
    if selected_area == "New York City":
        fig = px.scatter(
            filtered_df,
            x="price",
            y="rating",
            opacity=0.4,
            color="neighbourhood_group",
            trendline="ols",
            title="Price - Rating Correlation in New York City"
        )
        fig.update_layout(
            xaxis_title="Price",
            yaxis_title="Rating",
            scattermode="group"
        )
        return fig

    # Filter data based on area
    filtered_data = filter_by_neighbourhood_group(filtered_df, neighbourhood_group=selected_area, threshold=0.03)
    fig = px.scatter(
        filtered_data,
        x="price",
        y="rating",
        opacity=0.4,
        color="neighbourhood",
        trendline="ols",
        title=f"Price - Rating Correlation in {selected_area}"
    )
    fig.update_layout(
        xaxis_title="Price",
        yaxis_title="Rating"
    )
    return fig

