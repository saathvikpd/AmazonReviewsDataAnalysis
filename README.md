# Amazon Reviews Data Analysis
Group 19 ECE 143 Project

## Dataset
Amazon review dataset collected by UCSD McAuley lab: ([Amazon review dataset](https://amazon-reviews-2023.github.io/)) 

This dataset contains reviews grouped into many item categories (appliances, automotive, toys and games, baby products, etc.). The dataset spans from May. 1996 - Sep.2023, and contains information such as rating, helpful votes, review message, verified purchase tag, and product metadata (overall rating, number of ratings, price, etc.) 

## Project Structure

```
AmazonReviewsDataAnalysis/
├── Data_filter/                    # Data filtering utilities
├── Helpfulness_analysis/           # Helpfulness analysis pipeline
│   ├── helpfulness_analysis.py     # Main analysis script
│   └── helpfulness_summary.csv     # Output results
├── reviews_over_time/              # Time series analysis scripts
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

### How to Run Files
Running "helpfulness.py" where a folder named "review_categories" contains all review data and folder named "meta_categories" has all meta data files. This will generate a .csv file that conducts 3 helpfulness test metrics across all categories.

1. Star Rating
2. review message length
3. Verified purchase





## Third-Party Modules used
1. Pandas + Numpy
2. Matplotlib
3. Statsmodels
4. Seaborn
