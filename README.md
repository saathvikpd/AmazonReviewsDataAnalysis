# Amazon Reviews Data Analysis
Group 19 ECE 143 Project

## Dataset
Amazon review dataset collected by UCSD McAuley lab: ([Amazon review dataset](https://amazon-reviews-2023.github.io/)) 

This dataset contains reviews grouped into many item categories (appliances, automotive, toys and games, baby products, etc.). The dataset spans from May. 1996 - Sep.2023, and contains information such as rating, helpful votes, review message, verified purchase tag, and product metadata (overall rating, number of ratings, price, etc.) 

## Project Structure

```
AmazonReviewsDataAnalysis/
├── Data_filter/                    # Original data filtering utilities
├── Helpfulness_analysis/          # Helpfulness analysis pipeline
│   ├── helpfulness_analysis.py    # Main analysis script
│   └── helpfulness_summary.csv   # Output results
├── meta_categories/               # Product metadata JSONL files
├── review_categories/            # Review data JSONL files
├── reviews_over_time/             # Time series analysis scripts
└── README.md
```

## Helpfulness Analysis

### Overview
This analysis examines what factors make Amazon reviews more likely to receive "helpful" votes from other users. It processes 5 product categories and computes metrics from multiple dimensions.

### Categories Analyzed
- Appliances
- All_Beauty
- Handmade_Products
- Software
- Magazine_Subscriptions

### How It Works

#### 1. Data Loading & Merging
The pipeline loads two JSONL files for each category:
- **Review data** (`review_categories/{category}.jsonl`): Contains individual user reviews with rating, text, helpful_vote, verified_purchase, etc.
- **Metadata** (`meta_categories/meta_{category}.jsonl`): Contains product-level information including price

These are merged on `parent_asin` (the product ID).

#### 2. Feature Engineering
The following derived columns are created:
- `helpful_any`: Binary flag (1 if review received any helpful votes, 0 otherwise)
- `word_count`: Number of words in the review text
- `super_short`: Binary flag (1 if word_count < 3)
- `length_bin`: Categorical bin for review length [0-2, 3-19, 20-49, 50-99, 100-199, 200-399, 400+]
- `price_bucket`: Low/Mid/High tercile based on product price

#### 3. Metrics Computed
For each category, the pipeline computes 6 metrics:

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **One_Star** | % of 1-star reviews that received helpful votes | `groupby(rating==1).mean(helpful_any)` |
| **Five_Star** | % of 5-star reviews that received helpful votes | `groupby(rating==5).mean(helpful_any)` |
| **Long_400plus** | % of reviews with 400+ words that received helpful votes | `groupby(length_bin=="400+").mean(helpful_any)` |
| **Super_Short** | % of reviews with <3 words that received helpful votes | `groupby(super_short==1).mean(helpful_any)` |
| **Verified_Delta** | Difference in helpful rate between verified and unverified purchases | `helpful(verified=True) - helpful(verified=False)` |
| **High_Price** | % of reviews for high-price products (top tercile) that received helpful votes | `groupby(price_bucket=="High").mean(helpful_any)` |

### Output

The analysis produces `Helpfulness_analysis/helpfulness_summary.csv` with the following format:

```csv
Category,One_Star,Five_Star,Long_400plus,Super_Short,Verified_Delta,High_Price
Appliances,0.369,0.145,0.884,0.051,-0.184,0.234
All_Beauty,0.3,0.259,0.717,0.121,-0.017,0.349
Handmade_Products,0.346,0.227,0.7,0.138,0.009,0.309
Software,0.54,0.397,0.867,0.305,-0.042,0.489
Magazine_Subscriptions,0.734,0.344,0.964,0.132,-0.324,
```

### Running the Analysis

```bash
cd Helpfulness_analysis
python helpfulness_analysis.py
```

Output will be saved to `helpfulness_summary.csv` in the same directory.

### Key Findings

1. **Extremity Bias**: 1-star reviews consistently receive more helpful votes than 5-star reviews across all categories

2. **Length Effect**: Longer reviews (400+ words) have dramatically higher helpful rates (70-96%) compared to super-short reviews (<3 words, 5-30%)

3. **Verified Purchase**: Counterintuitively, unverified reviews often receive more helpful votes than verified ones (negative Delta in 4/5 categories)

4. **Price Effect**: High-price product reviews tend to receive more helpful votes (23-49% range)

## How to run code

```bash
# Run data filtering
python Data_filter/dataset_filter.py

# Run reviews over time analysis
python reviews_over_time/reviews_over_time.py

# Run statistical tests
python reviews_over_time/stats_tests.py

# Run helpfulness analysis
python Helpfulness_analysis/helpfulness_analysis.py

# Run Jupyter notebook
jupyter notebook reviews_over_time/analysis_nb.ipynb
```

## Third-Party Modules used
1. Pandas + Numpy
2. Matplotlib
3. Statsmodels
4. json (built-in)
