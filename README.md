# Amazon Reviews Data Analysis
Group 19 ECE 143 Project

## Dataset
Amazon review dataset collected by UCSD McAuley lab: ([Amazon review dataset](https://amazon-reviews-2023.github.io/))

This dataset contains reviews grouped into many item categories (appliances, automotive, toys and games, baby products, etc.). The dataset spans from May. 1996 - Sep.2023, and contains information such as rating, helpful votes, review message, verified purchase tag, and product metadata (overall rating, number of ratings, price, etc.)

## Project Structure

G:\AmazonReviewsDataAnalysis/
│
├── csv/
│ ├── helpfulness_summary.csv
│ ├── image_helpfulness_final_summary.csv
│ └── plot_ready_img_help.csv
│
├── meta_categories/
│ ├── meta_All_Beauty.jsonl   --- all .jsonl files are git-ignored
│ ├── meta_Appliances.jsonl
│ ├── meta_Digital_Music.jsonl
│ ├── meta_Gift_Cards.jsonl
│ ├── meta_Handmade_Products.jsonl
│ ├── meta_Magazine_Subscriptions.jsonl
│ └── meta_Software.jsonl
│
├── plots/
│ └── (generated plot images will be saved here)
│
├── review_categories/  --- all .jsonl files are git-ignored
│ ├── All_Beauty.jsonl
│ ├── Appliances.jsonl
│ ├── Digital_Music.jsonl
│ ├── Gift_Cards.jsonl
│ ├── Handmade_Products.jsonl
│ ├── Magazine_Subscriptions.jsonl
│ └── Software.jsonl
│
├── scripts/
│ ├── pycache/
│ ├── init.py
│ ├── dataset_filter.py
│ ├── reviews_over_time.py
│ └── stats_tests.py
│
├── analysis_nb.ipynb ----------------------------- these three notebooks are here temporarily till merge in final_notebook.ipynb is completed
├── final_notebook.ipynb
└── run_analysis_image_helpfulness.ipynb