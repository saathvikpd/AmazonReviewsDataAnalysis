import pandas as pd
import matplotlib.pyplot as plt
from dataset_filter import process_reviews

def plot_reviews_over_time(category):
    
    # Ensure the corresponding file paths exist in your local
    input_file_review = f"../../review_categories/{category}.jsonl"
    input_file_meta = f"../../meta_categories/meta_{category}.jsonl"

    # Load reviews data
    reviews = process_reviews(
        input_review_filename = input_file_review,
        input_meta_filename= input_file_meta,                      
        review_fields_to_keep= ['parent_asin', 'timestamp', 'helpful_vote'] 
    )

    # Keep only the necessary columns
    reviews = reviews[["parent_asin", "timestamp", "helpful_vote"]]

    # Get review counts for each ASIN
    counts = reviews.groupby("parent_asin").agg({'timestamp': 'count', 'helpful_vote': 'sum'}).rename({"timestamp": "num_reviews"}, axis = 1).sort_values(by = "num_reviews", ascending = False).reset_index()

    # Retrieve the top 10 percent of all ASINs based on review counts
    perc90 = counts.num_reviews.quantile(0.9)
    counts90 = counts[counts.num_reviews >= perc90]
    counts90 = counts90[["parent_asin"]]
    reviews90 = pd.merge(reviews, counts90, on = 'parent_asin', how = "inner")

    # Parse the timestamp column
    reviews90.timestamp = pd.to_datetime(reviews90.timestamp, format = "(%m, %d, %Y)")

    # Group review counts and helpful votes by ASIN and month
    reviews90_monthly_data = reviews90.groupby(["parent_asin", pd.Grouper(key='timestamp', freq='MS')]).agg({'timestamp': 'count', 'helpful_vote': 'sum'})
    unstacked = reviews90_monthly_data.unstack(level='parent_asin')
    continuous_data = unstacked.asfreq('MS').fillna(0)
    flattened_data = continuous_data.groupby(level=0, axis=1).mean()
    reviews90_monthly_data = flattened_data.rename({"timestamp": "num_reviews", "helpful_vote": "num_helpful_votes"}, axis = 1).reset_index()

    # Plot the data
    reviews90_monthly_agg = reviews90_monthly_data.groupby("timestamp")[["num_reviews", "num_helpful_votes"]].mean().reset_index()
    ax = reviews90_monthly_agg.plot(x = "timestamp", y = ["num_reviews", "num_helpful_votes"], secondary_y = ["num_helpful_votes"], kind = "line", title = f"Reviews over time, Category: '{category}'")
    plt.savefig(f'plots/{category}.png')

    # Extract data from the plot
    line1 = ax.get_lines()[0]
    line2 = ax.right_ax.get_lines()[0]
    
    time = line1.get_xdata()
    num_reviews = line1.get_ydata()
    helpful_votes = line2.get_ydata()

    return time, num_reviews, helpful_votes